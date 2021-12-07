from pathlib import Path, PurePath
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.records import array
import seaborn as sns


class RecordFucBasic():
    def __init__(self) -> None:
        pass


class FileLocBuild(RecordFucBasic):
    def __init__(self, cwd, obj_table, obj_record):
        super().__init__()
        self.__cwd = cwd
        self.__obj_1 = obj_table
        self.__obj_2 = obj_record

    def __Folder(self, main_loc, time_info, rid):
        parents_2 = Path(main_loc) if not isinstance(main_loc,
                                                     PurePath) else main_loc
        parents_1 = (str(time_info.year) + str(time_info.month).rjust(2, '0'))
        parents_0 = rid
        folder_loc = parents_2 / parents_1 / parents_0

        return folder_loc

    def ZifLoc(self):
        parent_loc = self.__Folder(self.__cwd, self.__obj_1.time,
                                   self.__obj_1.rid)
        self.__obj_2.zif_loc = parent_loc / (self.__obj_1.rid + '.zif')

    def ZdtLoc(self):
        parent_loc = self.__Folder(self.__cwd, self.__obj_1.time,
                                   self.__obj_1.rid)
        self.__obj_2.zdt_loc = parent_loc / (self.__obj_1.zdt + '.zdt')

    def ZpxLoc(self):
        parent_loc = self.__Folder(self.__cwd, self.__obj_1.time,
                                   self.__obj_1.rid)
        self.__obj_2.zpx_loc = parent_loc / (self.__obj_1.zpx + '.zpx')


class OutputCheck(RecordFucBasic):
    def __init__(self, obj):
        super().__init__()
        self.__obj = obj
        self.__size_min = 100

    def ZifContentCheck(self, func):
        default = None
        if self.__obj.zif_loc.stat().st_size >= self.__size_min:
            return func(self.__obj.zif_loc)
        else:
            return default

    def ZdtHeaderCheck(self, func):
        default = {}
        if self.__obj.zdt_loc.stat().st_size >= self.__size_min:
            return func(self.__obj.zdt_loc)[0]
        else:
            return default

    def ZdtContentCheck(self, class_):
        default = [[], [], [], [], [], 0]
        if self.__obj.zdt_loc.stat().st_size >= self.__size_min:
            return class_(self.__obj.zdt_loc)
        else:
            return default


class Calculation(RecordFucBasic):
    def __init__(self, p_start, p_end):
        super().__init__()
        self.__pro_ind = p_start
        self.__end_ind = p_end
        self.__min_ind = 0
        self.__p_in = np.array([])
        self.__p_ex = np.array([])
        self.__v_in = np.array([])
        self.__v_ex = np.array([])

        self.valid_tag = True

    def __GapDetection(self):
        min_gap = 50
        max_gap = 450
        gap = abs(self.__end_ind - self.__pro_ind)

        if gap < min_gap or gap > max_gap or gap == 0:
            return False
        else:
            return True

    def __LineDetection(self, array_):

        if np.all(array_ == array_[0]):
            return False
        else:
            return True

    def __SwitchPoint(self, array_):
        interval = 15
        ind_array = np.where(array_[interval:] < 0)[0]
        try:
            ind = ind_array[0] + interval
        except:
            ind = None
        return ind

    def __LenMatch(self, array_1, array_2):
        len_1 = array_1.shape[0]
        len_2 = array_2.shape[0]

        if len_1 != len_2:
            self.valid_tag = False

    def __ArrayCertify(self, list_):
        list_ = [list_] if type(list_) == np.array else list_

        for array in list_:
            if not np.any(array):
                self.valid_tag = False
                return

    def ValidityCheck(self, s_F, s_V, s_P):
        if self.__GapDetection():
            f_wave = np.array(s_F[self.__pro_ind:self.__end_ind])
            if self.__LineDetection(f_wave) and self.__SwitchPoint(f_wave):
                self.__min_ind = self.__SwitchPoint(f_wave) + self.__pro_ind
                if self.__min_ind != self.__pro_ind:

                    self.__p_in = np.array(s_P[self.__pro_ind:self.__min_ind])
                    self.__p_ex = np.array(s_P[self.__min_ind:self.__end_ind])
                    self.__v_in = np.array(s_V[self.__pro_ind:self.__min_ind])
                    self.__v_ex = np.array(s_V[self.__min_ind:self.__end_ind])

                    self.__ArrayCertify(
                        [self.__p_in, self.__p_ex, self.__v_in, self.__v_ex])
                    self.__LenMatch(self.__p_in, self.__v_in)
                    self.__LenMatch(self.__p_ex, self.__v_ex)

                    if self.__v_in[-1] == 0:
                        self.valid_tag = False

                else:
                    self.valid_tag = False
            else:
                self.valid_tag = False
        else:
            self.valid_tag = False

    def RR(self, sample_rate):
        vent_len = self.__end_ind - self.__pro_ind
        RR = 60 / (vent_len * 1 / sample_rate)
        return round(RR, 2)

    def V_t_i(self):
        v_t_i = self.__v_in[-1]
        return round(v_t_i, 2)

    def V_t_e(self):
        v_t_e = self.__v_in[-1] + (self.__v_ex[-1] if self.__v_ex[-1] < 0 else
                                   -self.__v_ex[-1])
        return round(v_t_e, 2)

    def WOB(self):
        vp_rectangle = (self.__p_in[-1] * self.__v_in[-1]) / 1000
        peep_rectangle = (self.__p_in[0] * self.__v_in[-1]) / 1000
        inhal_points = abs(np.trapz(self.__v_in, self.__p_in)) / 1000

        wob_full = vp_rectangle - inhal_points
        wob = wob_full - peep_rectangle
        wob_b = ((self.__p_in[-1] - self.__p_in[0]) * self.__v_in[-1]) / 2000
        wob_a = wob - wob_b

        return [
            round(wob, 2),
            round(wob_full, 2),
            round(wob_a, 2),
            round(wob_b, 2)
        ]

    def VE(self, rr, v_t):
        VE = rr * (v_t / 1000)
        return round(VE, 2)

    def RSBI(self, rr, v_t):
        rsbi = rr / (v_t / 1000)
        return round(rsbi, 2)

    def MP_Area(self, rr, v_t, wob):
        mp_jm_area = 0.098 * rr * wob
        mp_jl_area = 0.098 * wob / (v_t * 0.001)
        return [round(mp_jm_area, 2), round(mp_jl_area, 2)]


class ParaValidity(RecordFucBasic):
    def __init__(self, resp_obj):
        super().__init__()
        self.__obj = resp_obj
        self.validity = True

    def __ValRangeCheck(self, var, ran):
        self.validity = True if round(var) in ran else False

    def __RR_val(self):
        rr = self.__obj.RR
        val_range = range(0, 60)
        self.__ValRangeCheck(rr, val_range)

    def __VT_val(self):
        vt_i = self.__obj.V_T_i
        vt_e = self.__obj.V_T_e
        val_range = range(0, 2000)
        self.__ValRangeCheck(vt_i, val_range)
        self.__ValRangeCheck(vt_e, val_range)

    def __VE_val(self):
        ve = self.__obj.VE
        val_range = range(0, 30)
        self.__ValRangeCheck(ve, val_range)

    def __WOB_val(self):
        wob_a = self.__obj.wob_a
        wob_b = self.__obj.wob_b
        val_range = range(0, 20)
        self.__ValRangeCheck(wob_a, val_range)
        self.__ValRangeCheck(wob_b, val_range)

    def __MP_val(self):
        mp_jm_d = self.__obj.mp_jm_d
        mp_jl_d = self.__obj.mp_jl_d
        mp_jm_t = self.__obj.mp_jm_t
        mp_jl_t = self.__obj.mp_jl_t
        val_range = range(0, 20)
        self.__ValRangeCheck(mp_jm_d, val_range)
        self.__ValRangeCheck(mp_jl_d, val_range)
        self.__ValRangeCheck(mp_jm_t, val_range)
        self.__ValRangeCheck(mp_jl_t, val_range)

    def ValTotal(self, rr=True, vt=True, ve=True, wob=True, mp=True):
        if rr:
            self.__RR_val()
        if vt:
            self.__VT_val()
        if ve:
            self.__VE_val()
        if wob:
            self.__WOB_val()
        if mp:
            self.__MP_val()


class Analysis(RecordFucBasic):
    def __init__(self):
        super().__init__()

    def __PI(self, a_0, a_1):
        n = 0
        m = 0
        for i in range(len(a_0)):
            n += 1 if a_0[i] < a_1[i] else 0
            m += 1 if a_0[i] > a_1[i] else 0
        pi = 100 * m / (n + m)
        return round(pi, 2)

    def __GI(self, a_0, a_1):
        d1 = 0
        d2 = 0
        for i in range(len(a_0)):
            d1 += (a_1[i] - a_0[i]) / np.sqrt(2) if a_0[i] < a_1[i] else 0
            d2 += (a_0[i] - a_1[i]) / np.sqrt(2) if a_0[i] > a_1[i] else 0
        gi = 100 * d1 / (d1 + d2)
        return round(gi, 2)

    def __SI(self, a_0, a_1):
        theta_1 = 0
        theta_2 = 0
        for i in range(len(a_0)):
            theta_1 += (np.degrees(np.arctan(a_1[i] / a_0[i])) -
                        45) if a_0[i] < a_1[i] else 0
            theta_2 += (-np.degrees(np.arctan(a_1[i] / a_0[i])) +
                        45) if a_0[i] > a_1[i] else 0
        si = 100 * theta_1 / (theta_1 + theta_2)
        return round(si, 2)

    def __SD1(self, a_0, a_1):
        sd = np.std(a_1 - a_0) / np.sqrt(2)
        return round(sd, 2)

    def __SD2(self, a_0, a_1):
        sd = np.std(a_1 + a_0) / np.sqrt(2)
        return round(sd, 2)

    def Mean(self, list_):
        array_ = np.array(list_)
        result = np.mean(array_)
        return round(result, 2)

    def StanDev(self, list_):
        array_ = np.array(list_)
        result = np.std(array_)
        return round(result, 2)

    def TimeSeries(self, list_, method_sub):
        array_ = np.array(list_)

        if method_sub == 'AVE':
            ave = np.mean(array_)
            return round(ave, 2)
        if method_sub == 'STD':
            std = np.std(array_)
            return round(std, 2)
        if method_sub == 'CV':
            cv = np.std(array_) / np.mean(array_)
            return round(cv, 2)

    def HRA(self, list_, method_sub):
        array_0 = np.array(list_[:len(list_) - 1])
        array_1 = np.array(list_[1:])

        if method_sub == 'PI':
            pi = self.__PI(array_0, array_1)
            return pi
        if method_sub == 'GI':
            gi = self.__GI(array_0, array_1)
            return gi
        if method_sub == 'SI':
            si = self.__SI(array_0, array_1)
            return si

    def HRV(self, list_, method_sub):
        array_0 = np.array(list_[:len(list_) - 1])
        array_1 = np.array(list_[1:])

        if method_sub == 'SD1':
            sd1 = self.__SD1(array_0, array_1)
            return sd1
        if method_sub == 'SD2':
            sd2 = self.__SD2(array_0, array_1)
            return sd2


class Draft(RecordFucBasic):
    def __init__(self, save_loc, df=None):
        super().__init__()
        self.__save_loc = save_loc
        self.__df = df

    def BoxPlot(self, x_label, y_label, fig_name):
        saveloc = Path(self.__save_loc) / (fig_name + '.png')
        sns.set_theme(style="whitegrid")
        sns.boxplot(x=x_label, y=y_label, data=self.__df, order=[0, 1])
        plt.title(fig_name, fontsize=15)
        plt.savefig(saveloc)
        plt.close()

    def BoxPlotMulti(self, x_label, y_labels, fig_name, filt=None):
        saveloc = Path(self.__save_loc) / (fig_name + '.png')
        df = self.__df[filt] if not filt.empty else self.__df
        #df = self.__df
        multi_size = len(y_labels)
        sns.set_theme(style="whitegrid")
        sns.set(rc={'figure.figsize': (3.4 * multi_size, 4)})
        for i in range(multi_size):
            plt.subplot(1, multi_size, i + 1)
            sns.boxplot(x=x_label, y=y_labels[i], data=df,
                        order=[0, 1]).set_title(y_labels[i].split('_')[1])
        plt.tight_layout()
        plt.savefig(saveloc)
        plt.close()

    def ScatterPlot(self, x_label, y_label, folder_name, fig_name, tag):
        save_folder = Path(self.__save_loc) / folder_name
        save_folder.mkdir(parents=True, exist_ok=True)
        saveloc = save_folder / (fig_name + '.png')
        sns.scatterplot(data=self.__df, x=x_label, y=y_label)
        plt.title(fig_name + '__' + tag, fontsize=15)
        plt.savefig(saveloc)
        plt.close()

    def VentWavePlots(self, s_F, s_P, s_V, save_name):
        pass

    def LinePlot(self):
        pass

    def ViolinPlot(self, *args):
        pass

    def RocPlot(self, *args):
        pass