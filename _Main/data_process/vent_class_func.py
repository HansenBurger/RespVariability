import pandas as pd


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

    def TransmitValue(self):
        self.__obj2.pid = self.__ExtractValue(self.__obj1.pid_s)
        self.__obj2.icu = self.__ExtractValue(self.__obj1.icu_s)
        self.__obj2.end_state = self.__ExtractValue(self.__obj1.ending_s)
        self.__obj2.machine = self.__ExtractValue(self.__obj1.machine_s)
        self.__obj2.end_time = self.__obj1.resp_t_s.iloc[-1]
        self.__obj2.mode_list = self.__ExtractVentmode()


class TableQuery(FuncBasic):
    def __init__(self, df_1, df_2):
        super().__init__()
        self.__df1 = df_1
        self.__df2 = df_2
        self.df = None
        self.__index = []

    def __PSVFilter(self, series):
        mode = ['CPAP', 'SPONT']
        filt = series.str.contains(mode[0]) | series.str.contains(mode[1])
        return filt

    def __ColnameGenerate(self, v_list):
        pass

    def TableFilt(self, colname_list):
        filt_0 = self.__PSVFilter(self.__df2[colname_list[0]])
        filt_1 = self.__PSVFilter(self.__df2[colname_list[1]])
        filt_2 = self.__PSVFilter(self.__df2[colname_list[2]])
        self.__df2 = self.__df2.loc[filt_0 & filt_1 & filt_2]
        pass

    def ConcatQuery(self, colname_list):

        gp_1 = pd.DataFrame.groupby(self.__df1, colname_list[0])
        gp_2 = pd.DataFrame.groupby(self.__df2, colname_list[0])

        for pid in self.__df2[colname_list[0]].unique().tolist():

            df_main = gp_1.get_group(pid)
            df_depend = gp_2.get_group(pid)

            filt = df_main[colname_list[1]].isin(df_depend[colname_list[2]])
            df_main = df_main.loc[filt]

            if not df_main.empty:
                self.__index.append(df_main.index[0])

            del df_main, df_depend, filt

        del gp_1, gp_2

        self.df = self.__df1.iloc[self.__index]
        self.df = self.df.reset_index(drop=True)
        pass