import sys, pathlib
import table_filter_func_1 as func

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess
from Code.Fundal import basic

form_concat_loc = InIReaWri.ConfigR('FormRoute', 'MainDataForm', conf=None)
form_baguan_loc = InIReaWri.ConfigR('FormRoute', 'BaguanForm', conf=None)
form_record_loc = InIReaWri.ConfigR('FormRoute', 'RecordParaInfo', conf=None)
save_loc = InIReaWri.ConfigR('ResultRoute', 'FormFolder_new', conf=None)

#-----Step0: generate-----

timecol_format1 = [
    '入ICU时间', '出ICU时间', '上机时间', '撤机', 'record_time', '记录时间_1', '记录时间_2'
]

timecol_format2 = [
    'FirstMVTime', 'SBTTime', 'ExTime', 'WeanTime', 'BackOnTime', 'ICUInTime',
    'ICUOutTime', 'HPInTime', 'HPOutTime'
]

df_concat = FormProcess.FormPreProcess(form_concat_loc, ['上机时间'],
                                       'patient_id',
                                       add_index=False)
df_baguan = FormProcess.FormPreProcess(form_baguan_loc,
                                       sort_jud='PID',
                                       add_index=False)
df_record_para = FormProcess.FormPreProcess(form_record_loc,
                                            sort_jud='PID',
                                            add_index=False)

FormProcess.TimeShift(df_concat, timecol_format1)
FormProcess.TimeShift(df_baguan, timecol_format2)

#-----Step1: filt-----

result_ = func.TimeFilter(df_concat, df_baguan)
pid_miss_index = result_[0]
time_miss_index = result_[1]
filted_index_dict = result_[2]

#------Step2: build------

concat_name_map = {
    'PID': 'patient_id',
    'Record_t': 'record_time',
    'Record_id': 'record_id',
    'Resp_t': '记录时间_1',
    'Resp_id': 'RID_1',
    'zdt_1': 'zdt_1',
    'zpx_1': 'zpx_1',
    'Heart_id': 'RID_2',
    'Heart_t': '记录时间_2',
    'zdt_2': 'zdt_2',
    'zpx_2': 'zpx_2'
}

baguan_name_map = {
    'PID': 'PID',
    'endo_t': 'ExTime',
    'endo_end': 'WeaningStatus',
    'SBT_info': 'SBTInfo',
    'SBT_time': 'SBTTime',
    'SBT_Type': 'SBTType'
}

# filted_dict_half = basic.FromkeysReid(list(concat_name_map.keys()))
time_miss_dict = basic.FromkeysReid(list(baguan_name_map.keys()))
pid_miss_dict = basic.FromkeysReid(list(baguan_name_map.keys()))
filted_save_dict = {
    **basic.FromkeysReid(list(concat_name_map.keys())),
    **basic.FromkeysReid(list(baguan_name_map.keys()))
    # 不能用time_miss取地址会自动补
}

func.TableBuild1(filted_index_dict, df_concat, df_baguan, concat_name_map,
                 baguan_name_map, filted_save_dict)
func.TableBuild2(time_miss_index, df_baguan, baguan_name_map, time_miss_dict)
func.TableBuild2(pid_miss_index, df_baguan, baguan_name_map, pid_miss_dict)

#-------Step3: save-------

save_name_list = ['filted_r_new.csv', 'time_miss_new.csv', 'pid_miss_new.csv']

FormProcess.CsvToLocal(filted_save_dict, save_loc, save_name_list[0])
FormProcess.CsvToLocal(time_miss_dict, save_loc, save_name_list[1])
FormProcess.CsvToLocal(pid_miss_dict, save_loc, save_name_list[2])