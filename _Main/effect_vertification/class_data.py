class DataBasic():
    def __init__(self) -> None:
        pass


class DataStatic(DataBasic):
    def __init__(self):
        super().__init__()

        self.file_loc_dict = {
            'main table': {
                'category': 'FormRoute',
                'name': 'ProcessForm'
            },
            'data folder': {
                'category': 'SampleDataRoute',
                'name': 'FiltedData'
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

        self.table_col_map = {
            'patient ID': 'PID',
            'record time': 'Resp_t',
            'record ID': 'Resp_id',
            'zdt name': 'zdt_1',
            'zpx name': 'zpx_1',
            'exTube end': 'endo_end'
        }

        self.time_col_name = [
            'Resp_t', 'end_time', 'Heart_t', 'endo_t', 'SBT_time'
        ]

        self.output_name_map = {
            'machine name': 'machineType',
            'sample rate': 'RefSampleRate',
            'para data index': 'uiDataIndex',
            'sampling sites': 0,
            'flowrate': 2,
            'pressure': 3,
            'volume': 4,
        }


class DataDynamic(DataBasic):
    def __init__(self):
        super().__init__()
        self.__df = None
        self.__save_form_loc = ''
        self.__save_graph_loc = ''
        self.__result_list = []
        self.__objlist_table = []
        self.__objlist_record = []
        self.__objlist_result = []

    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, df):
        self.__df = df

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
    def result_list(self):
        return self.__result_list

    @result_list.setter
    def result_list(self, list_):
        self.__result_list = list_

    @property
    def objlist_table(self):
        return self.__objlist_table

    @objlist_table.setter
    def objlist_table(self, list_):
        self.__objlist_table = list_

    @property
    def objlist_record(self):
        return self.__objlist_record

    @objlist_record.setter
    def objlist_record(self, list_):
        self.__objlist_record = list_

    @property
    def objlist_result(self):
        return self.__objlist_result

    @objlist_result.setter
    def objlist_result(self, list_):
        self.__objlist_result = list_


class DomainTable(DataBasic):
    def __init__(self):
        super().__init__()
        self.__pid = ''
        self.__time = ''
        self.__rid = ''
        self.__zdt = ''
        self.__zpx = ''
        self.__end = ''

    @property
    def pid(self):
        return self.__pid

    @pid.setter
    def pid(self, v):
        self.__pid = v

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, v):
        self.__time = v

    @property
    def rid(self):
        return self.__rid

    @rid.setter
    def rid(self, v):
        self.__rid = v

    @property
    def zdt(self):
        return self.__zdt

    @zdt.setter
    def zdt(self, v):
        self.__zdt = v

    @property
    def zpx(self):
        return self.__zpx

    @zpx.setter
    def zpx(self, v):
        self.__zpx = v

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, v):
        self.__end = v


class DomainRecord(DataBasic):
    def __init__(self):
        super().__init__()
        self.__zif_loc = ''
        self.__zdt_loc = ''
        self.__zpx_loc = ''
        self.__machine = ''
        self.__sample_rate = ''
        self.__p_list = []
        self.__p_start = []
        self.__p_end = []
        self.__s_F = []
        self.__s_P = []
        self.__s_V = []
        self.__objlist_resp = []
        self.__obj_average = None
        self.__obj_standev = None

    @property
    def zif_loc(self):
        return self.__zif_loc

    @zif_loc.setter
    def zif_loc(self, v):
        self.__zif_loc = v

    @property
    def zdt_loc(self):
        return self.__zdt_loc

    @zdt_loc.setter
    def zdt_loc(self, v):
        self.__zdt_loc = v

    @property
    def zpx_loc(self):
        return self.__zpx_loc

    @zpx_loc.setter
    def zpx_loc(self, v):
        self.__zpx_loc = v

    @property
    def machine(self):
        return self.__machine

    @machine.setter
    def machine(self, v):
        self.__machine = v

    @property
    def sample_rate(self):
        return self.__sample_rate

    @sample_rate.setter
    def sample_rate(self, v):
        self.__sample_rate = v

    @property
    def p_list(self):
        return self.__p_list

    @p_list.setter
    def p_list(self, list_):
        self.__p_list = list_

    @property
    def p_start(self):
        return self.__p_start

    @p_start.setter
    def p_start(self, list_):
        self.__p_start = list_

    @property
    def p_end(self):
        return self.__p_end

    @p_end.setter
    def p_end(self, list_):
        self.__p_end = list_

    @property
    def s_F(self):
        return self.__s_F

    @s_F.setter
    def s_F(self, list_):
        self.__s_F = list_

    @property
    def s_P(self):
        return self.__s_P

    @s_P.setter
    def s_P(self, list_):
        self.__s_P = list_

    @property
    def s_V(self):
        return self.__s_V

    @s_V.setter
    def s_V(self, list_):
        self.__s_V = list_

    @property
    def objlist_resp(self):
        return self.__objlist_resp

    @objlist_resp.setter
    def objlist_resp(self, list_):
        self.__objlist_resp = list_

    @property
    def obj_average(self):
        return self.__obj_average

    @obj_average.setter
    def obj_average(self, v):
        self.__obj_average = v

    @property
    def obj_standev(self):
        return self.__obj_standev

    @obj_standev.setter
    def obj_standev(self, v):
        self.__obj_standev = v


class DomainResp(DataBasic):
    def __init__(self):
        super().__init__()
        self.__RR = 0
        self.__V_T_i = 0
        self.__V_T_e = 0
        self.__VE = 0
        self.__wob = 0
        self.__wob_a = 0
        self.__wob_b = 0
        self.__mp_area = 0
        self.__mp_formula = 0
        self.__rsbi = 0

    @property
    def RR(self):
        return self.__RR

    @RR.setter
    def RR(self, v):
        self.__RR = v

    @property
    def V_T_i(self):
        return self.__V_T_i

    @V_T_i.setter
    def V_T_i(self, v):
        self.__V_T_i = v

    @property
    def V_T_e(self):
        return self.__V_T_e

    @V_T_e.setter
    def V_T_e(self, v):
        self.__V_T_e = v

    @property
    def VE(self):
        return self.__VE

    @VE.setter
    def VE(self, v):
        self.__VE = v

    @property
    def wob(self):
        return self.__wob

    @wob.setter
    def wob(self, v):
        self.__wob = v

    @property
    def rsbi(self):
        return self.__rsbi

    @rsbi.setter
    def rsbi(self, v):
        self.__rsbi = v


class DomainAverage(DataBasic):
    def __init__(self):
        super().__init__()
        self.__RR = 0
        self.__V_T = 0
        self.__VE = 0
        self.__wob = 0
        self.__rsbi = 0

    @property
    def RR(self):
        return self.__RR

    @RR.setter
    def RR(self, v):
        self.__RR = v

    @property
    def V_T(self):
        return self.__V_T

    @V_T.setter
    def V_T(self, v):
        self.__V_T = v

    @property
    def VE(self):
        return self.__VE

    @VE.setter
    def VE(self, v):
        self.__VE = v

    @property
    def wob(self):
        return self.__wob

    @wob.setter
    def wob(self, v):
        self.__wob = v

    @property
    def rsbi(self):
        return self.__rsbi

    @rsbi.setter
    def rsbi(self, v):
        self.__rsbi = v


class DomainStanDev(DataBasic):
    def __init__(self):
        super().__init__()
        self.__RR = 0
        self.__V_T = 0
        self.__VE = 0
        self.__wob = 0
        self.__rsbi = 0

    @property
    def RR(self):
        return self.__RR

    @RR.setter
    def RR(self, v):
        self.__RR = v

    @property
    def V_T(self):
        return self.__V_T

    @V_T.setter
    def V_T(self, v):
        self.__V_T = v

    @property
    def VE(self):
        return self.__VE

    @VE.setter
    def VE(self, v):
        self.__VE = v

    @property
    def wob(self):
        return self.__wob

    @wob.setter
    def wob(self, v):
        self.__wob = v

    @property
    def rsbi(self):
        return self.__rsbi

    @rsbi.setter
    def rsbi(self, v):
        self.__rsbi = v