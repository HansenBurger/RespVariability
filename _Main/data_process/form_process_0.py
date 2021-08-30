import sys, pathlib
import pandas as pd

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess

form_loc = InIReaWri.ConfigR("FormRoute", "BaguanForm", conf=None)
save_loc = InIReaWri.ConfigR("FormRoute", "SortData", conf=None)

col_name_list = ['patient_id', '拔管时间']
df = FormProcess.FormPreProcess(form_loc, add_index=False)
df_gp = pd.DataFrame.groupby(df, by=col_name_list[0])

df_index_list = []

for pid in df[col_name_list[0]].unique():

    df_tmp = df_gp.get_group(pid)
    df_tmp = df_tmp.sort_values(by=col_name_list[1])

    for i in df_tmp.index:
        if df_tmp.shape[0] >= 1:
            df_index_list.append(i)
            break
        else:
            continue

df = df.loc[df_index_list]
print('Form Length: ', df.shape[0])
print('PID Length: ', len(df[col_name_list[0]].unique()))

save_route = pathlib.Path(save_loc) / 'vent_baguan_c_.csv'
pd.DataFrame.to_csv(df, save_route, index=False)