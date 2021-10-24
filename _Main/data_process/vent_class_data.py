class DataBasic():
    def __init__(self) -> None:
        pass


class DataStatic(DataBasic):
    def __init__(self):
        super().__init__()
        self.file_loc_dict = {
            'main table': {
                'category': 'FormRoute',
                'name': 'FiltedForm_with'
            },
            'save form': {
                'category': 'ResultRoute',
                'name': 'FormFolder_new'
            },
            'save graph': {
                'category': 'ResultRoute',
                'name': 'GraphFolder'
            }
        }

        self.time_col = ['Resp_t', 'end_time', 'Heart_t', 'endo_t', 'SBT_time']

        self.table_col_map = {
            'patient ID': 'PID',
            'ICU info': 'ICU',
            'record time': 'Resp_t',
            'exTube time': 'endo_t',
            'exTube end': 'endo_end',
            'venting time': 'vent_t',
            'machine type': 'machine',
            'vent m bin': 'vent_m_0',
            'vent m mid': 'vent_m_1',
            'vent m end': 'vent_m_2',
            'PEEP setting': 'st_peep',
            'PS setting': 'st_ps',
            'PEEP + PS': 'st_sumP'
        }

        self.save_table_name = {
            '30min vm distri': 'Every30min_st_vm',
            '30min peep distri': 'Every30min_st_peep',
            '30min ps distri': 'Every30min_st_ps',
            '30min sumP distri': 'Every30min_st_sumP',
            'result: 1h\'s sumP10+PSV filt': 'Records_1h_sumP10_PSV',
            'result: 1h\'s sumP12+PSV filt': 'Records_1h_sumP12_PSV',
            'table result filted': 'records_pro_1h_ExTube',
            'table result filted c': 'records_pro_1h_ExTube_c'
        }

    pass


class PIDGPObj(DataBasic):
    def __init__(self):
        super().__init__()
        self.__df = None
        self.__pid_s = []
        self.__icu_s = []
        self.__resp_t_s = []
        self.__endo_t_s = []
        self.__ending_s = []
        self.__still_t_s = []
        self.__machine_s = []
        self.__vtm_0_s = []
        self.__vtm_1_s = []
        self.__vtm_2_s = []
        self.__st_peep_s = []
        self.__st_ps_s = []
        self.__st_sumP_s = []

    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, df):
        self.__df = df

    @property
    def pid_s(self):
        return self.__pid_s

    @pid_s.setter
    def pid_s(self, series):
        self.__pid_s = series

    @property
    def icu_s(self):
        return self.__icu_s

    @icu_s.setter
    def icu_s(self, series):
        self.__icu_s = series

    @property
    def resp_t_s(self):
        return self.__resp_t_s

    @resp_t_s.setter
    def resp_t_s(self, series):
        self.__resp_t_s = series

    @property
    def resp_t_s(self):
        return self.__resp_t_s

    @resp_t_s.setter
    def resp_t_s(self, series):
        self.__resp_t_s = series

    @property
    def endo_t_s(self):
        return self.__endo_t_s

    @endo_t_s.setter
    def endo_t_s(self, series):
        self.__endo_t_s = series

    @property
    def ending_s(self):
        return self.__ending_s

    @ending_s.setter
    def ending_s(self, series):
        self.__ending_s = series

    @property
    def still_t_s(self):
        return self.__still_t_s

    @still_t_s.setter
    def still_t_s(self, series):
        self.__still_t_s = series

    @property
    def machine_s(self):
        return self.__machine_s

    @machine_s.setter
    def machine_s(self, series):
        self.__machine_s = series

    @property
    def machine_s(self):
        return self.__machine_s

    @machine_s.setter
    def machine_s(self, series):
        self.__machine_s = series

    @property
    def vtm_0_s(self):
        return self.__vtm_0_s

    @vtm_0_s.setter
    def vtm_0_s(self, series):
        self.__vtm_0_s = series

    @property
    def vtm_1_s(self):
        return self.__vtm_1_s

    @vtm_1_s.setter
    def vtm_1_s(self, series):
        self.__vtm_1_s = series

    @property
    def vtm_2_s(self):
        return self.__vtm_2_s

    @vtm_2_s.setter
    def vtm_2_s(self, series):
        self.__vtm_2_s = series

    @property
    def st_peep_s(self):
        return self.__st_peep_s

    @st_peep_s.setter
    def st_peep_s(self, series):
        self.__st_peep_s = series

    @property
    def st_ps_s(self):
        return self.__st_ps_s

    @st_ps_s.setter
    def st_ps_s(self, series):
        self.__st_ps_s = series

    @property
    def st_sumP_s(self):
        return self.__st_sumP_s

    @st_sumP_s.setter
    def st_sumP_s(self, series):
        self.__st_sumP_s = series


class PIDInfoObj(DataBasic):
    def __init__(self):
        super().__init__()
        self.__pid = ''
        self.__icu = ''
        self.__end_state = ''
        self.__end_time = ''
        self.__machine = ''
        self.__mode_list = []
        self.__st_peep_list = []
        self.__st_ps_list = []
        self.__st_sumP_list = []

    @property
    def pid(self):
        return self.__pid

    @pid.setter
    def pid(self, v):
        self.__pid = v

    @property
    def icu(self):
        return self.__icu

    @icu.setter
    def icu(self, v):
        self.__icu = v

    @property
    def end_state(self):
        return self.__end_state

    @end_state.setter
    def end_state(self, v):
        self.__end_state = v

    @property
    def end_time(self):
        return self.__end_time

    @end_time.setter
    def end_time(self, v):
        self.__end_time = v

    @property
    def machine(self):
        return self.__machine

    @machine.setter
    def machine(self, v):
        self.__machine = v

    @property
    def mode_list(self):
        return self.__mode_list

    @mode_list.setter
    def mode_list(self, list_):
        self.__mode_list = list_

    @property
    def st_peep_list(self):
        return self.__st_peep_list

    @st_peep_list.setter
    def st_peep_list(self, list_):
        self.__st_peep_list = list_

    @property
    def st_ps_list(self):
        return self.__st_ps_list

    @st_ps_list.setter
    def st_ps_list(self, list_):
        self.__st_ps_list = list_

    @property
    def st_sumP_list(self):
        return self.__st_sumP_list

    @st_sumP_list.setter
    def st_sumP_list(self, list_):
        self.__st_sumP_list = list_


class DataDynamic(DataBasic):
    def __init__(self):
        super().__init__()
        self.__df_main = None
        self.__df_basic = None
        self.__df_s_para = {}
        self.__save_form_loc = ''
        self.__save_graph_loc = ''
        self.__objlist_table = []
        self.__objlist_pinfo = []

    @property
    def df_main(self):
        return self.__df_main

    @df_main.setter
    def df_main(self, df):
        self.__df_main = df

    @property
    def df_basic(self):
        return self.__df_basic

    @df_basic.setter
    def df_basic(self, df):
        self.__df_basic = df

    @property
    def df_s_para(self):
        return self.__df_s_para

    @df_s_para.setter
    def df_s_para(self, dict_):
        self.__df_s_para = dict_

    @property
    def save_form_loc(self):
        return self.__save_form_loc

    @save_form_loc.setter
    def save_form_loc(self, v):
        self.__save_form_loc = v

    @property
    def save_graph_loc(self):
        return self.__save_graph_loc

    @save_graph_loc.setter
    def save_graph_loc(self, v):
        self.__save_graph_loc = v

    @property
    def objlist_table(self):
        return self.__objlist_table

    @objlist_table.setter
    def objlist_table(self, list_):
        self.__objlist_table = list_

    @property
    def objlist_pinfo(self):
        return self.__objlist_pinfo

    @objlist_pinfo.setter
    def objlist_pinfo(self, list_):
        self.__objlist_pinfo = list_