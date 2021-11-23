import re


class DataBasic():
    def __init__(self) -> None:
        pass


class DataStatic(DataBasic):
    def __init__(self):
        super().__init__()
        self.file_loc_dict = {
            'main table': {
                'category': 'FormRoute',
                'name': 'FiltedForm'
            },
            'data folder': {
                'category': 'SampleDataRoute',
                'name': 'FiltedData'
            },
            'save_form': {
                'category': 'ResultRoute',
                'name': 'FormFolder'
            }
        }

        self.time_col = ['Resp_t', 'end_time', 'Heart_t', 'endo_t', 'SBT_time']

        self.table_col_map = {
            'record time': 'Resp_t',
            'record ID': 'Resp_id',
            'zdt name': 'zdt_1',
            'zpx name': 'zpx_1',
        }

        self.output_name_map = {
            'machine name': 'machineType',
            'sample rate': 'RefSampleRate',
            'para index': 'uiDataIndex',
            'vent type': 'st_VENT_TYPE',
            'vent mode': 'st_VENT_MODE',
            'mand type': 'st_MAND_TYPE',
            'PEEP setting': 'st_PEEP',
            'PS setting': 'st_P_SUPP',
            'ESENS setting': 'st_E_SENS',
            'start index': 0,
            'flow index': 2
        }

        self.result_name_map = {
            'ICU': 'ICU',
            'machine type': 'machine',
            'vent m bin': 'vent_m_0',
            'vent m mid': 'vent_m_1',
            'vent m end': 'vent_m_2',
            'still time': 'vent_t',
            'peep setting': 'st_peep',
            'ps setting': 'st_ps',
            'esens setting': 'st_e_sens',
            'peep + ps': 'st_sumP'
        }

        self.save_table_name = {
            'result full': 'record_check_f',
            'result shrink': 'record_check_s'
        }


class DomainTable(DataBasic):
    def __init__(self):
        super().__init__()
        self.__row = 0
        self.__time = ''
        self.__rid = ''
        self.__zdt = ''
        self.__zpx = ''

    @property
    def row(self):
        return self.__row

    @row.setter
    def row(self, v):
        self.__row = v

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, v):
        self.__time = v

    @time.deleter
    def time(self):
        del self.__time

    @property
    def rid(self):
        return self.__rid

    @rid.setter
    def rid(self, v):
        self.__rid = v

    @rid.deleter
    def rid(self):
        del self.__rid

    @property
    def zdt(self):
        return self.__zdt

    @zdt.setter
    def zdt(self, v):
        self.__zdt = v

    @zdt.deleter
    def zdt(self):
        del self.__zdt

    @property
    def zpx(self):
        return self.__zpx

    @zpx.setter
    def zpx(self, v):
        self.__zpx = v

    @zpx.deleter
    def zpx(self):
        del self.__zpx


class DomainRecord(DataBasic):
    def __init__(self):
        super().__init__()
        self.__zif_loc = ''
        self.__zdt_loc = ''
        self.__zpx_loc = ''
        self.__machine = ''
        self.__sample_rate = ''
        self.__start_ind = []
        self.__s_F = []
        self.__para_ind = []  # keep np array
        self.__st_peep = []
        self.__st_ps = []
        self.__st_e_sens = []
        self.__vent_type = []
        self.__vent_mode = []
        self.__mand_type = []

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
    def start_ind(self):
        return self.__start_ind

    @start_ind.setter
    def start_ind(self, list_):
        self.__start_ind = list_

    @start_ind.deleter
    def start_ind(self):
        del self.__start_ind

    @property
    def s_F(self):
        return self.__s_F

    @s_F.setter
    def s_F(self, list_):
        self.__s_F = list_

    @property
    def para_ind(self):
        return self.__para_ind

    @para_ind.setter
    def para_ind(self, list_):
        self.__para_ind = list_

    @para_ind.deleter
    def para_ind(self):
        del self.__para_ind

    @property
    def st_peep(self):
        return self.__st_peep

    @st_peep.setter
    def st_peep(self, list_):
        self.__st_peep = list_

    @property
    def st_ps(self):
        return self.__st_ps

    @st_ps.setter
    def st_ps(self, list_):
        self.__st_ps = list_

    @property
    def st_e_sens(self):
        return self.__st_e_sens

    @st_e_sens.setter
    def st_e_sens(self, list_):
        self.__st_e_sens = list_

    @property
    def vent_type(self):
        return self.__vent_type

    @vent_type.setter
    def vent_type(self, list_):
        self.__vent_type = list_

    @vent_type.deleter
    def vent_type(self):
        del self.__vent_type

    @property
    def vent_mode(self):
        return self.__vent_mode

    @vent_mode.setter
    def vent_mode(self, list_):
        self.__vent_mode = list_

    @vent_mode.deleter
    def vent_mode(self):
        del self.__vent_mode

    @property
    def mand_type(self):
        return self.__mand_type

    @mand_type.setter
    def mand_type(self, list_):
        self.__mand_type = list_

    @mand_type.deleter
    def mand_type(self):
        del self.__mand_type


class DomainResult(DataBasic):
    def __init__(self):
        super().__init__()

        self.__still_time = 0
        self.__v_m_list = []
        self.__peep_list = []
        self.__ps_list = []
        self.__e_sens_list = []
        self.__sumP_list = []

    @property
    def still_time(self):
        return self.__still_time

    @still_time.setter
    def still_time(self, v):
        self.__still_time = v

    @property
    def v_m_list(self):
        return self.__v_m_list

    @v_m_list.setter
    def v_m_list(self, list_):
        self.__v_m_list = list_

    @property
    def peep_list(self):
        return self.__peep_list

    @peep_list.setter
    def peep_list(self, list_):
        self.__peep_list = list_

    @property
    def ps_list(self):
        return self.__ps_list

    @ps_list.setter
    def ps_list(self, list_):
        self.__ps_list = list_

    @property
    def e_sens_list(self):
        return self.__e_sens_list

    @e_sens_list.setter
    def e_sens_list(self, list_):
        self.__e_sens_list = list_

    @property
    def sumP_list(self):
        return self.__sumP_list

    @sumP_list.setter
    def sumP_list(self, list_):
        self.__sumP_list = list_


class DataDynamic(DataBasic):
    def __init__(self):
        super().__init__()
        self.__df = None
        self.__save_loc = ''
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
    def save_loc(self):
        return self.__save_loc

    @save_loc.setter
    def save_loc(self, v):
        self.__save_loc = v

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