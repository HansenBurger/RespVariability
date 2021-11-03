import sys, pathlib
import table_class_data as data
import table_class_filt as func
from datetime import datetime

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess
from Code.Fundal import basic

static = data.DataStatic()
dynamic = data.DataDynamic()


def SaveLocGenerate(module_name):
    save_info = static.file_loc_dict['save_form']
    now = datetime.now()
    folder_name = '{0}{1}{2}_{3}_{4}'.format(now.year,
                                             str(now.month).rjust(2, '0'),
                                             str(now.day).rjust(2, '0'),
                                             str(now.hour).rjust(2, '0'),
                                             module_name)

    save_form_loc = InIReaWri.ConfigR(type=save_info['category'],
                                      name=save_info['name'],
                                      conf=None)
    save_form_loc = pathlib.Path(save_form_loc) / folder_name
    save_form_loc.mkdir(parents=True, exist_ok=True)
    dynamic.save_loc = str(save_form_loc)


@basic.measure
def RecordTableBuild():
    record_info = static.file_loc_dict['concat']
    record_colmap = static.colmap_concat
    record_loc = InIReaWri.ConfigR(type=record_info['category'],
                                   name=record_info['name'],
                                   conf=None)

    dynamic.record_df = FormProcess.FormPreProcess(
        df_loc=record_loc,
        col_map=record_colmap,
        drop_jud=record_info['dropcol'],
        sort_jud=record_info['sortcol'])

    FormProcess.TimeShift(df=dynamic.record_df,
                          column_names=static.timecol_name)


@basic.measure
def DependTableBuild():
    depend_info = static.file_loc_dict['baguan']
    depend_colmap = static.colmap_baguan
    depend_loc = InIReaWri.ConfigR(type=depend_info['category'],
                                   name=depend_info['name'],
                                   conf=None)

    dynamic.depend_df = FormProcess.FormPreProcess(
        df_loc=depend_loc,
        col_map=depend_colmap,
        sort_jud=depend_info['sortcol'])

    FormProcess.TimeShift(dynamic.depend_df, static.timecol_name)


@basic.measure
def ParaTableBuild():
    para_info = static.file_loc_dict['para']
    para_colmap = static.colmap_para
    para_loc = InIReaWri.ConfigR(type=para_info['category'],
                                 name=para_info['name'],
                                 conf=None)

    dynamic.para_df = FormProcess.FormPreProcess(df_loc=para_loc,
                                                 col_map=para_colmap,
                                                 sort_jud=para_info['sortcol'])

    FormProcess.TimeShift(dynamic.para_df, static.timecol_name)


@basic.measure
def TableExpansion():
    func_expand = func.TableCobine(dynamic.para_df, dynamic.depend_df)
    func_expand.Conbine()


@basic.measure
def TableFilt():
    result_namelist = static.filt_result
    dynamic.result_dict = basic.FromkeysReid(result_namelist)
    func_filt = func.TableFilt(dynamic.record_df, dynamic.depend_df,
                               dynamic.result_dict)
    func_filt.Filt()


@basic.measure
def TableSave():
    save_loc = dynamic.save_loc
    table_name = static.save_table_name
    func_build = func.TableBuild(dynamic.record_df, dynamic.depend_df,
                                 dynamic.result_dict)

    func_build.PidmissBuild()
    df = func_build.df
    FormProcess.PrintTableInfor(df, 'PID')
    FormProcess.CsvToLocal(df, save_loc, table_name['table filt ex1'])
    del df

    func_build.TimemissBuild()
    df = func_build.df
    FormProcess.PrintTableInfor(df, 'PID')
    FormProcess.CsvToLocal(df, save_loc, table_name['table filt ex2'])
    del df

    func_build.FiltedDataBuild()
    df = func_build.df
    FormProcess.PrintTableInfor(df, 'PID')
    FormProcess.CsvToLocal(df, save_loc, table_name['table filt in'])
    dynamic.filt_df = df
    del df


@basic.measure
def TableProcess():
    save_loc = dynamic.save_loc
    table_name = static.save_table_name
    func_process = func.TableProcess(dynamic.filt_df, static.col_name)

    func_process.ValidProcess()  # Save to config.ini
    df = func_process.df
    FormProcess.PrintTableInfor(df, 'PID')
    FormProcess.CsvToLocal(df, save_loc, table_name['table valid'])

    func_process.inValidProcess()
    df = func_process.df
    FormProcess.CsvToLocal(df, save_loc, table_name['table invalid'])
