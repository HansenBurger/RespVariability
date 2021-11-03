import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import timedelta


class FuncBasic():
    def __init__(self) -> None:
        pass


class Certify(FuncBasic):
    def __init__(self, obj):
        super().__init__()
        self.__obj = obj

    def __PSVFilter(self, series):
        mode = ['CPAP', 'SPONT']
        filt = series.str.contains(mode[0]) | series.str.contains(mode[1])
        return filt

    def __UpperFilter(self):
        filt = self.__obj.resp_t_s <= self.__obj.endo_t_s
        return filt

    def __LowerFilter(self):
        filt = self.__obj.resp_t_s > self.__obj.endo_t_s
        return filt

    def EndtimeCertify(self):
        df_up = self.__obj.df[self.__UpperFilter()]
        df_down = self.__obj.df[self.__LowerFilter()]

        df_down = df_down.loc[self.__PSVFilter(self.__obj.vtm_0_s)
                              | self.__PSVFilter(self.__obj.vtm_1_s)
                              | self.__PSVFilter(self.__obj.vtm_2_s)]

        self.__obj.df = pd.concat(
            [df_up, df_down],
            ignore_index=True) if not df_down.empty else df_up

        if self.__obj.df.empty:
            print('PID: ',
                  self.__obj.pid_s.unique()[0], 'find no match records')


class Transmit(FuncBasic):
    def __init__(self, obj_1, obj_2):
        super().__init__()
        self.__obj1 = obj_1
        self.__obj2 = obj_2

    def __ExtractValue(self, series):
        spacer = '_'
        if len(series.unique()) > 1:
            return spacer.join(series.unique().tolist())
        else:
            return series.unique().item()

    def __ExtractSetting(self, series):
        gap_tag = '/'
        st_result = []

        for i in self.__obj1.df.index:

            st_content = series.loc[i].split(gap_tag)
            st_end_loc = self.__obj1.df.index[-1]
            st_tmp_list = st_content if i == st_end_loc else st_content[1:]
            st_result.extend(st_tmp_list)

        st_result.reverse()

        return st_result

    def __ExtractVentmode(self):
        vent_m_list = []

        for i in self.__obj1.df.index:

            if i != self.__obj1.df.index[-1]:
                vm_0 = self.__obj1.vtm_0_s.loc[i]
                vm_1 = self.__obj1.vtm_1_s.loc[i]
                vent_m_list.extend([vm_0, vm_1])

            else:
                vm_0 = self.__obj1.vtm_0_s.loc[i]
                vm_1 = self.__obj1.vtm_1_s.loc[i]
                vm_2 = self.__obj1.vtm_2_s.loc[i]
                vent_m_list.extend([vm_0, vm_1, vm_2])

        vent_m_list.reverse()

        return vent_m_list

    def TransmitValue_Basic(self):
        self.__obj2.pid = self.__ExtractValue(self.__obj1.pid_s)
        self.__obj2.icu = self.__ExtractValue(self.__obj1.icu_s)
        self.__obj2.end_state = self.__ExtractValue(self.__obj1.ending_s)
        self.__obj2.machine = self.__ExtractValue(self.__obj1.machine_s)
        self.__obj2.end_time = self.__obj1.resp_t_s.iloc[-1] + timedelta(
            seconds=self.__obj1.still_t_s.iloc[-1].item())

    def TransmitValue_VM(self):
        self.__obj2.mode_list = self.__ExtractVentmode()

    def TransmitValue_ST(self):
        self.__obj2.st_peep_list = self.__ExtractSetting(self.__obj1.st_peep_s)
        self.__obj2.st_ps_list = self.__ExtractSetting(self.__obj1.st_ps_s)
        self.__obj2.st_sumP_list = self.__ExtractSetting(self.__obj1.st_sumP_s)


class Charts():
    def __init__(self, df_l, df_r, info_list, save_loc):
        self.__df_l = df_l
        self.__df_r = df_r
        self.df_concat = None
        self.__info = info_list
        self.__save_loc = str(save_loc)

    def __ClassifySeriesProcess(self, colname_class):
        colvalue_map = {'成功': 0, '失败': 1}
        df = self.df_concat.copy()

        for i in df.index:
            for key in colvalue_map.keys():
                if key in df.loc[i, colname_class]:
                    df.loc[i, colname_class] = colvalue_map[key]
                    break

        return df

    def TableBuild(self, para_list):
        para_matrix = np.array(para_list)
        para_matrix = np.transpose(para_matrix)

        for i in range(para_matrix.shape[0]):
            col_name = '_'.join(
                [self.__info[0],
                 str(i * 30).rjust(3, '0'), 'min'])
            col_value = para_matrix[i]
            self.__df_r[col_name] = col_value\

        self.df_concat = pd.concat([self.__df_l, self.__df_r], axis=1)

    def DFInfoOutput(self, colname_gp_s, colname_class):
        df = self.__ClassifySeriesProcess(colname_class)
        txt_loc = str(Path(self.__save_loc) / (self.__info[1] + '.txt'))

        with open(txt_loc, 'w') as f:

            for colname_gp in colname_gp_s:
                f.write('{0}\'s distribution info: \n'.format(colname_gp))
                gp = pd.DataFrame.groupby(df, by=colname_gp)
                gp_cat_list = df[colname_gp].unique().tolist()
                gp_cat_list = [x for x in gp_cat_list if x]  # drop none value
                gp_cat_list.sort()

                for cat in gp_cat_list:
                    df_tmp = gp.get_group(cat)
                    succ_len = df_tmp.loc[df_tmp[colname_class] == 0].shape[0]
                    fail_len = df_tmp.loc[df_tmp[colname_class] == 1].shape[0]
                    f.write('{0}: succ {1} | fail {2} \n'.format(
                        cat, succ_len, fail_len))

                f.write('\n')

    def GroupBarPlot(self, x_label_s, hue_label):
        for x_label in x_label_s:
            fig_name = x_label
            saveloc = Path(self.__save_loc) / (fig_name + '.png')
            df = self.__ClassifySeriesProcess(hue_label)
            df = df.loc[(df[x_label] != '') & (df[x_label] != None)]
            df = df.sort_values(by=[x_label])

            sns.set(rc={'figure.figsize': (13, 8)},
                    style='whitegrid',
                    font_scale=0.7)
            fx = sns.histplot(data=df,
                              x=x_label,
                              hue=hue_label,
                              hue_order=[1, 0],
                              multiple="stack",
                              shrink=.9)
            fx.set(xlabel=None, ylabel=None)
            fx.tick_params(axis='x', rotation=45)
            plt.title(fig_name, fontsize=15)
            plt.savefig(saveloc)
            plt.close()


class TableQuery(FuncBasic):
    def __init__(self, df_whole, df_list):
        super().__init__()
        self.__df1 = df_whole
        self.__df2 = pd.concat(df_list, axis=1)
        self.df = None

    def __PSVFilter(self, series):
        mode = ['CPAP', 'SPONT']
        filt = series.str.contains(mode[0]) | series.str.contains(mode[1])
        return filt

    def __SumPressureFilter(self, series):
        threshold = [10, 12, 5]
        series = series.convert_dtypes()
        series = series.astype('int32')
        filt_0 = (series <= threshold[0]) & (series >= threshold[2])
        filt_1 = (series <= threshold[1]) & (series >= threshold[2])
        return {'sum_10': filt_0, 'sum_12': filt_1}

    def __PeepFilter(self, series):
        threshold = 10
        series = series.dropna()
        series = series.convert_dtypes()
        series = series.astype('int32')
        filt = series < threshold
        return filt

    def TableFilt_PSV(self, colname_list):
        df = self.__df2
        for col in colname_list:
            filt = self.__PSVFilter(df[col])
            df = df.loc[filt]
        self.__df2 = df

    def TableFilt_SumP(self, colname_list, filt_mode):
        df = self.__df2
        for col in colname_list:
            filt = self.__SumPressureFilter(df[col])[filt_mode]
            df = df.loc[filt]
        self.__df2 = df

    def TableFilt_InvalidPeep(self, colname_list):
        df = self.__df2
        threshold = 10
        index_list = []
        for i in df.index:
            series = df.loc[i, colname_list]
            list_ = [x for x in series.tolist() if x]
            if all(int(value) >= threshold for value in list_):
                index_list.append(i)
        df = df.iloc[index_list]
        self.__df2 = df

    def ConcatQueryByTime(self, col_pid, hour_set=None):
        gp = pd.DataFrame.groupby(self.__df1, col_pid)

        for pid in self.__df2[col_pid].unique().tolist():
            df_tmp = gp.get_group(pid)
            if hour_set:
                df_tmp_ = df_tmp.iloc[::-1][:hour_set]
                if not df_tmp_.empty and df_tmp_.shape[0] == hour_set:
                    self.df = pd.concat([self.df, df_tmp_],
                                        axis=0,
                                        ignore_index=True)
            else:
                self.df = pd.concat([self.df, df_tmp],
                                    axis=0,
                                    ignore_index=True)

        self.df = self.df.reset_index(drop=True)