import sys, pathlib, datetime, sqlite3
from tkinter import N
import pandas as pd

import class_func as func
import class_data as data
import class_domain_0 as domain0
import class_domain_1 as domain1
import class_domain_2 as domain2

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
def MainTableBuild_db(table_name):
    db = r'C:\Main\Data\_\Database\sqlite\RespdataWean_2203.db'
    query_state = '''
    SELECT * FROM {0}
    WHERE vent_t > 1800
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
    FormProcess.TimeShift(df, static.time_col_name)
    dynamic.df = df[:]
    dynamic.df_new = FormProcess.FormPreProcess()


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
                resp.ts = counter.RespT(record.sample_rate)
                resp.RR = counter.RR(record.sample_rate)
                resp.V_T_i = counter.V_t_i()
                resp.V_T_e = counter.V_t_e()
                resp.VE = counter.VE(resp.RR, resp.V_T_i)
                resp.rsbi = counter.RSBI(resp.RR, resp.V_T_i)

                wob_output = counter.WOB()
                resp.wob = wob_output[0]
                resp.wob_full = wob_output[1]
                resp.wob_a = wob_output[2]
                resp.wob_b = wob_output[3]

                mp_out_d = counter.MP_Area(resp.RR, resp.V_T_i, resp.wob)
                resp.mp_jm_d = mp_out_d[0]
                resp.mp_jl_d = mp_out_d[1]

                mp_out_ds = counter.MP_Area(resp.RR, resp.V_T_i, resp.wob_full)
                resp.mp_jm_t = mp_out_ds[0]
                resp.mp_jl_t = mp_out_ds[1]

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


@basic.measure
def TimeScreening(t_st):
    '''
    Objects:
    1. check the validity
    2. count total time width compare to t_ts
    3. exclue inclue by con
    '''
    objlist_1 = dynamic.objlist_record
    objlist_2 = dynamic.objlist_table

    t_st = t_st * 3600  # hour -> second

    for i in range(len(objlist_1)):

        ob1, ob2 = objlist_1[i], objlist_2[i]
        resp_l = ob1.objlist_resp.copy()
        resp_t_l = [x.ts for x in resp_l]

        if sum(resp_t_l) < t_st:
            ob1, ob2 = None, None
        else:
            resp_t_l.reverse()
            j = 1
            while sum(resp_t_l[0:j]) <= t_st:
                j += 1
            ob1.objlist_resp = resp_l[-1 - j:-1]

    dynamic.objlist_record = [i for i in objlist_1 if i]
    dynamic.objlist_table = [i for i in objlist_2 if i]


@basic.measure
def ScatterPlotPer():

    objlist_1 = dynamic.objlist_record
    objlist_2 = dynamic.objlist_table
    loc = dynamic.save_graph_loc
    save_loc = pathlib.Path(loc) / 'ScatterPlots'
    save_loc.mkdir(parents=True, exist_ok=True)

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
        mp_jl = [x.mp_jl_d for x in resp_list]
        df['MP(JL)_d_0'] = mp_jl[:len(mp_jl) - 1]
        df['MP(JL)_d_1'] = mp_jl[1:]
        mp_jm = [x.mp_jm_d for x in resp_list]
        df['MP(Jm)_d_0'] = mp_jm[:len(mp_jm) - 1]
        df['MP(Jm)_d_1'] = mp_jm[1:]
        mp_jl = [x.mp_jl_t for x in resp_list]
        df['MP(JL)_ds_0'] = mp_jl[:len(mp_jl) - 1]
        df['MP(JL)_ds_1'] = mp_jl[1:]
        mp_jm = [x.mp_jm_t for x in resp_list]
        df['MP(Jm)_ds_0'] = mp_jm[:len(mp_jm) - 1]
        df['MP(Jm)_ds_1'] = mp_jm[1:]

        draft_p = func.Draft(str(save_loc), df)

        draft_p.ScatterPlot('RR_0', 'RR_1', 'RR', pid, end)
        draft_p.ScatterPlot('VT_0', 'VT_1', 'VT', pid, end)
        draft_p.ScatterPlot('VE_0', 'VE_1', 'VE', pid, end)
        draft_p.ScatterPlot('WOB_0', 'WOB_1', 'WOB', pid, end)
        draft_p.ScatterPlot('RSBI_0', 'RSBI_1', 'RSBI', pid, end)
        draft_p.ScatterPlot('MP(JL)_d_0', 'MP(JL)_d_1', 'MP(JL)d', pid, end)
        draft_p.ScatterPlot('MP(Jm)_d_0', 'MP(Jm)_d_1', 'MP(Jm)d', pid, end)
        draft_p.ScatterPlot('MP(JL)_ds_0', 'MP(JL)_ds_1', 'MP(JL)ds', pid, end)
        draft_p.ScatterPlot('MP(Jm)_ds_0', 'MP(Jm)_ds_1', 'MP(Jm)ds', pid, end)


@basic.measure
def WaveformPlotting():
    #TODO
    # each record generate the waveform
    # static value: fig(width, height),
    pass


def __MethodBasic(method, result, resp_list, method_sub=None):
    result.RR = method([x.RR for x in resp_list], method_sub)
    result.V_T = method([x.V_T_i for x in resp_list], method_sub)
    result.VE = method([x.VE for x in resp_list], method_sub)
    result.wob = method([x.wob for x in resp_list], method_sub)
    result.rsbi = method([x.rsbi for x in resp_list], method_sub)
    result.mp_jm_d = method([x.mp_jm_d for x in resp_list], method_sub)
    result.mp_jl_d = method([x.mp_jl_d for x in resp_list], method_sub)
    result.mp_jm_t = method([x.mp_jm_t for x in resp_list], method_sub)
    result.mp_jl_t = method([x.mp_jl_t for x in resp_list], method_sub)


@basic.measure
def MethodTS():
    method = func.Analysis().TimeSeries
    objlist = dynamic.objlist_record

    for record in objlist:
        record.obj_ts = domain1.DomainTS()
        record.obj_ts.ave = domain2.DomainTimeSeries()
        record.obj_ts.med = domain2.DomainTimeSeries()
        record.obj_ts.std = domain2.DomainTimeSeries()
        record.obj_ts.cv = domain2.DomainTimeSeries()
        __MethodBasic(method, record.obj_ts.ave, record.objlist_resp, 'AVE')
        __MethodBasic(method, record.obj_ts.med, record.objlist_resp, 'MED')
        __MethodBasic(method, record.obj_ts.std, record.objlist_resp, 'STD')
        __MethodBasic(method, record.obj_ts.cv, record.objlist_resp, 'CV')


@basic.measure
def MethodHRA():
    method = func.Analysis().HRA
    objlist = dynamic.objlist_record

    for record in objlist:
        record.obj_hra = domain1.DomainHRA()
        record.obj_hra.pi = domain2.DomainNonlinear()
        record.obj_hra.gi = domain2.DomainNonlinear()
        record.obj_hra.si = domain2.DomainNonlinear()
        __MethodBasic(method, record.obj_hra.pi, record.objlist_resp, 'PI')
        __MethodBasic(method, record.obj_hra.gi, record.objlist_resp, 'GI')
        __MethodBasic(method, record.obj_hra.si, record.objlist_resp, 'SI')


@basic.measure
def MethodHRV():
    method = func.Analysis().HRV
    objlist = dynamic.objlist_record

    for record in objlist:
        record.obj_hrv = domain1.DomainHRV()
        record.obj_hrv.sd1 = domain2.DomainNonlinear()
        record.obj_hrv.sd2 = domain2.DomainNonlinear()
        __MethodBasic(method, record.obj_hrv.sd1, record.objlist_resp, 'SD1')
        __MethodBasic(method, record.obj_hrv.sd2, record.objlist_resp, 'SD2')


@basic.measure
def TimeAggregate():

    objlist_1 = dynamic.objlist_record
    objlist_2 = dynamic.objlist_table

    for i in range(len(objlist_1)):

        obj = domain0.DomainAggr_Time()

        obj.pid = objlist_2[i].pid
        obj.end = objlist_2[i].end
        obj.ave = objlist_1[i].obj_ts.ave
        obj.med = objlist_1[i].obj_ts.med
        obj.std = objlist_1[i].obj_ts.std
        obj.cv = objlist_1[i].obj_ts.cv

        dynamic.time_results.append(obj)


@basic.measure
def FreqAggregate():
    #TODO use the fd to sove the problem
    pass


@basic.measure
def NonlinearAggregate():

    objlist_1 = dynamic.objlist_record
    objlist_2 = dynamic.objlist_table

    for i in range(len(objlist_1)):

        obj = domain0.DomainAggr_NonL()

        obj.pid = objlist_2[i].pid
        obj.end = objlist_2[i].end
        obj.hra_pi = objlist_1[i].obj_hra.pi
        obj.hra_gi = objlist_1[i].obj_hra.gi
        obj.hra_si = objlist_1[i].obj_hra.si
        obj.hrv_sd1 = objlist_1[i].obj_hrv.sd1
        obj.hrv_sd2 = objlist_1[i].obj_hrv.sd2

        dynamic.nonl_results.append(obj)


@basic.measure
def TimeDomainTableBuild(form_name):

    colname = static.result_name_map
    result_list = dynamic.time_results
    save_form_n = static.save_table_name[form_name]
    df = FormProcess.FormPreProcess()

    df[colname['patient ID']] = [x.pid for x in result_list]
    df[colname['exTube end']] = [x.end for x in result_list]

    df[colname['Median RR']] = [x.med.RR for x in result_list]
    df[colname['Median V_T']] = [x.med.V_T for x in result_list]
    df[colname['Median VE']] = [x.med.VE for x in result_list]
    df[colname['Median WOB']] = [x.med.wob for x in result_list]
    df[colname['Median RSBI']] = [x.med.rsbi for x in result_list]
    df[colname['Median MP(Jm) d']] = [x.med.mp_jm_d for x in result_list]
    df[colname['Median MP(JL) d']] = [x.med.mp_jl_d for x in result_list]
    df[colname['Median MP(Jm) t']] = [x.med.mp_jm_t for x in result_list]
    df[colname['Median MP(JL) t']] = [x.med.mp_jl_t for x in result_list]

    df[colname['Average RR']] = [x.ave.RR for x in result_list]
    df[colname['Average V_T']] = [x.ave.V_T for x in result_list]
    df[colname['Average VE']] = [x.ave.VE for x in result_list]
    df[colname['Average WOB']] = [x.ave.wob for x in result_list]
    df[colname['Average RSBI']] = [x.ave.rsbi for x in result_list]
    df[colname['Average MP(Jm) d']] = [x.ave.mp_jm_d for x in result_list]
    df[colname['Average MP(JL) d']] = [x.ave.mp_jl_d for x in result_list]
    df[colname['Average MP(Jm) t']] = [x.ave.mp_jm_t for x in result_list]
    df[colname['Average MP(JL) t']] = [x.ave.mp_jl_t for x in result_list]

    df[colname['Standev RR']] = [x.std.RR for x in result_list]
    df[colname['Standev V_T']] = [x.std.V_T for x in result_list]
    df[colname['Standev VE']] = [x.std.VE for x in result_list]
    df[colname['Standev WOB']] = [x.std.wob for x in result_list]
    df[colname['Standev RSBI']] = [x.std.rsbi for x in result_list]
    df[colname['Standev MP(Jm) d']] = [x.std.mp_jm_d for x in result_list]
    df[colname['Standev MP(JL) d']] = [x.std.mp_jl_d for x in result_list]
    df[colname['Standev MP(Jm) t']] = [x.std.mp_jm_t for x in result_list]
    df[colname['Standev MP(JL) t']] = [x.std.mp_jl_t for x in result_list]

    df[colname['CV RR']] = [x.cv.RR for x in result_list]
    df[colname['CV V_T']] = [x.cv.V_T for x in result_list]
    df[colname['CV VE']] = [x.cv.VE for x in result_list]
    df[colname['CV WOB']] = [x.cv.wob for x in result_list]
    df[colname['CV RSBI']] = [x.cv.rsbi for x in result_list]
    df[colname['CV MP(Jm) d']] = [x.cv.mp_jm_d for x in result_list]
    df[colname['CV MP(JL) d']] = [x.cv.mp_jl_d for x in result_list]
    df[colname['CV MP(Jm) t']] = [x.cv.mp_jm_t for x in result_list]
    df[colname['CV MP(JL) t']] = [x.cv.mp_jl_t for x in result_list]

    dynamic.df_new = df

    FormProcess.CsvToLocal(dynamic.df_new, dynamic.save_form_loc, save_form_n)


@basic.measure
def NonlinearTableBuild(form_name):

    colname = static.result_name_map
    result_list = dynamic.nonl_results
    save_form_n = static.save_table_name[form_name]
    df = FormProcess.FormPreProcess()

    df[colname['patient ID']] = [x.pid for x in result_list]
    df[colname['exTube end']] = [x.end for x in result_list]

    df[colname['HRA RR'][0]] = [x.hra_pi.RR for x in result_list]
    df[colname['HRA RR'][1]] = [x.hra_gi.RR for x in result_list]
    df[colname['HRA RR'][2]] = [x.hra_si.RR for x in result_list]
    df[colname['HRA V_T'][0]] = [x.hra_pi.V_T for x in result_list]
    df[colname['HRA V_T'][1]] = [x.hra_gi.V_T for x in result_list]
    df[colname['HRA V_T'][2]] = [x.hra_si.V_T for x in result_list]
    df[colname['HRA VE'][0]] = [x.hra_pi.VE for x in result_list]
    df[colname['HRA VE'][1]] = [x.hra_gi.VE for x in result_list]
    df[colname['HRA VE'][2]] = [x.hra_si.VE for x in result_list]
    df[colname['HRA WOB'][0]] = [x.hra_pi.wob for x in result_list]
    df[colname['HRA WOB'][1]] = [x.hra_gi.wob for x in result_list]
    df[colname['HRA WOB'][2]] = [x.hra_si.wob for x in result_list]
    df[colname['HRA RSBI'][0]] = [x.hra_pi.rsbi for x in result_list]
    df[colname['HRA RSBI'][1]] = [x.hra_gi.rsbi for x in result_list]
    df[colname['HRA RSBI'][2]] = [x.hra_si.rsbi for x in result_list]
    df[colname['HRA MP(Jm) d'][0]] = [x.hra_pi.mp_jm_d for x in result_list]
    df[colname['HRA MP(Jm) d'][1]] = [x.hra_gi.mp_jm_d for x in result_list]
    df[colname['HRA MP(Jm) d'][2]] = [x.hra_si.mp_jm_d for x in result_list]
    df[colname['HRA MP(Jm) t'][0]] = [x.hra_pi.mp_jm_t for x in result_list]
    df[colname['HRA MP(Jm) t'][1]] = [x.hra_gi.mp_jm_t for x in result_list]
    df[colname['HRA MP(Jm) t'][2]] = [x.hra_si.mp_jm_t for x in result_list]
    df[colname['HRA MP(JL) d'][0]] = [x.hra_pi.mp_jl_d for x in result_list]
    df[colname['HRA MP(JL) d'][1]] = [x.hra_gi.mp_jl_d for x in result_list]
    df[colname['HRA MP(JL) d'][2]] = [x.hra_si.mp_jl_d for x in result_list]
    df[colname['HRA MP(JL) t'][0]] = [x.hra_pi.mp_jl_t for x in result_list]
    df[colname['HRA MP(JL) t'][1]] = [x.hra_gi.mp_jl_t for x in result_list]
    df[colname['HRA MP(JL) t'][2]] = [x.hra_si.mp_jl_t for x in result_list]

    df[colname['HRV RR'][0]] = [x.hrv_sd1.RR for x in result_list]
    df[colname['HRV RR'][1]] = [x.hrv_sd2.RR for x in result_list]
    df[colname['HRV V_T'][0]] = [x.hrv_sd1.V_T for x in result_list]
    df[colname['HRV V_T'][1]] = [x.hrv_sd2.V_T for x in result_list]
    df[colname['HRV VE'][0]] = [x.hrv_sd1.VE for x in result_list]
    df[colname['HRV VE'][1]] = [x.hrv_sd2.VE for x in result_list]
    df[colname['HRV WOB'][0]] = [x.hrv_sd1.wob for x in result_list]
    df[colname['HRV WOB'][1]] = [x.hrv_sd2.wob for x in result_list]
    df[colname['HRV RSBI'][0]] = [x.hrv_sd1.rsbi for x in result_list]
    df[colname['HRV RSBI'][1]] = [x.hrv_sd2.rsbi for x in result_list]
    df[colname['HRV MP(Jm) d'][0]] = [x.hrv_sd1.mp_jm_d for x in result_list]
    df[colname['HRV MP(Jm) d'][1]] = [x.hrv_sd2.mp_jm_d for x in result_list]
    df[colname['HRV MP(Jm) t'][0]] = [x.hrv_sd1.mp_jm_t for x in result_list]
    df[colname['HRV MP(Jm) t'][1]] = [x.hrv_sd2.mp_jm_t for x in result_list]
    df[colname['HRV MP(JL) d'][0]] = [x.hrv_sd1.mp_jl_d for x in result_list]
    df[colname['HRV MP(JL) d'][1]] = [x.hrv_sd2.mp_jl_d for x in result_list]
    df[colname['HRV MP(JL) t'][0]] = [x.hrv_sd1.mp_jl_t for x in result_list]
    df[colname['HRV MP(JL) t'][1]] = [x.hrv_sd2.mp_jl_t for x in result_list]

    dynamic.df_new = df

    FormProcess.CsvToLocal(dynamic.df_new, dynamic.save_form_loc, save_form_n)


@basic.measure
def LinearGraph():

    colname = static.result_name_map
    loc = pathlib.Path(dynamic.save_graph_loc) / 'Linear'
    loc.mkdir(parents=True, exist_ok=True)
    df = dynamic.df_new
    filt_ave = (df[colname['Average RR']] < 50)
    filt_std = (df[colname['Standev WOB']] <
                10) & (df[colname['Standev MP(JL)']] < 1)
    df = df[filt_ave & filt_std]
    draf = func.Draft(str(loc), df).BoxPlot

    targets_list = ['RR', 'V_T', 'VE', 'WOB', 'RSBI', 'MP(Jm)', 'MP(JL)']
    targets_len = len(targets_list)
    extube_colname_list = ['exTube end'] * targets_len
    average_colname_list = [('Average ' + x) for x in targets_list]
    standev_colname_list = [('Standev ' + x) for x in targets_list]
    cv_colname_list = [('CV ' + x) for x in targets_list]
    average_savename_list = [(x + '_average') for x in targets_list]
    standev_savename_list = [(x + '_standev') for x in targets_list]
    cv_savename_list = [(x + '_cv') for x in targets_list]

    for i in range(targets_len):

        draf(x_label=colname[extube_colname_list[i]],
             y_label=colname[average_colname_list[i]],
             fig_name=average_savename_list[i])

        draf(x_label=colname[extube_colname_list[i]],
             y_label=colname[standev_colname_list[i]],
             fig_name=standev_savename_list[i])

        draf(x_label=colname[extube_colname_list[i]],
             y_label=colname[cv_colname_list[i]],
             fig_name=cv_savename_list[i])


@basic.measure
def NonlinearGraph():

    colname = static.result_name_map
    loc = pathlib.Path(dynamic.save_graph_loc) / 'NonLinear'
    loc.mkdir(parents=True, exist_ok=True)
    df = dynamic.df_new

    targets_list = ['RR', 'V_T', 'VE', 'WOB', 'RSBI', 'MP(Jm)', 'MP(JL)']
    targets_len = len(targets_list)
    extube_colname_list = ['exTube end'] * targets_len
    hra_colname_list = [('HRA ' + x) for x in targets_list]
    hra_savename_list = [(x + '_HRA') for x in targets_list]
    hrv_colname_list = [('HRV ' + x) for x in targets_list]
    hrv_savename_list = [(x + '_HRV') for x in targets_list]

    filt_list_hra = [
        (df[colname['HRA RR'][2]] < 20000),
        (df[colname['HRA V_T'][1]] < 52) & (df[colname['HRA V_T'][2]] < 10000)
        & (df[colname['HRA V_T'][2]] > -20000),
        (df[colname['HRA VE'][1]] < 54) & (df[colname['HRA VE'][2]] > -20000),
        (df[colname['HRA WOB'][1]] < 54), (df[colname['HRA RSBI'][1]] < 51.5) &
        (df[colname['HRA RSBI'][2]] > -12000) &
        (df[colname['HRA RSBI'][2]] < 12000),
        (df[colname['HRA MP(Jm)'][1]] < 54) &
        (df[colname['HRA MP(Jm)'][2]] < 20000),
        (df[colname['HRA MP(JL)'][2]] < 30000)
    ]

    filt_list_hrv = [
        (df[colname['HRV RR'][0]] < 20) & (df[colname['HRV RR'][1]] < 20),
        (df[colname['HRV V_T'][0]] < 1000), (df[colname['HRV VE'][0]] < 20),
        (df[colname['HRV WOB'][0]] < 10) & (df[colname['HRV WOB'][1]] < 10),
        (df[colname['HRV RSBI'][0]] < 2000)
        & (df[colname['HRV RSBI'][1]] < 2000),
        (df[colname['HRV MP(Jm)'][0]] < 20),
        (df[colname['HRV MP(JL)'][0]] < 1) & (df[colname['HRV MP(JL)'][1]] < 1)
    ]

    draf = func.Draft(loc, df).BoxPlotMulti

    for i in range(targets_len):

        draf(x_label=colname[extube_colname_list[i]],
             y_labels=colname[hra_colname_list[i]],
             fig_name=hra_savename_list[i],
             filt=filt_list_hra[i])

        draf(x_label=colname[extube_colname_list[i]],
             y_labels=colname[hrv_colname_list[i]],
             fig_name=hrv_savename_list[i],
             filt=filt_list_hrv[i])
