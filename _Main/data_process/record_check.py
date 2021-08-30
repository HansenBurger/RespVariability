import sys, pathlib, datetime
import pandas as pd

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess, PointProcess
from Code.Fundal import BinImport, ReadSamplerate

vent_machine_list = []
vent_mode_name_list = []
vent_still_time_list = []

#   Import Data

data_folder = InIReaWri.ConfigR('SampleDataRoute', 'FiltedData', conf=None)
save_loc = InIReaWri.ConfigR("ResultRoute", "FormFolder", conf=None)
form_loc = pathlib.Path(
    InIReaWri.ConfigR('ResultRoute', 'FormFolder',
                      conf=None)) / 'filted_c_new.csv'
form_test_loc = r'C:\Users\HY_Burger\Desktop\Project\RespVariability\test.csv'
#   Form Process

time_columns = ['Record_t', 'Resp_t', 'Heart_t', 'endo_t', 'SBT_time']
time_column = ['Record_t', 'Resp_t', 'endo_t']
#   time_columns = ['Record_t', 'Resp_t', 'endo_t']
df = FormProcess.FormPreProcess(form_loc, add_index=False)
FormProcess.TimeShift(df, time_columns)

#   read the info


def RouteCombine(serie, file_level_list):
    '''
    level_0: main folder location
    level_1: time name
    level_2: record name
    '''

    level_0 = file_level_list[0]
    level_1 = file_level_list[1]
    level_2 = file_level_list[2]

    loc = pathlib.Path(level_0) / (str(serie[level_1].year) + str(
        serie[level_1].month).rjust(2, '0')) / serie[level_2]  # 月份保留两位小数

    return loc


total_t = 0

for i in df.index:

    start_time = datetime.datetime.now()

    file_level_list = [data_folder, 'Record_t', 'Record_id']
    record_folder = RouteCombine(df.iloc[i], file_level_list)

    zif = pathlib.Path(record_folder) / (df.iloc[i]['Resp_id'] + '.zif')
    zdt = pathlib.Path(record_folder) / (df.iloc[i]['zdt_1'] + '.zdt')
    zpx = pathlib.Path(record_folder) / (df.iloc[i]['zpx_1'] + '.zpx')

    vent_machine = BinImport.ImportZif(zif)['machineType'].split(
        '-')[0] if zif.stat().st_size >= 100 else None
    wave_outputs = BinImport.ImportWaveHeader(
        zdt)[0] if zdt.stat().st_size >= 100 else {}
    para_outputs = BinImport.ImportPara(
        zpx)[0] if zpx.stat().st_size >= 100 else {}
    process_result = PointProcess.PointProcessing(
        zdt) if zdt.stat().st_size >= 100 else [[], [], [], [], [], 0]

    vent_mode_name = None if not vent_machine or not para_outputs else ReadSamplerate.ReadVentMode(
        vent_machine, para_outputs['st_VENT_TYPE'][0].item(),
        para_outputs['st_VENT_MODE'][0].item(),
        para_outputs['st_VENT_TYPE'][0].item())

    vent_still_time = 0 if not wave_outputs else (round(
        (process_result[0][-1] * 1 /
         wave_outputs['RefSampleRate']).item()) if process_result[0] else 0)

    vent_machine_list.append(vent_machine)
    vent_mode_name_list.append(vent_mode_name)
    vent_still_time_list.append(vent_still_time)

    end_time = datetime.datetime.now()
    time_scamp = (end_time - start_time).seconds
    total_t = total_t + time_scamp
    print('process the ',
          str(i + 1).rjust(4, '0'), ' row consume ', time_scamp, ' s')

print('total consuming time during process: ', total_t)

df['machine'] = vent_machine_list
df['vent_m'] = vent_mode_name_list
df['vent_t'] = vent_still_time_list
save_route_1 = pathlib.Path(save_loc) / 'machinetype_new.csv'
save_route_2 = 'test_result.csv'
# save_route_2 = pathlib.Path(save_loc) / 'machinetype_lack.csv'
pd.DataFrame.to_csv(df, save_route_1, index=False)
# pd.DataFrame.to_csv(df_lack, save_route_2, index=False)
