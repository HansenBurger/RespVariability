import pandas as pd
from datetime import datetime

format_concat_loc = r"Data\Format\DATA.csv"
format_baguan_loc = r"Data\Format\vent_baguan.csv"

df_concat = pd.read_csv(format_concat_loc)
df_baguan = pd.read_csv(format_baguan_loc)

df_concat.dropna(axis=0, how="any", subset=["记录时间_1"], inplace=True)
df_concat.sort_values(by="patient_id", ascending=False, inplace=True)
df_concat.reset_index(drop=True, inplace=True)

df_baguan.sort_values(by="patient_id", ascending=False, inplace=True)
df_baguan.reset_index(drop=True, inplace=True)


def TimeShift(df_name, dt_format, column_names):
    for i in df_name.columns:
        if i in column_names:
            if len(df_name.loc[0, i].split("-")) == 1:
                df_name[i] = pd.to_datetime(df_name[i], format=dt_format[0])
            else:
                df_name[i] = pd.to_datetime(df_name[i], format=dt_format[1])


timecol_names = ["入ICU时间", "出ICU时间", "上机时间", "撤机", "record_time", "记录时间_1"]
datetime_format = ["%Y/%m/%d %X", "%Y-%m-%d %X"]

TimeShift(df_concat, datetime_format, timecol_names)
TimeShift(df_baguan, datetime_format, timecol_names)

