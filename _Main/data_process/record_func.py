import sys, pathlib, datetime
import record_class_func as func
import record_class_data as data

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess, PointProcess
from Code.Fundal import basic, BinImport, ReadSamplerate

static = data.DataStatic()
dynamic = data.DataDynamic()


def SaveLocGenerate():

    save_info = static.file_loc_dict['save_form']
    dynamic.save_loc = InIReaWri.ConfigR(type=save_info['category'],
                                         name=save_info['name'],
                                         conf=None)


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
        record_obj = data.RecordObj()
        record_obj.row = i
        record_obj.time = dynamic.df.loc[i, colname['record time']]
        record_obj.rid = dynamic.df.loc[i, colname['record ID']]
        record_obj.zdt = dynamic.df.loc[i, colname['zdt name']]
        record_obj.zpx = dynamic.df.loc[i, colname['zpx name']]
        dynamic.obj_list.append(record_obj)


@basic.measure
def GenerateFileLoc():

    data_info = static.file_loc_dict['data folder']
    data_loc = InIReaWri.ConfigR(type=data_info['category'],
                                 name=data_info['name'],
                                 conf=None)
    for i in dynamic.obj_list:
        process = func.FileLocBuild(data_loc, i)
        process.ZifLoc()
        process.ZdtLoc()
        process.ZpxLoc()


@basic.measure
def GetBinOutput():

    for i in dynamic.obj_list:

        para = static.output_name_map

        start_time = datetime.datetime.now()

        process_0 = func.OutputCheck(i)
        process_1 = func.Calculation(i)

        zif_output = process_0.ZifContentCheck(BinImport.ImportZif)
        zdt_output = process_0.ZdtHeaderCheck(BinImport.ImportWaveHeader)
        zpx_output = process_0.ZpxParaCheck(BinImport.ImportPara)
        wave_output = process_0.ZdtPointCheck(PointProcess.PointProcessing)

        i.machine = zif_output[para['machine name']].split(
            '-')[0] if zif_output else None

        i.sample_rate = zdt_output[para['sample rate']].item(
        ) if zdt_output else ReadSamplerate.ReadSamplerate(
            str_machine_type=i.machine)

        i.start_ind = wave_output[para['start index']]

        i.para_ind = zpx_output[para['para data index']] if zpx_output else []

        i.vent_type = zpx_output[para['vent type list']] if zpx_output else []

        i.vent_mode = zpx_output[para['vent mode list']] if zpx_output else []

        i.mand_type = zpx_output[para['mand type list']] if zpx_output else []

        process_1.VMtimeBuild()
        process_1.VMlistBuild(ReadSamplerate.ReadVentMode)

        end_time = datetime.datetime.now()
        print('process the ',
              str(i.row).rjust(4, '0'), ' row consume ',
              (end_time - start_time).seconds, ' s')


@basic.measure
def TableBuild():

    colname = static.result_name_map
    df = dynamic.df

    df[colname['machine type']] = [obj.machine for obj in dynamic.obj_list]
    df[colname['vent m bin']] = [obj.v_m_list[0] for obj in dynamic.obj_list]
    df[colname['vent m mid']] = [obj.v_m_list[1] for obj in dynamic.obj_list]
    df[colname['vent m end']] = [obj.v_m_list[2] for obj in dynamic.obj_list]
    df[colname['vent still time']] = [
        obj.still_time for obj in dynamic.obj_list
    ]

    FormProcess.CsvToLocal(df, dynamic.save_loc,
                           static.save_table_name['table result'])