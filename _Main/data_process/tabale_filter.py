import sys, pathlib
import table_filter_func as func

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess
from Code.Fundal import basic

form_concat_loc = InIReaWri.ConfigR("FormRoute", "MainDataForm", conf=None)
form_baguan_loc = InIReaWri.ConfigR("FormRoute", "BaguanForm", conf=None)
save_loc = InIReaWri.ConfigR("ResultRoute", "FormFolder", conf=None)

#-----Step1: filt-----

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

df_concat = FormProcess.FormPreProcess(form_concat_loc, ['上机时间'], 'patient_id')
df_baguan = FormProcess.FormPreProcess(form_baguan_loc, sort_jud='patient_id')

FormProcess.TimeShift(df_concat, timecol_names)
FormProcess.TimeShift(df_baguan, timecol_names)

result_ = func.TimeFilter(df_concat, df_baguan)
pid_miss_index = result_[0]
time_miss_index = result_[1]
filted_index_list = result_[2]

#------Step2: build------

concat_name_map = {
    "PID": "patient_id",
    "Record_t": "record_time",
    "Record_id": "record_id",
    "Resp_t": "记录时间_1",
    "zdt_1": "zdt_1",
    "zpx_1": "zpx_1",
    "Heart_t": "记录时间_2",
    "zdt_2": "zdt_2",
    "zpx_2": "zpx_2"
}

baguan_name_map = {
    "PID": "patient_id",
    "tracheotomy": "气切（气切=1）",
    "endo_t": "拔管时间",
    "endo_end": "拔管结局（失败=1）",
    "SBT_time": "第一次SBT时间",
    "SBT_days": "第一次SBT到撤机的时间（天）"
}

combine_name_map = {**concat_name_map, **baguan_name_map}

filted_save_dict = basic.FromkeysReid(list(combine_name_map.keys()))
time_miss_dict = basic.FromkeysReid(list(baguan_name_map.keys()))

func.TableBuild1(filted_index_list, df_concat, df_baguan, combine_name_map,
                 concat_name_map, filted_save_dict)
func.TableBuild2(time_miss_index, df_baguan, baguan_name_map, time_miss_dict)

#-------Step3: save-------

save_name_list = ['filted_r.csv', 'time_miss.csv']

FormProcess.CsvToLocal(filted_save_dict, save_loc, save_name_list[0])
FormProcess.CsvToLocal(time_miss_dict, save_loc, save_name_list[1])