import sys, pathlib
import pandas as pd
import numpy as np

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import InIReaWri, FormProcess

form_loc = InIReaWri.ConfigR('FormRoute', 'ModeForm', conf=None)
save_form_loc = InIReaWri.ConfigR('ResultRoute', 'FormFolder_new', conf=None)
save_graph_loc = InIReaWri.ConfigR('ResultRoute', 'GraphFolder', conf=None)

time_col = ['Resp_t', 'end_time', 'Heart_t', 'endo_t', 'SBT_time']
df = FormProcess.FormPreProcess(form_loc, sort_jud=['PID', 'Resp_t'])
FormProcess.TimeShift(df, time_col)
gp = pd.DataFrame.groupby(df, 'PID')
pid_list = df['PID'].unique().tolist()

save_dict = {'PID': [], 'ICU': [], 'machine': [], 'endo_end': [], 'vent_m': []}


def Certificate(df):

    vent_m_list = []
    max_t = df['Resp_t'].max()
    baguan_t = df['endo_t'].unique()[0]

    if max_t <= baguan_t:
        Collect(df, vent_m_list)
    elif max_t > baguan_t:
        df_up = df.loc[df['Resp_t'] <= df['endo_t']]
        df_down = df.loc[df['Resp_t'] > df['endo_t']]
        filt_0 = df['vent_m_0'].str.contains(
            'SPONT') | df['vent_m_0'].str.contains('CPAP')
        filt_1 = df['vent_m_1'].str.contains(
            'SPONT') | df['vent_m_1'].str.contains('CPAP')
        df_down = df_down.loc[filt_0 | filt_1]
        df_ = pd.concat([df_up, df_down],
                        ignore_index=True) if not df_down.empty else df_up
        # if df['PID'].unique()[0] == 3400875:
        #     a = 1
        if df_.empty:
            print(df['PID'].unique()[0])
        Collect(df_, vent_m_list)
    return vent_m_list


def Collect(df_, list_):
    for i in df_.index:
        list_.append(df_.loc[i, 'vent_m_1'])
        list_.append(df_.loc[i, 'vent_m_0'])
    list_.reverse()
    return


def BuildListbyRange(num):
    list_ = []
    for i in range(num):
        min_gap = str((i + 1) * 30).rjust(3, '0')
        list_.append('mode_' + min_gap + '_min')
    return list_


for pid in pid_list:

    df_tmp = gp.get_group(pid)
    filt_v60 = df['machine'].str.contains('V60')
    df_tmp = df_tmp.loc[~filt_v60]  # pass all mode V60

    if not df_tmp.empty:

        vent_m_list = Certificate(df_tmp)

        if vent_m_list:
            save_dict['PID'].append(pid)
            save_dict['ICU'].append(df_tmp['ICU'].unique()[0])
            save_dict['endo_end'].append(df_tmp['endo_end'].unique()[0])
            machine_type = '_'.join(
                df_tmp['machine'].unique().tolist()) if len(
                    df_tmp['machine'].unique(
                    )) > 1 else df_tmp['machine'].unique()[0]
            save_dict['machine'].append(machine_type)
            save_dict['vent_m'].append(vent_m_list)

max_ventm_time = len(max(save_dict['vent_m'], key=len))
time_gap_name_list = BuildListbyRange(max_ventm_time)

for i in range(len(save_dict['vent_m'])):
    save_dict['vent_m'][i] += [''] * (max_ventm_time -
                                      len(save_dict['vent_m'][i]))

arr = np.asarray(save_dict['vent_m'])

for i in range(max_ventm_time):
    save_dict[time_gap_name_list[i]] = arr[:, i]

del save_dict['vent_m']

df_save = pd.DataFrame.from_dict(save_dict)
pd.DataFrame.to_csv(df_save,
                    save_form_loc + 'vent_mode_bytime.csv',
                    index=False)


def StrFilt(df, col, string_list):
    if len(string_list) > 1:
        filt = df[col].str.contains(string_list[0]) | df[col].str.contains(
            string_list[1])
    else:
        filt = df[col].str.contains(string_list[0])

    return filt


def ValueToKey(dict_, key):
    key_list = dict_.keys()
    for i in key_list:
        if i == key:
            return
    dict_[key] = {'succ': 0, 'fail': 0}
    return


def Count(df, col_name):
    dict_ = {}
    for i in df.index:
        vent_m = df.loc[i, col_name]
        if vent_m == '' or vent_m == '107':
            continue
        ValueToKey(dict_, vent_m)
        if '成功' in df.loc[i, 'endo_end']:
            dict_[vent_m]['succ'] += 1
        elif '失败' in df.loc[i, 'endo_end']:
            dict_[vent_m]['fail'] += 1
    return dict_


def VentFunc(df, col_name):
    list_0 = []
    list_1 = []
    dict_ = Count(df, col_name)
    [(k, dict_[k]) for k in sorted(dict_.keys())]
    vent_m = list(dict_.keys())
    for i in vent_m:
        print(i, ': ', dict_[i]['succ'], '|', dict_[i]['fail'])
        list_0.append(dict_[i]['succ'])
        list_1.append(dict_[i]['fail'])
    dict_tmp = {'successful': list_0, 'failed': list_1}
    return dict_tmp, vent_m


def Plot_bar(dict_, list_index=None, fig_name=None, width_=0.7):
    df = pd.DataFrame(dict_, index=list_index)
    plt = df.plot(kind='bar',
                  stacked=True,
                  width=width_,
                  sort_columns=True,
                  figsize=(20, 10),
                  fontsize=12)
    fig = plt.get_figure()
    fig.savefig(save_graph_loc + fig_name)


# for i in range(max_ventm_time)[:10]:
#     col_name = time_gap_name_list[i]
#     print('the result of ', col_name)
#     output = VentFunc(df_save, col_name)
#     Plot_bar(output[0], output[1], col_name + '.jpg', width_=0.7)

filt_icu3 = df_save['ICU'] == 'ICU3F'

for i in range(max_ventm_time)[:2]:
    col_name = time_gap_name_list[i]
    print('the result of ', col_name)
    output = VentFunc(df_save.loc[filt_icu3], col_name)
    Plot_bar(output[0], output[1], col_name + '_icu3_.jpg', width_=0.7)

a = 1