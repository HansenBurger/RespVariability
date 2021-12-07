import numpy as np
import pandas as pd


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

        df = pd.DataFrame({'freq': f_ind, 'range': f_out})
        self.fft_si = df

    def PS_Si(self):
        if self.fft_si.empty:
            return
        else:
            f_ind = self.fft_si.freq
            f_out = self.fft_si.range
            f_out = f_out**2

            df = pd.DataFrame({'freq': f_ind, 'range': f_out})