import sys, pathlib
import pandas as pd

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri

save_loc = InIReaWri.ConfigR("ResultRoute", "FormFolder", conf=None)
form_name_list = ["filted_r.csv", 'records_lack.csv', 'filted_c.csv']

filted_form_loc = pathlib.Path(save_loc) / form_name_list[0]
save_form_1_loc = pathlib.Path(save_loc) / form_name_list[1]
save_form_2_loc = pathlib.Path(save_loc) / form_name_list[2]

df = pd.read_csv(filted_form_loc)

df_lack = df.loc[(df['zdt_1'].isna()) | (df['zpx_1'].isna())]
df_nona = df.dropna(axis=0, how='any', subset=['zdt_1', 'zpx_1'])
df_lack = df_lack.sort_values(by='Record_t')
df_nona = df_nona.sort_values(by='Record_t')

pd.DataFrame.to_csv(df_lack, save_form_1_loc, index=False)
pd.DataFrame.to_csv(df_nona, save_form_2_loc, index=False)