import sys, pathlib
import table_class_data as data
import table_class_filt as func

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess
from Code.Fundal import basic

static = data.DataStatic()
dynamic = data.DataDynamic()  # life cycle ?


def SaveLocGenerate():
    save_info = static.file_loc_dict['save_form']
    dynamic.save_loc = InIReaWri.ConfigR(type=save_info['category'],
                                         name=save_info['name'],
                                         conf=None)


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

    FormProcess.TimeShift(df=dynamic.depend_df,
                          column_names=static.timecol_name)


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

    FormProcess.TimeShift(df=dynamic.para_df, column_names=static.timecol_name)


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
    func_build = func.TableBuild(dynamic.record_df, dynamic.depend_df,
                                 dynamic.result_dict)

    func_build.PidmissBuild()
    FormProcess.PrintTableInfor(func_build.df, 'PID')
    FormProcess.CsvToLocal(func_build.df, dynamic.save_loc,
                           static.save_table_name['table filt ex1'])

    func_build.TimemissBuild()
    FormProcess.PrintTableInfor(func_build.df, 'PID')
    FormProcess.CsvToLocal(func_build.df, dynamic.save_loc,
                           static.save_table_name['table filt ex2'])

    func_build.FiltedDataBuild()
    dynamic.filt_df = func_build.df
    FormProcess.PrintTableInfor(func_build.df, 'PID')
    FormProcess.CsvToLocal(func_build.df, dynamic.save_loc,
                           static.save_table_name['table filt in'])


@basic.measure
def TableProcess():
    func_process = func.TableProcess(dynamic.filt_df, static.col_name)

    func_process.ValidProcess()
    FormProcess.PrintTableInfor(func_process.df, 'PID')
    FormProcess.CsvToLocal(func_process.df, dynamic.save_loc,
                           static.save_table_name['table valid'])

    func_process.inValidProcess()
    FormProcess.CsvToLocal(func_process.df, dynamic.save_loc,
                           static.save_table_name['table invalid'])
