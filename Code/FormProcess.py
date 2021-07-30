import pandas as pd
from pathlib import Path


def FormPreProcess(df_loc,
                   drop_jud=None,
                   sort_jud=None,
                   reset_jud=True,
                   add_index=True):
    '''
    df_loc: location of csv (str)
    drop_jud: removal of invalid rows based on column names (list)
    sort_jud: sort the dataframe by column name (str, list)
    reset_jud: reset the index (default true)
    add_index: add "Index" column at the end (default true)
    '''

    df_tmp = pd.read_csv(df_loc)
    #   df_tmp = pd.read_csv(df_loc, index_col=0)
    #   TODO:the index_col = 0 cause the astype error

    if drop_jud is not None:
        df_tmp = df_tmp.dropna(axis=0, how="any", subset=drop_jud)

    if sort_jud is not None:
        df_tmp = df_tmp.sort_values(by=sort_jud, ascending=True)
        try:
            df_tmp[sort_jud] = df_tmp[sort_jud].astype("uint32")
        except:
            print(sort_jud, ':unable to do type conversion')

    if reset_jud:
        df_tmp = df_tmp.reset_index(drop=True)

    if add_index:
        df_tmp["Index"] = df_tmp.index

    return df_tmp


def TimeShift(df_name, column_names):
    '''
    df_name: the dataframe to be processed (str)
    column_names: column name of the type that needs to be changed (list)
    '''

    date_format = {"/": "%Y/%m/%d %X", "-": "%Y-%m-%d %X"}
    date_split = list(date_format.keys())

    for i in df_name.columns:

        if i in column_names:

            index_num = 0

            while pd.isna(df_name.loc[index_num, i]):
                index_num = index_num + 1

            judge_cell = str(df_name.loc[index_num, i])

            for j in range(len(date_split)):
                date_split_mark = date_split[j]
                date_format_select = date_format[date_split_mark]

                if len(judge_cell.split(date_split_mark)) > 1:
                    df_name[i] = pd.to_datetime(df_name[i],
                                                format=date_format_select)


def CsvToLocal(dict_, save_loc, save_name):
    '''
    dict_: the dict that needs to be converted to a form (dict)
    save_loc: main folder to save the form (str)
    save_name: form name"xxx.csv" (str)
    '''

    route = Path(save_loc) / save_name
    df = pd.DataFrame.from_dict(dict_)
    pd.DataFrame.to_csv(df, route, index=False)
