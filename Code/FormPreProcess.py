import pandas as pd


def FormProcess(df_loc, drop_jud=None, sort_jud=None, reset_jud=0):
    df_tmp = pd.read_csv(df_loc)
    if drop_jud is not None:
        df_tmp = df_tmp.dropna(axis=0, how="any", subset=drop_jud)
    if sort_jud is not None:
        df_tmp = df_tmp.sort_values(by=sort_jud, ascending=True)
        df_tmp[sort_jud] = df_tmp[sort_jud].astype("uint32")
    if not reset_jud:
        df_tmp = df_tmp.reset_index(drop=True)

    df_tmp["Index"] = df_tmp.index

    return df_tmp


def TimeShift(df_name, column_names):

    date_format = {"/": "%Y/%m/%d %X", "-": "%Y-%m-%d %X"}
    date_split = date_format.keys()

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
                    df_name[i] = pd.to_datetime(df_name[i], format=date_format_select)
