import os
import pandas as pd
from Code import InIReaWri

save_loc = InIReaWri.ConfigR("ResultRoute", "FormFolder", conf=None)
rsbi_loc = os.path.join(save_loc, "rsbi_r.csv")

df_rsbi = pd.read_csv(rsbi_loc)
df_rsbi = df_rsbi.dropna(axis=0, how="any", subset=["Resp_t"])
df_rsbi = df_rsbi.sort_values(by="Record_t")
df_rsbi = df_rsbi.reset_index(drop=True)

rsbi_c_loc = os.path.join(save_loc, "rsbi_c.csv")
pd.DataFrame.to_csv(df_rsbi, rsbi_c_loc, index=False)
