import sys, pathlib
import record_class_func as func
import record_class_data as data
from datetime import datetime

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess, PointProcess
from Code.Fundal import basic, BinImport, ReadSamplerate

static = data.DataStatic()
dynamic = data.DataDynamic()


def SaveLocGenerate(module_name):
    now = datetime.now()
    folder_name = '{0}{1}{2}_{3}_{4}'.format(now.year,
                                             str(now.month).rjust(2, '0'),
                                             str(now.day).rjust(2, '0'),
                                             str(now.hour).rjust(2, '0'),
                                             module_name)
    save_info = static.file_loc_dict['save_form']
    save_form_loc = InIReaWri.ConfigR(type=save_info['category'],
                                      name=save_info['name'],
                                      conf=None)
    save_form_loc = pathlib.Path(save_form_loc) / folder_name
    save_form_loc.mkdir(parents=True, exist_ok=True)
    dynamic.save_loc = str(save_form_loc)


@basic.measure
def MainTableBuild():

    table_info = static.file_loc_dict['main table']
    table_loc = InIReaWri.ConfigR(type=table_info['category'],
                                  name=table_info['name'],
                                  conf=None)

    dynamic.df = FormProcess.FormPreProcess(df_loc=table_loc)

    FormProcess.TimeShift(df=dynamic.df, column_names=static.time_col)


def TestTableBuild():

    table_loc = r'C:\Users\HY_Burger\Desktop\Project\RespVariability\test.csv'
    dynamic.df = FormProcess.FormPreProcess(df_loc=table_loc)
    FormProcess.TimeShift(df=dynamic.df, column_names=static.time_col)


@basic.measure
def GenerateObjList():

    colname = static.table_col_map

    for i in dynamic.df.index:
        obj = data.DomainTable()
        obj.row = i
        obj.time = dynamic.df.loc[i, colname['record time']]
        obj.rid = dynamic.df.loc[i, colname['record ID']]
        obj.zdt = dynamic.df.loc[i, colname['zdt name']]
        obj.zpx = dynamic.df.loc[i, colname['zpx name']]
        dynamic.objlist_table.append(obj)


@basic.measure
def GenerateFileLoc():

    data_info = static.file_loc_dict['data folder']
    data_loc = InIReaWri.ConfigR(type=data_info['category'],
                                 name=data_info['name'],
                                 conf=None)
    for obj_table in dynamic.objlist_table:
        obj_record = data.DomainRecord()
        process = func.FileLocBuild(data_loc, obj_table, obj_record)
        process.ZifLoc()
        process.ZdtLoc()
        process.ZpxLoc()

        dynamic.objlist_record.append(obj_record)


@basic.measure
def GetBinOutput():

    objlist_0 = dynamic.objlist_table
    objlist_1 = dynamic.objlist_record
    para = static.output_name_map

    for i in range(len(objlist_0)):
        start_time = datetime.now()

        ob0 = objlist_0[i]
        ob1 = objlist_1[i]

        process = func.OutputCheck(ob1)
        zif_output = process.ZifContentCheck(BinImport.ImportZif)
        zdt_output = process.ZdtHeaderCheck(BinImport.ImportWaveHeader)
        zpx_output = process.ZpxParaCheck(BinImport.ImportPara)
        wave_output = process.ZdtPointCheck(PointProcess.PointProcessing)

        ob1.machine = zif_output[para['machine name']] if zif_output else None
        # resive the machine num

        ob1.sample_rate = zdt_output[para['sample rate']].item(
        ) if zdt_output else ReadSamplerate.ReadSamplerate(
            str_machine_type=ob1.machine)

        ob1.start_ind = wave_output[para['start index']]

        ob1.s_F = wave_output[para['flow index']]

        ob1.para_ind = zpx_output[para['para index']] if zpx_output else []

        ob1.st_peep = zpx_output[para['PEEP setting']] if zpx_output else []

        ob1.st_ps = zpx_output[para['PS setting']] if zpx_output else []

        ob1.st_e_sens = zpx_output[para['ESENS setting']] if zpx_output else []

        ob1.vent_type = zpx_output[para['vent type']] if zpx_output else []

        ob1.vent_mode = zpx_output[para['vent mode']] if zpx_output else []

        ob1.mand_type = zpx_output[para['mand type']] if zpx_output else []

        end_time = datetime.now()

        print('process the {0} row consume {1} s'.format(
            str(ob0.row).rjust(4, '0'), (end_time - start_time).seconds))


@basic.measure
def ResultGenerate():

    for obj_record in dynamic.objlist_record:
        obj_result = data.DomainResult()
        process = func.Calculation(obj_record, obj_result)

        process.FlowtimeBuild()
        process.VMlistBuild(ReadSamplerate.ReadVentMode)
        obj_result.peep_list = process.SetsBuild(obj_record.st_peep)
        obj_result.ps_list = process.SetsBuild(obj_record.st_ps)
        obj_result.e_sens_list = process.SetsBuild(obj_record.st_e_sens)
        obj_result.sumP_list = process.SetSum(obj_result.peep_list,
                                              obj_result.ps_list)

        dynamic.objlist_result.append(obj_result)


@basic.measure
def TableBuild():

    colname = static.result_name_map
    objlist_0 = dynamic.objlist_record
    objlist_1 = dynamic.objlist_result
    save_form_loc = static.save_table_name['result full']
    df = dynamic.df

    df[colname['machine type']] = [obj.machine for obj in objlist_0]
    df[colname['vent m bin']] = [obj.v_m_list[0] for obj in objlist_1]
    df[colname['vent m mid']] = [obj.v_m_list[1] for obj in objlist_1]
    df[colname['vent m end']] = [obj.v_m_list[2] for obj in objlist_1]
    df[colname['still time']] = [obj.still_time for obj in objlist_1]
    df[colname['peep setting']] = [
        '/'.join(str(x) for x in obj.peep_list) for obj in objlist_1
    ]
    df[colname['ps setting']] = [
        '/'.join(str(x) for x in obj.ps_list) for obj in objlist_1
    ]
    df[colname['esens setting']] = [
        '/'.join(str(x) for x in obj.e_sens_list) for obj in objlist_1
    ]
    df[colname['peep + ps']] = [
        '/'.join(str(x) for x in obj.sumP_list) for obj in objlist_1
    ]

    FormProcess.CsvToLocal(df, dynamic.save_loc, save_form_loc)


@basic.measure
def TableProcess():

    colname = static.result_name_map
    save_form_loc = static.save_table_name['result shrink']
    df = dynamic.df.copy()

    filt_machine_840_0 = df[colname['machine type']].str.contains('840-4')
    filt_machine_840_1 = df[colname['machine type']].str.contains('840-22')
    filt_ICU4 = df[colname['ICU']] == 'ICU4F'

    df = df[~filt_machine_840_0 & ~filt_machine_840_1 & ~filt_ICU4]

    FormProcess.CsvToLocal(df, dynamic.save_loc, save_form_loc)
