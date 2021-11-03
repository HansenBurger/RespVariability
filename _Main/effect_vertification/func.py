import sys, pathlib, datetime
from time import process_time

import class_func as func
import class_data as data
import class_domain_0 as domain0
import class_domain_1 as domain1

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess, PointProcess
from Code.Fundal import basic, BinImport, ReadSamplerate

static = data.DataStatic()
dynamic = data.DataDynamic()


def SaveLocGenerate(module_name):

    form_info = static.file_loc_dict['save form']
    graph_info = static.file_loc_dict['save graph']
    now = datetime.datetime.now()
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
    dynamic.save_form_loc = str(save_form_loc)

    save_graph_loc = InIReaWri.ConfigR(type=graph_info['category'],
                                       name=graph_info['name'],
                                       conf=None)
    save_graph_loc = pathlib.Path(save_graph_loc) / folder_name
    save_graph_loc.mkdir(parents=True, exist_ok=True)
    dynamic.save_graph_loc = str(save_graph_loc)


@basic.measure
def MainTableBuild():

    table_info = static.file_loc_dict['main table']
    table_loc = InIReaWri.ConfigR(type=table_info['category'],
                                  name=table_info['name'],
                                  conf=None)

    dynamic.df = FormProcess.FormPreProcess(df_loc=table_loc)
    dynamic.df_new = FormProcess.FormPreProcess()
    FormProcess.TimeShift(dynamic.df, static.time_col_name)


@basic.measure
def TestTableBuild():

    table_loc = 'test.csv'
    dynamic.df = FormProcess.FormPreProcess(df_loc=table_loc)
    dynamic.df_new = FormProcess.FormPreProcess()
    FormProcess.TimeShift(dynamic.df, static.time_col_name)


@basic.measure
def GenerateObjList(table_len=None):

    colname = static.table_col_map

    for i in dynamic.df.index[:table_len]:

        obj = domain0.DomainTable()

        obj.pid = dynamic.df.loc[i, colname['patient ID']].item()
        obj.time = dynamic.df.loc[i, colname['record time']]
        obj.rid = dynamic.df.loc[i, colname['record ID']]
        obj.zdt = dynamic.df.loc[i, colname['zdt name']]
        obj.zpx = dynamic.df.loc[i, colname['zpx name']]
        obj.end = dynamic.df.loc[i, colname['exTube end']]
        obj.end = 0 if '成功' in obj.end else 1

        dynamic.objlist_table.append(obj)


@basic.measure
def GenerateFileLoc():

    data_info = static.file_loc_dict['data folder']
    data_loc = InIReaWri.ConfigR(type=data_info['category'],
                                 name=data_info['name'],
                                 conf=None)

    for obj_1 in dynamic.objlist_table:

        obj_2 = domain0.DomainRecord()

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

            resp = domain1.DomainResp()
            counter = func.Calculation(record.p_start[j], record.p_end[j])
            counter.ValidityCheck(record.s_F, record.s_V, record.s_P)

            if not counter.valid_tag:
                continue

            else:
                resp.RR = counter.RR(record.sample_rate)
                resp.V_T_i = counter.V_t_i()
                resp.V_T_e = counter.V_t_e()
                resp.VE = counter.VE(resp.RR, resp.V_T_i)
                resp.rsbi = counter.RSBI(resp.RR, resp.V_T_i)

                wob_output = counter.WOB()
                resp.wob = wob_output[0]
                resp.wob_a = wob_output[1]
                resp.wob_b = wob_output[2]

                mp_output = counter.MP_Area(resp.RR, resp.V_T_i, resp.wob_a)
                resp.mp_jm = mp_output[0]
                resp.mp_jl = mp_output[1]

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
def RespValidity():

    objlist = dynamic.objlist_record

    for obj in objlist:

        resplist = obj.objlist_resp

        for j in range(len(resplist)):

            resp = resplist[j]
            process = func.ParaValidity(resp)
            process.ValTotal()
            if not process.validity:
                resp = None

        obj.objlist_resp = [i for i in resplist if i]
        a = obj.objlist_resp
        pass


@basic.measure
def ScatterPlotPer():

    objlist_1 = dynamic.objlist_record
    objlist_2 = dynamic.objlist_table
    loc = dynamic.save_graph_loc

    for i in range(len(objlist_1)):

        resp_list = objlist_1[i].objlist_resp
        pid = str(objlist_2[i].pid)
        end = str(objlist_2[i].end)

        df = FormProcess.FormPreProcess()
        RR = [x.RR for x in resp_list]
        df['RR_0'] = RR[:len(RR) - 1]
        df['RR_1'] = RR[1:]
        VT = [x.V_T_i for x in resp_list]
        df['VT_0'] = VT[:len(VT) - 1]
        df['VT_1'] = VT[1:]
        VE = [x.VE for x in resp_list]
        df['VE_0'] = VE[:len(VE) - 1]
        df['VE_1'] = VE[1:]
        wob = [x.wob for x in resp_list]
        df['WOB_0'] = wob[:len(wob) - 1]
        df['WOB_1'] = wob[1:]
        rsbi = [x.rsbi for x in resp_list]
        df['RSBI_0'] = rsbi[:len(rsbi) - 1]
        df['RSBI_1'] = rsbi[1:]

        draft_p = func.Draft(loc, df)

        draft_p.ScatterPlot('RR_0', 'RR_1', 'RR', pid, end)
        draft_p.ScatterPlot('VT_0', 'VT_1', 'VT', pid, end)
        draft_p.ScatterPlot('VE_0', 'VE_1', 'VE', pid, end)
        draft_p.ScatterPlot('WOB_0', 'WOB_1', 'WOB', pid, end)
        draft_p.ScatterPlot('RSBI_0', 'RSBI_1', 'RSBI', pid, end)


@basic.measure
def WaveformPlotting():
    #TODO
    # each record generate the waveform
    # static value: fig(width, height),
    pass


@basic.measure
def MethodAverage():

    objlist = dynamic.objlist_record

    for record in objlist:

        record.obj_average = domain1.DomainAverage()
        method = func.Analysis().Mean
        obj_result = record.obj_average
        resp_list = record.objlist_resp

        obj_result.RR = method([x.RR for x in resp_list])
        obj_result.V_T = method([x.V_T_i for x in resp_list])
        obj_result.VE = method([x.VE for x in resp_list])
        obj_result.wob = method([x.wob for x in resp_list])
        obj_result.rsbi = method([x.rsbi for x in resp_list])
        obj_result.mp_jm = method([x.mp_jm for x in resp_list])
        obj_result.mp_jl = method([x.mp_jl for x in resp_list])


@basic.measure
def MethodStanDev():

    objlist = dynamic.objlist_record

    for record in objlist:

        record.obj_standev = domain1.DomainStanDev()
        method = func.Analysis().StanDev
        obj_result = record.obj_standev
        resp_list = record.objlist_resp

        obj_result.RR = method([x.RR for x in resp_list])
        obj_result.V_T = method([x.V_T_i for x in resp_list])
        obj_result.VE = method([x.VE for x in resp_list])
        obj_result.wob = method([x.wob for x in resp_list])
        obj_result.rsbi = method([x.rsbi for x in resp_list])
        obj_result.mp_jm = method([x.mp_jm for x in resp_list])
        obj_result.mp_jl = method([x.mp_jl for x in resp_list])


@basic.measure
def MethodHRA():

    objlist = dynamic.objlist_record

    for record in objlist:

        record.obj_hra = domain1.DomainHRA()
        method = func.Analysis().HRA
        obj_result = record.obj_hra
        resp_list = record.objlist_resp

        obj_result.RR_s = method([x.RR for x in resp_list])
        obj_result.V_T_s = method([x.V_T_i for x in resp_list])
        obj_result.VE_s = method([x.VE for x in resp_list])
        obj_result.wob_s = method([x.wob for x in resp_list])
        obj_result.rsbi_s = method([x.rsbi for x in resp_list])


@basic.measure
def LinearAggregate():

    objlist_1 = dynamic.objlist_record
    objlist_2 = dynamic.objlist_table

    for i in range(len(objlist_1)):

        obj = domain0.DomainAggregate()

        obj.pid = objlist_2[i].pid
        obj.end = objlist_2[i].end
        obj.resp = objlist_1[i].objlist_resp
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
        obj.mp_jm_1 = objlist_1[i].obj_average.mp_jm
        obj.mp_jl_1 = objlist_1[i].obj_average.mp_jl
        obj.mp_jm_2 = objlist_1[i].obj_standev.mp_jm
        obj.mp_jl_2 = objlist_1[i].obj_standev.mp_jl

        dynamic.linear_results.append(obj)


@basic.measure
def NonlinearAggregate():

    objlist_1 = dynamic.objlist_record
    objlist_2 = dynamic.objlist_table

    for i in range(len(objlist_1)):

        obj = domain0.DomainAggregate()

        obj.pid = objlist_2[i].pid
        obj.end = objlist_2[i].end
        obj.RR_3 = objlist_1[i].obj_hra.RR_s
        obj.V_T_3 = objlist_1[i].obj_hra.V_T_s
        obj.VE_3 = objlist_1[i].obj_hra.VE_s
        obj.wob_3 = objlist_1[i].obj_hra.wob_s
        obj.rsbi_3 = objlist_1[i].obj_hra.rsbi_s

        dynamic.nonlinear_results.append(obj)


@basic.measure
def LinearTableBuild():

    colname = static.result_name_map
    df = dynamic.df_new if dynamic.df_new.empty else FormProcess.FormPreProcess(
    )

    df[colname['patient ID']] = [x.pid for x in dynamic.linear_results]
    df[colname['exTube end']] = [x.end for x in dynamic.linear_results]

    df[colname['Average RR']] = [x.RR_1 for x in dynamic.linear_results]
    df[colname['Average V_T']] = [x.V_T_1 for x in dynamic.linear_results]
    df[colname['Average VE']] = [x.VE_1 for x in dynamic.linear_results]
    df[colname['Average WOB']] = [x.wob_1 for x in dynamic.linear_results]
    df[colname['Average RSBI']] = [x.rsbi_1 for x in dynamic.linear_results]
    df[colname['Average MP(Jm)']] = [x.mp_jm_1 for x in dynamic.linear_results]
    df[colname['Average MP(JL)']] = [x.mp_jl_1 for x in dynamic.linear_results]

    df[colname['Standev RR']] = [x.RR_2 for x in dynamic.linear_results]
    df[colname['Standev V_T']] = [x.V_T_2 for x in dynamic.linear_results]
    df[colname['Standev VE']] = [x.VE_2 for x in dynamic.linear_results]
    df[colname['Standev WOB']] = [x.wob_2 for x in dynamic.linear_results]
    df[colname['Standev RSBI']] = [x.rsbi_2 for x in dynamic.linear_results]
    df[colname['Standev MP(Jm)']] = [x.mp_jm_2 for x in dynamic.linear_results]
    df[colname['Standev MP(JL)']] = [x.mp_jl_2 for x in dynamic.linear_results]

    filt_a = (df[colname['Average RR']] < 80) & (df[colname['Average RSBI']] <
                                                 400)
    filt_b = df[colname['Standev WOB']] < 40
    dynamic.df_new = df.loc[filt_a & filt_b]

    FormProcess.CsvToLocal(dynamic.df_new, dynamic.save_form_loc,
                           static.save_table_name['result: linear sumP10'])


@basic.measure
def NonlinearTableBuild():

    colname = static.result_name_map
    df = dynamic.df_new if dynamic.df_new.empty else FormProcess.FormPreProcess(
    )

    df[colname['patient ID']] = [x.pid for x in dynamic.nonlinear_results]
    df[colname['exTube end']] = [x.end for x in dynamic.nonlinear_results]

    df[colname['HRA RR'][0]] = [
        x.RR_3['PI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA RR'][1]] = [
        x.RR_3['GI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA RR'][2]] = [
        x.RR_3['SI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA V_T'][0]] = [
        x.V_T_3['PI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA V_T'][1]] = [
        x.V_T_3['GI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA V_T'][2]] = [
        x.V_T_3['SI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA VE'][0]] = [
        x.VE_3['PI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA VE'][1]] = [
        x.VE_3['GI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA VE'][2]] = [
        x.VE_3['SI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA WOB'][0]] = [
        x.wob_3['PI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA WOB'][1]] = [
        x.wob_3['GI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA WOB'][2]] = [
        x.wob_3['SI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA RSBI'][0]] = [
        x.rsbi_3['PI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA RSBI'][1]] = [
        x.rsbi_3['GI'] for x in dynamic.nonlinear_results
    ]
    df[colname['HRA RSBI'][2]] = [
        x.rsbi_3['SI'] for x in dynamic.nonlinear_results
    ]

    dynamic.df_new = df

    FormProcess.CsvToLocal(dynamic.df_new, dynamic.save_form_loc,
                           static.save_table_name['result nonlinear'])


@basic.measure
def LinearGraph():

    colname = static.result_name_map
    loc = pathlib.Path(dynamic.save_graph_loc) / 'Linear'
    loc.mkdir(parents=True, exist_ok=True)
    df = dynamic.df_new

    draf = func.Draft(str(loc), df).BoxPlot

    targets_list = ['RR', 'V_T', 'VE', 'WOB', 'RSBI', 'MP(Jm)', 'MP(JL)']
    targets_len = len(targets_list)
    extube_colname_list = ['exTube end'] * targets_len
    average_colname_list = [('Average ' + x) for x in targets_list]
    standev_colname_list = [('Standev ' + x) for x in targets_list]
    average_savename_list = [(x + '_average') for x in targets_list]
    standev_savename_list = [(x + '_standev') for x in targets_list]

    for i in range(targets_len):

        draf(x_label=colname[extube_colname_list[i]],
             y_label=colname[average_colname_list[i]],
             fig_name=average_savename_list[i])

        draf(x_label=colname[extube_colname_list[i]],
             y_label=colname[standev_colname_list[i]],
             fig_name=standev_savename_list[i])


@basic.measure
def NonlinearGraph():

    colname = static.result_name_map
    loc = dynamic.save_graph_loc
    df = dynamic.df_new

    draf = func.Draft(loc, df).BoxPlotMulti

    targets_list = ['RR', 'V_T', 'VE', 'WOB', 'RSBI']
    targets_len = len(targets_list)
    extube_colname_list = ['exTube end'] * targets_len
    hra_colname_list = [('HRA ' + x) for x in targets_list]
    hra_savename_list = [(x + '_HRA') for x in targets_list]

    filt_list = [
        (df[colname['HRA RR'][1]] > 48) &
        (df[colname['HRA RR'][1]] < 52) & (df[colname['HRA RR'][2]] < 0.5),
        (df[colname['HRA V_T'][1]] < 55) & (df[colname['HRA V_T'][2]] < 50000)
        & (df[colname['HRA V_T'][2]] > -50000),
        (df[colname['HRA VE'][1]] < 52.5) &
        (df[colname['HRA VE'][2]] < 100000),
        (df[colname['HRA WOB'][1]] < 52) & (df[colname['HRA WOB'][2]] < 100000)
        & (df[colname['HRA WOB'][2]] > -100000),
        (df[colname['HRA RSBI'][1]] < 55) &
        (df[colname['HRA RSBI'][2]] > -50000)
    ]

    for i in range(targets_len):

        draf(x_label=colname[extube_colname_list[i]],
             y_labels=colname[hra_colname_list[i]],
             fig_name=hra_savename_list[i],
             filt=filt_list[i])
