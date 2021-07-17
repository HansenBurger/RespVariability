import sys, pathlib
from copy import deepcopy

sys.path.append(str(pathlib.Path.cwd().parents[0]))
from Code import InIReaWri, PointProcess

zdt_sample = InIReaWri.ConfigR('FileTestRoute', 'WaveRead_zdt', conf=None)


def ZeroJudge(list_):
    list_ = list(map(lambda x: 0 if x < 0 else x, list_))


def FromkeysReid(dict_name):
    dict_ = dict.fromkeys(dict_name)
    for i in dict_name:
        tmp = []
        dict_[i] = deepcopy(tmp)

    return dict_


vent_list = PointProcess.PointProcessing(zdt_sample)
vent_name = ['p_s', 'p_e', 's_F', 's_P', 's_V', 'ref_samplerate']
vent_dict = FromkeysReid(vent_name)

for i in range(len(vent_list)):
    vent_dict[vent_name[i]] = vent_list[i]

ZeroJudge(vent_dict['s_V'])

for i in range(len(vent_dict['p_s']) - 1):

    start_point = vent_dict['p_s'][i]
    end_point = vent_dict['p_s'][i + 1] - 1

    wave_len = end_point - start_point

    if wave_len == 0 or wave_len < 50 or wave_len > 450:
        continue
    else:
        wave_data_f = vent_dict['s_F'][start_point, end_point]
