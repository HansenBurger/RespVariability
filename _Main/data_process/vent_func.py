import sys, pathlib, sqlite3
from traceback import print_tb

import pandas as pd
import vent_class_data as data
import vent_class_func as func
from datetime import datetime

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess
from Code.Fundal import basic

static = data.DataStatic()
dynamic = data.DataDynamic()


def SaveLocGenerate(module_name):

    form_info = static.file_loc_dict['save form']
    graph_info = static.file_loc_dict['save graph']
    now = datetime.now()
    folder_name = '{0}{1}{2}_{3}_{4}'.format(now.year,
                                             str(now.month).rjust(2, '0'),
                                             str(now.day).rjust(2, '0'),
                                             str(now.hour).rjust(2, '0'),
                                             module_name)

    save_form_loc = InIReaWri.ConfigR(type=form_info['category'],
                                      name=form_info['name'],
                                      conf=None)
    save_form_loc = pathlib.Path(save_form_loc) / folder_name
    save_form_loc.mkdir(parents=True, exist_ok=True)
    dynamic.save_form_loc = save_form_loc

    save_graph_loc = InIReaWri.ConfigR(type=graph_info['category'],
                                       name=graph_info['name'],
                                       conf=None)
    save_graph_loc = pathlib.Path(save_graph_loc) / folder_name
    save_graph_loc.mkdir(parents=True, exist_ok=True)
    dynamic.save_graph_loc = save_graph_loc


@basic.measure
def MainTableBuild():

    table_info = static.file_loc_dict['main table']
    table_loc = InIReaWri.ConfigR(type=table_info['category'],
                                  name=table_info['name'],
                                  conf=None)

    dynamic.df_main = FormProcess.FormPreProcess(df_loc=table_loc)
    FormProcess.TimeShift(df=dynamic.df_main, column_names=static.time_col)


@basic.measure
def MainTableBuild_db(table_name):
    db = r'C:\Main\Data\_\Database\sqlite\RespData_2201.db'
    query_state = '''
    SELECT * FROM {0}
    '''.format(table_name)
    with sqlite3.connect(db) as con:
        df = pd.read_sql(query_state, con)
    col_map = {
        'PID': 'PID',
        'ICU': 'ICU',
        'RID': 'Record_id',
        'REC_t': 'Resp_t',
        'zdt': 'zdt_1',
        'zpx': 'zpx_1',
        'Extube_t': 'endo_t',
        'Extube_end': 'endo_end',
        'machine': 'machine',
        'vent_t': 'vent_t',
        'vent_m_0': 'vent_m_0',
        'vent_m_1': 'vent_m_1',
        'vent_m_2': 'vent_m_2',
        'st_peep': 'st_peep',
        'st_ps': 'st_ps',
        'st_e_sens': 'st_e_sens',
        'st_sumP': 'st_sumP'
    }
    df = df.rename(columns=col_map)
    FormProcess.TimeShift(df, static.time_col)
    dynamic.df_main = df


@basic.measure
def TableRead_GP():

    colname = static.table_col_map
    pid_list = dynamic.df_main[colname['patient ID']].unique().tolist()
    gp_main = func.pd.DataFrame.groupby(dynamic.df_main, colname['patient ID'])

    for pid in pid_list:

        obj = data.PIDGPObj()
        df_tmp = gp_main.get_group(pid)

        obj.df = df_tmp
        obj.pid_s = df_tmp[colname['patient ID']]
        obj.icu_s = df_tmp[colname['ICU info']]
        obj.resp_t_s = df_tmp[colname['record time']]
        obj.endo_t_s = df_tmp[colname['exTube time']]
        obj.ending_s = df_tmp[colname['exTube end']]
        obj.still_t_s = df_tmp[colname['venting time']]
        obj.machine_s = df_tmp[colname['machine type']]
        obj.vtm_0_s = df_tmp[colname['vent m bin']]
        obj.vtm_1_s = df_tmp[colname['vent m mid']]
        obj.vtm_2_s = df_tmp[colname['vent m end']]
        obj.st_peep_s = df_tmp[colname['PEEP setting']]
        obj.st_ps_s = df_tmp[colname['PS setting']]
        obj.st_e_sens_s = df_tmp[colname['ESENS setting']]
        obj.st_sumP_s = df_tmp[colname['PEEP + PS']]

        dynamic.objlist_table.append(obj)


@basic.measure
def RecordValidate_GP():

    colname = static.table_col_map
    objlist = dynamic.objlist_table
    df_whole = FormProcess.FormPreProcess()

    for i in range(len(objlist)):

        process = func.Certify(objlist[i])
        process.EndtimeCertify()

        df_tmp = objlist[i].df
        df_whole = func.pd.concat([df_whole, df_tmp], ignore_index=True)

        if df_tmp.empty:
            objlist[i] = None
            continue
        else:
            objlist[i].pid_s = df_tmp[colname['patient ID']]
            objlist[i].icu_s = df_tmp[colname['ICU info']]
            objlist[i].resp_t_s = df_tmp[colname['record time']]
            objlist[i].endo_t_s = df_tmp[colname['exTube time']]
            objlist[i].ending_s = df_tmp[colname['exTube end']]
            objlist[i].still_t_s = df_tmp[colname['venting time']]
            objlist[i].machine_s = df_tmp[colname['machine type']]
            objlist[i].vtm_0_s = df_tmp[colname['vent m bin']]
            objlist[i].vtm_1_s = df_tmp[colname['vent m mid']]
            objlist[i].vtm_2_s = df_tmp[colname['vent m end']]
            objlist[i].st_peep_s = df_tmp[colname['PEEP setting']]
            objlist[i].st_ps_s = df_tmp[colname['PS setting']]
            objlist[i].st_e_sens_s = df_tmp[colname['ESENS setting']]
            objlist[i].st_sumP_s = df_tmp[colname['PEEP + PS']]

    dynamic.objlist_table = [i for i in objlist if i]
    dynamic.df_main = df_whole


@basic.measure
def CombineRecordsToPinfo():

    for obj_gp in dynamic.objlist_table:

        obj_pinfo = data.PIDInfoObj()
        process = func.Transmit(obj_gp, obj_pinfo)

        process.TransmitValue_Basic()
        process.TransmitValue_VM()
        process.TransmitValue_ST()
        dynamic.objlist_pinfo.append(obj_pinfo)
        del obj_pinfo, process

    max_len = max([len(obj.mode_list) for obj in dynamic.objlist_pinfo])

    for i in dynamic.objlist_pinfo:
        i.mode_list += [''] * (max_len - len(i.mode_list))
        i.st_peep_list += [None] * (max_len - len(i.st_peep_list))
        i.st_ps_list += [None] * (max_len - len(i.st_ps_list))
        i.st_sumP_list += [None] * (max_len - len(i.st_sumP_list))
        i.st_e_sens_list += [None] * (max_len - len(i.st_e_sens_list))


def ResultBuild_PID():

    colname = static.table_col_map
    objlist = dynamic.objlist_pinfo
    df = FormProcess.FormPreProcess()

    df[colname['patient ID']] = [obj.pid for obj in objlist]
    df[colname['ICU info']] = [obj.icu for obj in objlist]
    df[colname['exTube end']] = [obj.end_state for obj in objlist]
    df[colname['exTube time']] = [obj.end_time for obj in objlist]
    df[colname['machine type']] = [obj.machine for obj in objlist]

    dynamic.df_basic = df


def __ResultBuild_Main(para_info, para_value_list, form_name):

    colname = static.table_col_map
    df_left = dynamic.df_basic
    df_right = FormProcess.FormPreProcess()
    saveloc_graph = pathlib.Path(dynamic.save_graph_loc) / para_info[1]
    saveloc_graph.mkdir(parents=True, exist_ok=True)

    process = func.Charts(df_left, df_right, para_info, saveloc_graph)
    process.TableBuild(para_value_list)
    process.DFInfoOutput(df_right.columns[:6], colname['exTube end'])
    process.GroupBarPlot(df_right.columns[:6], colname['exTube end'])

    dynamic.df_s_para[para_info[1]] = df_right
    FormProcess.CsvToLocal(process.df_concat, dynamic.save_form_loc, form_name)


@basic.measure
def ResultBuild_VM():

    para_info = ['mode', 'ST_VM']
    para_list = [obj.mode_list for obj in dynamic.objlist_pinfo]
    form_save_name = static.save_table_name['30min vm distri']
    __ResultBuild_Main(para_info, para_list, form_save_name)


@basic.measure
def ResultBuild_ST_PEEP():

    para_info = ['peep', 'ST_PEEP']
    para_list = [obj.st_peep_list for obj in dynamic.objlist_pinfo]
    form_save_name = static.save_table_name['30min peep distri']
    __ResultBuild_Main(para_info, para_list, form_save_name)


@basic.measure
def ResultBuild_ST_PS():

    para_info = ['ps', 'ST_PS']
    para_list = [obj.st_ps_list for obj in dynamic.objlist_pinfo]
    form_save_name = static.save_table_name['30min ps distri']
    __ResultBuild_Main(para_info, para_list, form_save_name)


@basic.measure
def ResultBuild_ST_E_SENS():

    para_info = ['esens', 'ST_E_SENS']
    para_list = [obj.st_e_sens_list for obj in dynamic.objlist_pinfo]
    form_save_name = static.save_table_name['30min esens distri']
    __ResultBuild_Main(para_info, para_list, form_save_name)


@basic.measure
def ResultBuild_ST_SUMP():

    para_info = ['sumP', 'ST_SUMP']
    para_list = [obj.st_sumP_list for obj in dynamic.objlist_pinfo]
    form_save_name = static.save_table_name['30min sumP distri']
    __ResultBuild_Main(para_info, para_list, form_save_name)


def __TableProcess_SumPMain(mode, hours):
    colname = static.table_col_map
    df_record = dynamic.df_main
    df_basic = dynamic.df_basic
    df_vent = dynamic.df_s_para['ST_VM']
    df_sumP = dynamic.df_s_para['ST_SUMP']

    process = func.TableQuery(df_record, [df_basic, df_vent, df_sumP])
    process.TableFilt_PSV(df_vent.columns[:int(hours * 2 + 1)])
    process.TableFilt_SumP(df_sumP.columns[:int(hours * 2 + 1)], mode)
    process.ConcatQueryByTime(colname['patient ID'], hours)

    return process.df


@basic.measure
def TableProcess_SumP10(hour_set):

    filt_mode = 'sum_10'
    form_save_name = 'Records_{0}h_sumP10_PSV'.format(hour_set)
    result_df = __TableProcess_SumPMain(filt_mode, hour_set)

    FormProcess.CsvToLocal(result_df, dynamic.save_form_loc, form_save_name)


@basic.measure
def TableProcess_SumP12(hour_set):

    filt_mode = 'sum_12'
    form_save_name = 'Records_{0}h_sumP12_PSV'.format(hour_set)
    result_df = __TableProcess_SumPMain(filt_mode, hour_set)
    FormProcess.CsvToLocal(result_df, dynamic.save_form_loc, form_save_name)


@basic.measure
def TableProcess_PSV(hour_set):
    colname = static.table_col_map
    df_record = dynamic.df_main
    df_basic = dynamic.df_basic
    df_vent = dynamic.df_s_para['ST_VM']
    form_save_name = 'Records_{0}h_PSV'.format(hour_set)

    process = func.TableQuery(df_record, [df_basic, df_vent])
    process.TableFilt_PSV(df_vent.columns[:int(hour_set * 2 + 1)])
    process.ConcatQueryByTime(colname['patient ID'], hour_set)
    FormProcess.CsvToLocal(process.df, dynamic.save_form_loc, form_save_name)


@basic.measure
def TbaleProcess_PEEPInvalid():
    colname = static.table_col_map
    df_record = dynamic.df_main
    df_basic = dynamic.df_basic
    df_peep = dynamic.df_s_para['ST_PEEP']
    form_save_name = static.save_table_name['result: wh\'s invalid peep filt']

    process = func.TableQuery(df_record, [df_basic, df_peep])
    process.TableFilt_InvalidPeep(df_peep.columns)
    process.ConcatQueryByTime(colname['patient ID'])

    FormProcess.CsvToLocal(process.df, dynamic.save_form_loc, form_save_name)