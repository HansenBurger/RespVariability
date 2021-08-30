import sys, pathlib
import pandas as pd

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri

#   Add Path

save_loc = InIReaWri.ConfigR("ResultRoute", "FormFolder", conf=None)
form_name_list = [
    "filted_r_new.csv", 'filted_c_new.csv', 'records_lack_new.csv'
]

filted_form_loc = pathlib.Path(save_loc) / form_name_list[0]
save_form_1_loc = pathlib.Path(save_loc) / form_name_list[1]
save_form_2_loc = pathlib.Path(save_loc) / form_name_list[2]

#   Form filted

df = pd.read_csv(filted_form_loc)

filt_lack_0 = (df['zdt_1'].notna()) & (df['zpx_1'].notna())
filt_lack_1 = (df['zdt_1'].isna()) | (df['zpx_1'].isna())
filt_monitor_0 = df['Record_id'].eq(df['Resp_id'], fill_value=0)
filt_monitor_1 = df['Record_id'].ne(df['Resp_id'], fill_value=0)

df_0 = df.loc[filt_lack_0 & filt_monitor_0]  # the records reached norm
df_1 = df.loc[filt_lack_1 | filt_monitor_1]  # the records be filted

df_0 = df_0.sort_values(by=['PID', 'Record_t', 'Resp_t'])
df_1 = df_1.sort_values(by=['PID', 'Record_t', 'Resp_t'])

pd.DataFrame.to_csv(df_0, save_form_1_loc, index=False)
pd.DataFrame.to_csv(df_1, save_form_2_loc, index=False)