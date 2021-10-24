class DomainBasic():
    def __init__(self) -> None:
        pass


class DomainTable(DomainBasic):
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


class DomainRecord(DomainBasic):
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
        self.__obj_hra = None

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

    @property
    def obj_hra(self):
        return self.__obj_hra

    @obj_hra.setter
    def obj_hra(self, v):
        self.__obj_hra = v


class DomainAggregate(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__pid = ''
        self.__end = 0
        self.__resp = None
        self.__RR_1 = 0
        self.__V_T_1 = 0
        self.__VE_1 = 0
        self.__wob_1 = 0
        self.__rsbi_1 = 0
        self.__mp_jm_1 = 0
        self.__mp_jl_1 = 0
        self.__RR_2 = 0
        self.__V_T_2 = 0
        self.__VE_2 = 0
        self.__wob_2 = 0
        self.__rsbi_2 = 0
        self.__mp_jm_2 = 0
        self.__mp_jl_2 = 0
        self.__RR_3 = {}
        self.__V_T_3 = {}
        self.__VE_3 = {}
        self.__wob_3 = {}
        self.__rsbi_3 = {}

    @property
    def pid(self):
        return self.__pid

    @pid.setter
    def pid(self, v):
        self.__pid = v

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, v):
        self.__end = v

    @property
    def resp(self):
        return self.__resp

    @resp.setter
    def resp(self, v):
        self.__resp = v

    @property
    def RR_1(self):
        return self.__RR_1

    @RR_1.setter
    def RR_1(self, v):
        self.__RR_1 = v

    @property
    def V_T_1(self):
        return self.__V_T_1

    @V_T_1.setter
    def V_T_1(self, v):
        self.__V_T_1 = v

    @property
    def VE_1(self):
        return self.__VE_1

    @VE_1.setter
    def VE_1(self, v):
        self.__VE_1 = v

    @property
    def wob_1(self):
        return self.__wob_1

    @wob_1.setter
    def wob_1(self, v):
        self.__wob_1 = v

    @property
    def rsbi_1(self):
        return self.__rsbi_1

    @rsbi_1.setter
    def rsbi_1(self, v):
        self.__rsbi_1 = v

    @property
    def mp_jm_1(self):
        return self.__mp_jm_1

    @mp_jm_1.setter
    def mp_jm_1(self, v):
        self.__mp_jm_1 = v

    @property
    def mp_jl_1(self):
        return self.__mp_jl_1

    @mp_jl_1.setter
    def mp_jl_1(self, v):
        self.__mp_jl_1 = v

    @property
    def RR_2(self):
        return self.__RR_2

    @RR_2.setter
    def RR_2(self, v):
        self.__RR_2 = v

    @property
    def V_T_2(self):
        return self.__V_T_2

    @V_T_2.setter
    def V_T_2(self, v):
        self.__V_T_2 = v

    @property
    def VE_2(self):
        return self.__VE_2

    @VE_2.setter
    def VE_2(self, v):
        self.__VE_2 = v

    @property
    def wob_2(self):
        return self.__wob_2

    @wob_2.setter
    def wob_2(self, v):
        self.__wob_2 = v

    @property
    def rsbi_2(self):
        return self.__rsbi_2

    @rsbi_2.setter
    def rsbi_2(self, v):
        self.__rsbi_2 = v

    @property
    def mp_jm_2(self):
        return self.__mp_jm_2

    @mp_jm_2.setter
    def mp_jm_2(self, v):
        self.__mp_jm_2 = v

    @property
    def mp_jl_2(self):
        return self.__mp_jl_2

    @mp_jl_2.setter
    def mp_jl_2(self, v):
        self.__mp_jl_2 = v

    @property
    def RR_3(self):
        return self.__RR_3

    @RR_3.setter
    def RR_3(self, dict_):
        self.__RR_3 = dict_

    @property
    def V_T_3(self):
        return self.__V_T_3

    @V_T_3.setter
    def V_T_3(self, dict_):
        self.__V_T_3 = dict_

    @property
    def VE_3(self):
        return self.__VE_3

    @VE_3.setter
    def VE_3(self, dict_):
        self.__VE_3 = dict_

    @property
    def wob_3(self):
        return self.__wob_3

    @wob_3.setter
    def wob_3(self, dict_):
        self.__wob_3 = dict_

    @property
    def rsbi_3(self):
        return self.__rsbi_3

    @rsbi_3.setter
    def rsbi_3(self, dict_):
        self.__rsbi_3 = dict_