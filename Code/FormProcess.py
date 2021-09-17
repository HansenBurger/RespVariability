import pandas as pd
from pathlib import Path


def FormPreProcess(df_loc,
                   col_map=None,
                   drop_jud=None,
                   sort_jud=None,
                   reset_jud=True,
                   nan_none=True):
    '''
    df_loc: location of csv (str)
    drop_jud: removal of invalid rows based on column names (list)
    sort_jud: sort the dataframe by column name (str, list)
    reset_jud: reset the index (default true)
    add_index: add "Index" column at the end (default true)
    '''

    if col_map:
        if type(col_map) == dict:
            df_tmp = pd.read_csv(df_loc, usecols=list(col_map.keys()))
            df_tmp = df_tmp.rename(columns=col_map)
        if type(col_map) == list:
            df_tmp = pd.read_csv(df_loc, usecols=col_map)
    else:
        df_tmp = pd.read_csv(df_loc)

    if drop_jud:
        df_tmp = df_tmp.dropna(axis=0, how="any", subset=drop_jud)

    if sort_jud:
        df_tmp = df_tmp.sort_values(by=sort_jud, ascending=True)
        try:
            df_tmp[sort_jud] = df_tmp[sort_jud].astype("uint32")
        except:
            print(sort_jud, ':unable to do type conversion')

    if reset_jud:
        df_tmp = df_tmp.reset_index(drop=True)

    if nan_none:
        df_tmp = df_tmp.where(df_tmp.notnull(), None)

    return df_tmp


def TimeShift(df, column_names):
    '''
    df: the dataframe to be processed (str)
    column_names: column name of the type that needs to be changed (list)
    '''

    date_format = ['%Y/%m/%d %X', '%Y-%m-%d %X', '%Y-%m-%d %H:%M']

    for i in df.columns:

        if i in column_names:

            for fmt in date_format:
                try:
                    df[i] = pd.to_datetime(df[i], format=fmt)
                    break
                except ValueError:
                    print(
                        'The "{0}" of table cannot find the corresponding time format'
                        .format(i))
                    pass


def CsvToLocal(table, save_loc, save_name):
    '''
    dict_: the dict that needs to be converted to a form (dict)
    save_loc: main folder to save the form (str)
    save_name: form name"xxx.csv" (str)
    '''

    route = Path(save_loc) / (save_name + '.csv')
    if type(table) == dict:
        df = pd.DataFrame.from_dict(table)
    else:
        df = table
    pd.DataFrame.to_csv(df, route, index=False)
    print('Save the current table to "{0}" complete.'.format(str(route)))


def PrintTableInfor(df, unicol):
    # can add basic info
    print('TableSize: ', df.shape, '\n', '"', unicol, '"', 'length: ',
          len(df[unicol].unique()))


def LocatIndex(df, col, value):
    '''
    df: dataframe to be search
    col: df column name to seach (string, list)
    value: the locat value
    '''
    index_list = []
    gp = df.groupby(col)
    df_tmp = gp.get_group(value)
    for i in df_tmp.index:
        index_list.append(i)

    return index_list