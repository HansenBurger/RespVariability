import sys, pathlib, datetime

import class_func as func
import class_data as data

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess, PointProcess
from Code.Fundal import basic, BinImport, ReadSamplerate

static = data.DataStatic()
dynamic = data.DataDynamic()


def SaveLocGenerate():

    form_info = static.file_loc_dict['save form']
    graph_info = static.file_loc_dict['save graph']

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

    dynamic.df = FormProcess.FormPreProcess(df_loc=table_loc)
    dynamic.df_new = func.pd.DataFrame()
    FormProcess.TimeShift(dynamic.df, static.time_col_name)


@basic.measure
def TestTableBuild():

    table_loc = 'test.csv'
    dynamic.df = FormProcess.FormPreProcess(df_loc=table_loc)
    dynamic.df_new = func.DataFrame()
    FormProcess.TimeShift(dynamic.df, static.time_col_name)


@basic.measure
def GenerateObjList(table_len=None):

    colname = static.table_col_map

    for i in dynamic.df.index[:table_len]:

        obj = data.DomainTable()

        obj.pid = dynamic.df.loc[i, colname['patient ID']].item()
        obj.time = dynamic.df.loc[i, colname['record time']]
        obj.rid = dynamic.df.loc[i, colname['record ID']]
        obj.zdt = dynamic.df.loc[i, colname['zdt name']]
        obj.zpx = dynamic.df.loc[i, colname['zpx name']]
        obj.end = dynamic.df.loc[i, colname['exTube end']]
        obj.end = 1 if '成功' in obj.end else 0

        dynamic.objlist_table.append(obj)


@basic.measure
def GenerateFileLoc():

    data_info = static.file_loc_dict['data folder']
    data_loc = InIReaWri.ConfigR(type=data_info['category'],
                                 name=data_info['name'],
                                 conf=None)

    for obj_1 in dynamic.objlist_table:

        obj_2 = data.DomainRecord()

        process = func.FileLocBuild(data_loc, obj_1, obj_2)
        process.ZifLoc()
        process.ZdtLoc()
        process.ZpxLoc()

        dynamic.objlist_record.append(obj_2)


@basic.measure
def GetBinOutput():

    objlist_1 = dynamic.objlist_record
    objlist_2 = dynamic.objlist_table
    para = static.output_name_map

    for i in range(len(objlist_1)):

        start_time = datetime.datetime.now()
        try:
            process = func.OutputCheck(objlist_1[i])
        except:
            break

        zif_output = process.ZifContentCheck(BinImport.ImportZif)
        zdt_output = process.ZdtHeaderCheck(BinImport.ImportWaveHeader)
        wave_output = process.ZdtContentCheck(PointProcess.PointProcessing)

        objlist_1[i].machine = zif_output[para['machine name']].split('-')[0]
        del zif_output

        objlist_1[i].sample_rate = zdt_output[para['sample rate']].item(
        ) if zdt_output else ReadSamplerate.ReadSamplerate(
            str_machine_type=objlist_1[i].machine)
        del zdt_output

        objlist_1[i].p_list = wave_output[para['sampling sites']]
        objlist_1[i].s_F = wave_output[para['flowrate']]
        objlist_1[i].s_P = wave_output[para['pressure']]
        objlist_1[i].s_V = wave_output[para['volume']]
        del wave_output

        p_length = len(objlist_1[i].p_list)

        if p_length < 10:
            print('{0}: {1} lack waveform info'.format(i, objlist_2[i].pid))
            objlist_1[i] = None
            objlist_2[i] = None
            continue
        else:
            objlist_1[i].p_start = objlist_1[i].p_list[:p_length - 1]
            objlist_1[i].p_end = [x - 1 for x in objlist_1[i].p_list[1:]]

        end_time = datetime.datetime.now()
        print('{0}: process the {1}\'s data consume {2}'.format(
            i, objlist_2[i].pid, (end_time - start_time)))

    dynamic.objlist_record = [i for i in objlist_1 if i]
    dynamic.objlist_table = [i for i in objlist_2 if i]


@basic.measure
def Calculate():

    objlist_1 = dynamic.objlist_record
    objlist_2 = dynamic.objlist_table

    for i in range(len(objlist_1)):  # For each record

        record = objlist_1[i]
        pid = objlist_2[i].pid
        p_range = len(record.p_start)

        for j in range(p_range):  # For each resp

            resp = data.DomainResp()
            counter = func.Calculation(record.p_start[j], record.p_end[j])
            counter.ValidityCheck(record.s_F, record.s_V, record.s_P)

            if not counter.valid_tag:
                continue

            else:
                resp.RR = counter.RR(record.sample_rate)
                resp.V_T_i = counter.V_t_i()
                resp.V_T_e = counter.V_t_e()
                resp.wob = counter.WOB()
                resp.VE = counter.VE(resp.RR, resp.V_T_i)
                resp.rsbi = counter.RSBI(resp.RR, resp.V_T_i)

            record.objlist_resp.append(resp)

        print('RespInfo of {0}\'s record: total | {1}, valid | {2}'.format(
            pid,
            str(p_range).rjust(4, '0'),
            str(len(record.objlist_resp)).rjust(4, '0')))

        if len(record.objlist_resp) == 0:
            objlist_1[i] = None
            objlist_2[i] = None

    dynamic.objlist_record = [i for i in objlist_1 if i]
    dynamic.objlist_table = [i for i in objlist_2 if i]


@basic.measure
def MethodAverage():

    objlist = dynamic.objlist_record

    for record in objlist:

        record.obj_average = data.DomainAverage()
        method = func.Analysis().Mean
        obj_result = record.obj_average
        resp_list = record.objlist_resp

        obj_result.RR = method([x.RR for x in resp_list])
        obj_result.V_T = method([x.V_T_i for x in resp_list])
        obj_result.VE = method([x.VE for x in resp_list])
        obj_result.wob = method([x.wob for x in resp_list])
        obj_result.rsbi = method([x.rsbi for x in resp_list])


@basic.measure
def MethodStanDev():

    objlist = dynamic.objlist_record

    for record in objlist:

        record.obj_standev = data.DomainStanDev()
        method = func.Analysis().StanDev
        obj_result = record.obj_standev
        resp_list = record.objlist_resp

        obj_result.RR = method([x.RR for x in resp_list])
        obj_result.V_T = method([x.V_T_i for x in resp_list])
        obj_result.VE = method([x.VE for x in resp_list])
        obj_result.wob = method([x.wob for x in resp_list])
        obj_result.rsbi = method([x.rsbi for x in resp_list])


@basic.measure
def ResultAggregate():

    objlist_1 = dynamic.objlist_record
    objlist_2 = dynamic.objlist_table

    for i in range(len(objlist_1)):

        obj = data.DomainAggregate()

        obj.pid = objlist_2[i].pid
        obj.end = objlist_2[i].end
        obj.RR_1 = objlist_1[i].obj_average.RR
        obj.V_T_1 = objlist_1[i].obj_average.V_T
        obj.VE_1 = objlist_1[i].obj_average.VE
        obj.wob_1 = objlist_1[i].obj_average.wob
        obj.rsbi_1 = objlist_1[i].obj_average.rsbi
        obj.RR_2 = objlist_1[i].obj_standev.RR
        obj.V_T_2 = objlist_1[i].obj_standev.V_T
        obj.VE_2 = objlist_1[i].obj_standev.VE
        obj.wob_2 = objlist_1[i].obj_standev.wob
        obj.rsbi_2 = objlist_1[i].obj_standev.rsbi

        dynamic.objlist_result.append(obj)


@basic.measure
def SaveTableBuild():

    colname = static.result_name_map
    df = dynamic.df_new
    df[colname['patient ID']] = [x.pid for x in dynamic.objlist_result]
    df[colname['exTube end']] = [x.end for x in dynamic.objlist_result]
    df[colname['Average RR']] = [x.RR_1 for x in dynamic.objlist_result]
    df[colname['Average V_T']] = [x.V_T_1 for x in dynamic.objlist_result]
    df[colname['Average VE']] = [x.VE_1 for x in dynamic.objlist_result]
    df[colname['Average WOB']] = [x.wob_1 for x in dynamic.objlist_result]
    df[colname['Average RSBI']] = [x.rsbi_1 for x in dynamic.objlist_result]
    df[colname['Standev RR']] = [x.RR_2 for x in dynamic.objlist_result]
    df[colname['Standev V_T']] = [x.V_T_2 for x in dynamic.objlist_result]
    df[colname['Standev VE']] = [x.VE_2 for x in dynamic.objlist_result]
    df[colname['Standev WOB']] = [x.wob_2 for x in dynamic.objlist_result]
    df[colname['Standev RSBI']] = [x.rsbi_2 for x in dynamic.objlist_result]

    FormProcess.CsvToLocal(df, dynamic.save_form_loc,
                           static.save_table_name['table result'])


@basic.measure
def SaveGraphs():

    colname = static.result_name_map

    draf = func.Draft(dynamic.save_graph_loc, dynamic.df_new)
    draf.BoxPlot(colname['exTube end'], colname['Average RR'], 'rr_average')
    draf.BoxPlot(colname['exTube end'], colname['Average V_T'], 'vt_average')
    draf.BoxPlot(colname['exTube end'], colname['Average VE'], 've_average')
    draf.BoxPlot(colname['exTube end'], colname['Average WOB'], 'wob_average')
    draf.BoxPlot(colname['exTube end'], colname['Average RSBI'],
                 'rsbi_average')

    draf.BoxPlot(colname['exTube end'], colname['Standev RR'], 'rr_standev')
    draf.BoxPlot(colname['exTube end'], colname['Standev V_T'], 'vt_standev')
    draf.BoxPlot(colname['exTube end'], colname['Standev VE'], 've_standev')
    draf.BoxPlot(colname['exTube end'], colname['Standev WOB'], 'wob_standev')
    draf.BoxPlot(colname['exTube end'], colname['Standev RSBI'],
                 'rsbi_standev')
