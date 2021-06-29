import pandas as pd


def FormProcess(df_loc, sort_jud):
    df_tmp = pd.read_csv(df_loc)
    df_tmp = df_tmp.dropna(axis=0, how="any", subset=["上机时间"])
    df_tmp = df_tmp.sort_values(by=sort_jud, ascending=True)
    df_tmp = df_tmp.reset_index(drop=True)

    df_tmp[sort_jud] = df_tmp[sort_jud].astype("uint32")
    df_tmp["Index"] = df_tmp.index

    return df_tmp


def TimeShift(df_name, dt_format, column_names):
    for i in df_name.columns:
        if i in column_names:
            index_num = 0
            while pd.isna(df_name.loc[index_num, i]):
                index_num = index_num + 1
            else:
                if len(str(df_name.loc[index_num, i]).split("-")) == 1:
                    df_name[i] = pd.to_datetime(df_name[i], format=dt_format[0])
                else:
                    df_name[i] = pd.to_datetime(df_name[i], format=dt_format[1])
