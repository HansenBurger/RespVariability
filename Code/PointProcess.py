from Code.Fundal import BinImport as BI
from Code.Fundal import ReadSamplerate as RS
import numpy as np


def IndexSet(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]


def PointProcessing(*args):

    resp_mark = {"insp_mark": True, "exsp_mark": False}

    s_F = []
    s_P = []
    s_V = []
    insp_mark_list = []
    exsp_mark_list = []

    wave_header = BI.ImportWaveHeader(args[0])[0]
    head_size = wave_header["HeaderSize"].item()
    channel_cnt = wave_header["ChannelCnt"].item()
    ref_sample_rate = wave_header["RefSampleRate"].item()

    if ref_sample_rate == 0:
        machine_type = wave_header["Reserved1"][0].item()
        ref_sample_rate = RS.ReadSamplerate(machine_type)

    with open(args[0], "rb") as fid:
        fid.seek(head_size)
        data_info = np.fromfile(fid, np.uint16).tolist()
        data_info = np.array(data_info)

    if len(data_info) % channel_cnt != 0:
        norm_length = int(len(data_info) / channel_cnt) * channel_cnt
        data_info = data_info[:norm_length]

    row_n = int(len(data_info) / channel_cnt)
    column_n = channel_cnt

    wave_data = np.reshape((data_info - 32768) / 100, (row_n, column_n)).T

    if channel_cnt == 2:
        F = wave_data[0]
        P = wave_data[1]
        v = []

    elif channel_cnt == 3:
        F = wave_data[0]
        P = wave_data[1]
        V = wave_data[2]

    for i in range(len(F)):

        if F[i] == 327.67:
            resp_mark["insp_mark"] = True
            resp_mark["exsp_mark"] = False
        elif F[i] == 327.65:
            resp_mark["insp_mark"] = False
            resp_mark["exsp_mark"] = True
        else:
            s_F.append(F[i])
            s_P.append(P[i])
            if resp_mark["insp_mark"]:
                insp_mark_list.append(1)
                exsp_mark_list.append(0)
                resp_mark["insp_mark"] = False
            elif resp_mark["exsp_mark"]:
                insp_mark_list.append(0)
                exsp_mark_list.append(1)
                resp_mark["exsp_mark"] = False
            else:
                insp_mark_list.append(0)
                exsp_mark_list.append(0)

    start_ind = IndexSet(insp_mark_list, lambda x: x == 1)
    min_ind = IndexSet(exsp_mark_list, lambda x: x == 1)

    for i in range(len(start_ind) - 1):
        point_sta = start_ind[i]
        point_end = start_ind[i + 1]
        sumV = 0
        for j in range(point_sta, point_end, 1):
            sumV += (s_F[j] * 1000) / (60 * ref_sample_rate)
            s_V.append(sumV)

    return [start_ind, min_ind, s_F, s_P, s_V, ref_sample_rate]
