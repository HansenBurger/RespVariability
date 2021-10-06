from Code.Fundal import BinImport as BI
from Code.Fundal import ReadSamplerate as RS
import numpy as np


def IndexSet(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]


class PointProcessing():
    def __init__(self, zdt_loc):
        self.__zdt = zdt_loc
        self.__head_size = 0
        self.__channel_cnt = 0
        self.__sample_rate = 0
        self.__wave_data = None

        self.p_s = []
        self.s_F = []
        self.s_P = []
        self.s_V = []
        pass

    def __HeadInfo(self):

        wave_header = BI.ImportWaveHeader(self.__zdt)[0]
        self.__head_size = wave_header["HeaderSize"].item()
        self.__channel_cnt = wave_header["ChannelCnt"].item()

        sample_rate = wave_header["RefSampleRate"].item()

        if sample_rate == 0:
            machine_type = wave_header["Reserved1"][0].item()
            sample_rate = RS.ReadSamplerate(machine_type)
            self.__sample_rate = sample_rate
        else:
            self.__sample_rate = sample_rate

    def __BuildWaveData(self):

        self.__HeadInfo()
        with open(self.__zdt, "rb") as fid:
            fid.seek(self.__head_size)
            data_info = np.fromfile(fid, np.uint16).tolist()
            data_info = np.array(data_info)

        if len(data_info) % self.__channel_cnt != 0:
            norm_length = int(
                len(data_info) / self.__channel_cnt) * self.__channel_cnt
            data_info = data_info[:norm_length]

        row_n = int(len(data_info) / self.__channel_cnt)
        column_n = self.__channel_cnt

        self.__wave_data = np.reshape((data_info - 32768) / 100,
                                      (row_n, column_n)).T

    def main(self):

        self.__BuildWaveData()
        resp_mark = {"insp_mark": False, "exsp_mark": False}
        insp_mark_list = []
        exsp_mark_list = []

        if self.__channel_cnt == 2:
            F = self.__wave_data[0]
            P = self.__wave_data[1]
            V = []

        elif self.__channel_cnt == 3:
            F = self.__wave_data[0]
            P = self.__wave_data[1]
            V = self.__wave_data[2]

        for i in range(len(F)):

            if F[i] == 327.67:
                resp_mark["insp_mark"] = True
                resp_mark["exsp_mark"] = False
            elif F[i] == 327.65:
                resp_mark["insp_mark"] = False
                resp_mark["exsp_mark"] = True
            else:
                self.s_F.append(F[i])
                self.s_P.append(P[i])
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

        s_V = [0] * len(self.s_P) if not V.all() else V
        start_ind = IndexSet(insp_mark_list, lambda x: x == 1)
        min_ind = IndexSet(exsp_mark_list, lambda x: x == 1)

        del insp_mark_list, exsp_mark_list

        for i in range(len(start_ind) - 1):
            point_sta = start_ind[i]
            point_end = start_ind[i + 1]
            sumV = 0
            a_id_list = [id(x) for x in s_V[0:20]]
            for j in range(point_sta, point_end, 1):
                sumV += (self.s_F[j] * 1000) / (60 * self.__sample_rate)
                s_V[j] = sumV

        self.s_V = [0 for x in s_V if x < 0]