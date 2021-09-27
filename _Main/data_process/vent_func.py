import sys, pathlib
import vent_class_data as data
import vent_class_func as func

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess
from Code.Fundal import basic

static = data.DataStatic()
dynamic = data.DataDynamic()


def SaveLocGenerate():

    form_info = static.file_loc_dict['save form']
    graph_info = static.file_loc_dict['save form']

    dynamic.save_form_loc = InIReaWri.ConfigR(type=form_info['category'],
                                              name=form_info['name'],
                                              conf=None)
    dynamic.save_graph_loc = InIReaWri.ConfigR(type=graph_info['category'],
                                               name=graph_info['name'],
                                               conf=None)


@basic.measure
def MainTableBuild():

    table_info = static.file_loc_dict['main table']
    table_loc = InIReaWri.ConfigR(type=table_info['category'],
                                  name=table_info['name'],
                                  conf=None)

    dynamic.df_main = FormProcess.FormPreProcess(df_loc=table_loc)
    dynamic.df_new = func.pd.DataFrame()

    FormProcess.TimeShift(df=dynamic.df_main, column_names=static.time_col)


@basic.measure
def GenerateObjList_gp():

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
        obj.machine_s = df_tmp[colname['machine type']]
        obj.vtm_0_s = df_tmp[colname['vent m bin']]
        obj.vtm_1_s = df_tmp[colname['vent m mid']]
        obj.vtm_2_s = df_tmp[colname['vent m end']]

        dynamic.obj_list_main.append(obj)


@basic.measure
def ValidateObjList_gp():

    colname = static.table_col_map
    objlist = dynamic.obj_list_main

    for i in range(len(objlist)):

        try:
            process = func.Certify(objlist[i])
            process.EndtimeCertify()
        except:
            break

        df_tmp = objlist[i].df

        if df_tmp.empty:
            del objlist[i]
            continue
        else:
            objlist[i].pid_s = df_tmp[colname['patient ID']]
            objlist[i].icu_s = df_tmp[colname['ICU info']]
            objlist[i].resp_t_s = df_tmp[colname['record time']]
            objlist[i].endo_t_s = df_tmp[colname['exTube time']]
            objlist[i].ending_s = df_tmp[colname['exTube end']]
            objlist[i].machine_s = df_tmp[colname['machine type']]
            objlist[i].vtm_0_s = df_tmp[colname['vent m bin']]
            objlist[i].vtm_1_s = df_tmp[colname['vent m mid']]
            objlist[i].vtm_2_s = df_tmp[colname['vent m end']]


@basic.measure
def GenerateObjList_pid():

    for obj_gp in dynamic.obj_list_main:

        obj_pid = data.VentModeObj()

        process = func.Transmit(obj_gp, obj_pid)
        process.TransmitValue()
        dynamic.obj_list_new.append(obj_pid)

        del obj_gp, obj_pid

    dynamic.vm_max_len = max(
        [len(obj.mode_list) for obj in dynamic.obj_list_new])

    for i in dynamic.obj_list_new:
        i.mode_list += [''] * (dynamic.vm_max_len - len(i.mode_list))
        del i


@basic.measure
def TableBuild():

    colname = static.table_col_map
    df = dynamic.df_new

    print(dynamic.df_new.shape)

    df[colname['patient ID']] = [obj.pid for obj in dynamic.obj_list_new]
    df[colname['ICU info']] = [obj.icu for obj in dynamic.obj_list_new]
    df[colname['exTube end']] = [obj.end_state for obj in dynamic.obj_list_new]
    df[colname['exTube time']] = [obj.end_time for obj in dynamic.obj_list_new]
    df[colname['machine type']] = [obj.machine for obj in dynamic.obj_list_new]

    for i in range(dynamic.vm_max_len):
        col_name_i = 'mode_' + str(i * 30).rjust(3, '0') + '_min'
        col_value_i = [obj.mode_list[i] for obj in dynamic.obj_list_new]
        df[col_name_i] = col_value_i
        del col_name_i, col_value_i

    print(dynamic.df_new.shape)

    FormProcess.CsvToLocal(df, dynamic.save_form_loc,
                           static.save_table_name['table result 1'])


@basic.measure
def TableProcess_1h():

    colname = static.table_col_map
    df_record = dynamic.df_main
    df_vent = dynamic.df_new

    process = func.TableQuery(df_record, df_vent)
    process.ConcatQuery([
        colname['patient ID'], colname['record time'], colname['exTube time']
    ])

    FormProcess.CsvToLocal(process.df, dynamic.save_form_loc,
                           static.save_table_name['table result 2'])
