import numpy as np
import pandas as pd
import seaborn as sns
from scipy import signal
from datetime import datetime
import matplotlib.pyplot as plt
from class_data import Data, Target
import sys, pathlib, sqlite3

sys.path.append(str(pathlib.Path.cwd().parents[1]))

from Code.Fundal import BinImport
from Code import FormProcess, PointProcess
from _Main.effect_vertification import class_func, class_domain_0, class_domain_1

data = Data()


def TableBuild(pid):
    with sqlite3.connect(data.db_loc()) as con:
        df = pd.read_sql(data.pid_statement(pid), con)

    df = df.rename(columns=data.table_info('col_map'))
    FormProcess.TimeShift(df, data.table_info('time_col'))
    obj = class_domain_0.DomainTable()
    obj.pid = df['PID'].item()
    obj.time = df['REC_t'].item()
    obj.rid = df['RID'].item()
    obj.zdt = df['zdt'].item()
    obj.zpx = df['zpx'].item()
    obj.end = 0 if '成功' in df['Extube_end'].item() else 1
    data.record_0 = obj


def BinaryRead():
    s_t = datetime.now()

    obj = class_domain_0.DomainRecord()
    loc_build = class_func.FileLocBuild(data.records_loc(), data.record_0, obj)
    loc_build.ZifLoc()
    loc_build.ZdtLoc()
    loc_build.ZpxLoc()

    bin_read = class_func.OutputCheck(obj)
    zif_ = bin_read.ZifContentCheck(BinImport.ImportZif)
    zdt_ = bin_read.ZdtHeaderCheck(BinImport.ImportWaveHeader)
    wave_ = bin_read.ZdtContentCheck(PointProcess.PointProcessing)

    e_t = datetime.now()

    print('Process consum: {0}'.format(e_t - s_t))

    obj.machine = zif_['machineType'].split('-')[0]
    obj.sample_rate = zdt_['RefSampleRate'].item()
    obj.p_list = wave_[0]
    obj.s_F = wave_[2]
    obj.s_P = wave_[3]
    obj.s_V = wave_[4]
    obj.p_start = obj.p_list[:len(obj.p_list) - 1]
    obj.p_end = [x - 1 for x in obj.p_list[1:]]

    data.record_1 = obj


def Calculate():
    record = data.record_1
    targets_arr = Target()
    for i in range(len(record.p_start)):

        resp = class_domain_1.DomainResp()
        resp_ind = [record.p_start[i], record.p_end[i]]
        counter = class_func.Calculation(resp_ind[0], resp_ind[1])
        counter.ValidityCheck(record.s_F, record.s_V, record.s_P)

        if not counter.valid_tag:
            continue

        else:

            targets_arr.resp_t.append(
                round(resp_ind[0] * 1 / record.sample_rate))

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

    data.targets = targets_arr


def Agger():
    targets_arr = data.targets
    targets_arr.rr = np.array([x.RR for x in data.record_1.objlist_resp])
    targets_arr.v_t = np.array([x.V_T_i for x in data.record_1.objlist_resp])
    targets_arr.mv = np.array([x.VE for x in data.record_1.objlist_resp])
    targets_arr.rsbi = np.array([x.rsbi for x in data.record_1.objlist_resp])
    targets_arr.wob = np.array([x.wob for x in data.record_1.objlist_resp])
    targets_arr.mp_jm_d = np.array(
        [x.mp_jm_d for x in data.record_1.objlist_resp])
    targets_arr.mp_jl_d = np.array(
        [x.mp_jl_d for x in data.record_1.objlist_resp])
    targets_arr.mp_jm_t = np.array(
        [x.mp_jm_t for x in data.record_1.objlist_resp])
    targets_arr.mp_jl_t = np.array(
        [x.mp_jl_t for x in data.record_1.objlist_resp])
    targets_arr.resp_t = np.array(targets_arr.resp_t)

    return targets_arr


class PlotMain():
    def __init__(self, save_loc=str(pathlib.Path.cwd())):
        self.__safe_loc = save_loc

    def lmplot(self, x_label, y_label, df, fig_name):
        save_loc = pathlib.Path(self.__safe_loc) / (fig_name + '.png')
        sns.set_theme(style='whitegrid')
        sns.lmplot(x=x_label,
                   y=y_label,
                   data=df,
                   fit_reg=False,
                   height=3.3,
                   aspect=5.5)
        plt.title(fig_name, fontsize=12)
        plt.savefig(save_loc)
        plt.close()

    def lineplot(self, x_label, y_label, df, fig_name):
        save_loc = pathlib.Path(self.__safe_loc) / (fig_name + '.png')
        sns.set_theme(style='whitegrid')
        sns.set(rc={'figure.figsize': (18, 7)})
        sns.lineplot(x=x_label, y=y_label, data=df)
        plt.title(fig_name, fontsize=12)
        plt.savefig(save_loc)
        plt.close()


class FreqPreMethod():
    def __init__(self, time_array, target_array, range_):
        self.__time_a = time_array[range_]
        self.__target_a = target_array[range_]
        self.df_raw = None
        self.df_interp = None
        self.df_sample = None

    def __LenVertify(self):
        if not len(self.__time_a) == len(self.__target_a):
            print('Length Mismatch !')
            return

    def __SpaceGen(self, fs):
        ind_0 = self.__time_a.min()
        ind_1 = self.__time_a.max()
        ind_num = (ind_1 - ind_0) * fs
        array = np.linspace(ind_0, ind_1, ind_num, endpoint=False)
        array = np.around(array, decimals=2)
        return array

    def InitTimeSeries(self):
        self.__LenVertify()

        df = pd.DataFrame({'time': self.__time_a, 'value': self.__target_a})
        self.df_raw = df

    def InterpValue(self, interp_rate):
        self.__LenVertify()

        array_x = self.__SpaceGen(interp_rate)
        array_y = np.interp(array_x, self.__time_a, self.__target_a)

        df = pd.DataFrame({'time': array_x, 'value': array_y})
        self.df_interp = df

    def Resampling(self, resample_rate):
        self.__LenVertify()

        array_x = self.__SpaceGen(resample_rate)
        array_y = np.array([
            self.df_interp.loc[self.df_interp['time'] == i]['value'].item()
            for i in array_x
        ])

        df = pd.DataFrame({'time': array_x, 'value': array_y})
        self.df_sample = df


class FreqTransMethod():
    def __init__(self, time_series, sample_rate):
        self.__t_a = time_series  # time series input
        self.__fs = sample_rate  # sampling rate
        self.__n = len(time_series)  #
        self.fft_bi = None
        self.fft_si = None
        self.ps_si = None

    def __FFT(self):

        f_ind = np.arange(self.__n) / (self.__n / self.__fs)
        f_output = np.fft.fft(self.__t_a) / self.__n  # 归一化
        f_output = signal.detrend(f_output)
        f_output = np.abs(f_output)
        f_output[0] = 0

        return f_ind, f_output

    def FFT_Bi(self):
        # FS bilateral spectrum
        f_ind, f_out = self.__FFT()

        df = pd.DataFrame({'freq': f_ind, 'range': f_out})
        self.fft_bi = df

    def FFT_Si(self):
        # FS unilateral spectrum
        f_ind, f_out = self.__FFT()
        f_ind = f_ind[range(int(self.__n / 2))]
        f_out = f_out[range(int(self.__n / 2))]

        df = pd.DataFrame({'freq': f_ind, 'range': f_out})[:350]
        self.fft_si = df

    def PS_Si(self):
        if self.fft_si.empty:
            return
        else:
            f_ind = self.fft_si.freq
            f_out = self.fft_si.range
            f_out = f_out**2

            df = pd.DataFrame({'freq': f_ind, 'range': f_out})[:350]
            self.ps_si = df
