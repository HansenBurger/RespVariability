import sys, pathlib
import pandas as pd

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess

form_mode_loc = InIReaWri.ConfigR('FormRoute', 'RecordForm', conf=None)
form_baguan_loc = InIReaWri.ConfigR('FormRoute', 'BaguanForm', conf=None)

timecol_format = ['Record_t', 'endo_t']

mode_col_map = {
    'PID': 'PID',
    'RecordTime': 'Record_t',
    'VentType': 'vent_t',
    'VentMode': 'vent_m'
}

baguan_col_map = {'PID': 'PID', 'ExTime': 'endo_t'}

df_mode = FormProcess.FormPreProcess(form_mode_loc,
                                     mode_col_map,
                                     sort_jud='PID')
df_baguan = FormProcess.FormPreProcess(form_baguan_loc,
                                       baguan_col_map,
                                       sort_jud='PID')

FormProcess.TimeShift(df_mode, timecol_format)
FormProcess.TimeShift(df_baguan, timecol_format)

# process1 filt
