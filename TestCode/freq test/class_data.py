class basic():
    def __init__(self) -> None:
        pass


class Data(basic):
    def __init__(self):
        super().__init__()
        self.__df = None
        self.__record_0 = None
        self.__record_1 = None
        self.__targets = None

    def pid_statement(self, pid):
        statement = '''
        SELECT * FROM Records_half_h_PSV
        WHERE PID={0}
        '''.format(pid)
        return statement

    def records_loc(self):
        loc = r'C:\Main\Data\_\Baguan\Records'
        return loc

    def db_loc(self):
        loc = r'C:\Main\Data\_\Database\sqlite\RespData_2201.db'
        return loc

    def table_info(self, type):
        dict_ = {
            'time_col': ['REC_t', 'Extube_t', 'SBT_time'],
            'col_map': {
                'PID': 'PID',
                'ICU': 'ICU',
                'Record_id': 'RID',
                'Resp_t': 'REC_t',
                'zdt_1': 'zdt',
                'zpx_1': 'zpx',
                'endo_t': 'Extube_t',
                'endo_end': 'Extube_end',
                'machine': 'machine',
                'vent_t': 'vent_t',
                'vent_m_0': 'vent_m_0',
                'vent_m_1': 'vent_m_1',
                'vent_m_2': 'vent_m_2',
                'st_peep': 'st_peep',
                'st_ps': 'st_ps',
                'st_e_sens': 'st_e_sens',
                'st_sumP': 'st_sumP'
            }
        }
        return dict_[type]

    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, v):
        self.__df = v

    @property
    def record_0(self):
        return self.__record_0

    @record_0.setter
    def record_0(self, v):
        self.__record_0 = v

    @property
    def record_1(self):
        return self.__record_1

    @record_1.setter
    def record_1(self, v):
        self.__record_1 = v

    @property
    def targets(self):
        return self.__targets

    @targets.setter
    def targets(self, v):
        self.__targets = v


class Target(basic):
    def __init__(self):
        super().__init__()
        self.__resp_t = []
        self.__rr = []
        self.__v_t = []
        self.__mv = []
        self.__rsbi = []
        self.__wob = []
        self.__mp_jl_d = 0
        self.__mp_jm_d = 0
        self.__mp_jl_t = 0
        self.__mp_jm_t = 0

    @property
    def resp_t(self):
        return self.__resp_t

    @resp_t.setter
    def resp_t(self, list_):
        self.__resp_t = list_

    @property
    def rr(self):
        return self.__rr

    @rr.setter
    def rr(self, list_):
        self.__rr = list_

    @property
    def v_t(self):
        return self.__v_t

    @v_t.setter
    def v_t(self, list_):
        self.__v_t = list_

    @property
    def mv(self):
        return self.__mv

    @mv.setter
    def mv(self, list_):
        self.__mv = list_

    @property
    def rsbi(self):
        return self.__rsbi

    @rsbi.setter
    def rsbi(self, list_):
        self.__rsbi = list_

    @property
    def wob(self):
        return self.__wob

    @wob.setter
    def wob(self, list_):
        self.__wob = list_

    @property
    def mp_jm_d(self):
        return self.__mp_jm_d

    @mp_jm_d.setter
    def mp_jm_d(self, v):
        self.__mp_jm_d = v

    @property
    def mp_jl_d(self):
        return self.__mp_jl_d

    @mp_jl_d.setter
    def mp_jl_d(self, v):
        self.__mp_jl_d = v

    @property
    def mp_jm_t(self):
        return self.__mp_jm_t

    @mp_jm_t.setter
    def mp_jm_t(self, v):
        self.__mp_jm_t = v

    @property
    def mp_jl_t(self):
        return self.__mp_jl_t

    @mp_jl_t.setter
    def mp_jl_t(self, v):
        self.__mp_jl_t = v