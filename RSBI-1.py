import os
import pandas as pd
from datetime import datetime, timedelta
from copy import deepcopy

# import sys
# sys.path.insert(1, "")

from Code import InIReaWri, FormPreProcess

# format_concat_loc = r"Data\Format\DATA.csv"
# format_baguan_loc = r"Data\Format\vent_baguan.csv"

form_concat_loc = InIReaWri.ConfigR("FormRoute", "MainDataForm", conf=None)
form_baguan_loc = InIReaWri.ConfigR("FormRoute", "BaguanForm", conf=None)
save_loc = InIReaWri.ConfigR("ResultRoute", "FormFolder", conf=None)

timecol_names = [
    "入ICU时间",
    "出ICU时间",
    "上机时间",
    "撤机",
    "record_time",
    "记录时间_1",
    "插管时间",
    "拔管时间",
    "撤机时间",
    "第一次SBT时间",
]

datetime_format = ["%Y/%m/%d %X", "%Y-%m-%d %X"]

pid_miss_index = []
time_miss_index = []
rsbi_index_list = []

df_concat = FormPreProcess.FormProcess(form_concat_loc, "patient_id")
df_baguan = FormPreProcess.FormProcess(form_baguan_loc, "patient_id")

FormPreProcess.TimeShift(df_concat, datetime_format, timecol_names)
FormPreProcess.TimeShift(df_baguan, datetime_format, timecol_names)

gp_concat = df_concat.groupby("patient_id")
gp_baguan = df_baguan.groupby("patient_id")

for pid in df_baguan["patient_id"].unique():

    try:
        df_tmp_concat = gp_concat.get_group(pid)
        df_tmp_baguan = gp_baguan.get_group(pid)
        df_tmp_concat = df_tmp_concat.sort_values(by="record_time")
        df_tmp_baguan = df_tmp_baguan.sort_values(by="拔管时间")
    except:
        pid_miss_index.append(pid)
        print(pid)
        continue

    for i in df_tmp_baguan.index:

        time_post = df_tmp_baguan.loc[i, "拔管时间"]
        time_forw = time_post - timedelta(hours=2)
        index_tmp_list = []

        for j in df_tmp_concat.index:
            time_ = df_tmp_concat.loc[j, "record_time"]
            if time_ <= time_post and time_ > time_forw:
                index_tmp_list.append(df_tmp_concat.loc[j, "Index"])
            # elif time_ > time_post:
            #     break

        if not index_tmp_list:
            time_miss_index.append(df_tmp_baguan.loc[i, "Index"])
        else:
            index_tmp_list.append(df_tmp_baguan.loc[i, "Index"])
            rsbi_index_list.append(index_tmp_list)

rsbi_map = {
    "PID": "patient_id",
    "Record_t": "record_time",
    "Record_id": "record_id",
    "Resp_t": "记录时间_1",
    "zdt_1": "zdt_1",
    "zpx_1": "zpx_1",
    "Heart_t": "记录时间_2",
    "zdt_2": "zdt_2",
    "zpx_2": "zpx_2",
    "tracheotomy": "气切（气切=1）",
    "endo_t": "拔管时间",
    "endo_end": "拔管结局（失败=1）",
    "SBT_time": "第一次SBT时间",
    "SBT_days": "第一次SBT到撤机的时间（天）",
}

rsbi_name = list(rsbi_map.keys())
rsbi_dict = dict.fromkeys(rsbi_name, [])

for i in rsbi_name:
    new_list = []
    rsbi_dict[i] = deepcopy(new_list)

for i in rsbi_index_list:

    copy_times = len(i[:-1])
    concat_id = i[:-1]
    baguan_id = i[-1]

    concat_info = df_concat.loc[concat_id]
    baguan_info = df_baguan.iloc[baguan_id]

    for j in rsbi_name:

        tmp = []

        if j in rsbi_name[:9]:
            tmp.append(concat_info[rsbi_map[j]].tolist())
            rsbi_dict[j].extend(tmp[0])

        else:
            for x in range(copy_times):
                tmp.append(baguan_info[rsbi_map[j]])
            rsbi_dict[j].extend(tmp)

df_time_miss = df_baguan.loc[time_miss_index]
df_time_miss = df_time_miss.drop(labels="Unnamed: 0", axis=1)
df_rsbi = pd.DataFrame.from_dict(rsbi_dict)

rsbi_save_route = os.path.join(save_loc, "rsbi_r.csv")
time_miss_route = os.path.join(save_loc, "df_time_miss.csv")

pd.DataFrame.to_csv(df_rsbi, rsbi_save_route, index=False)
pd.DataFrame.to_csv(df_time_miss, time_miss_route, index=False)
