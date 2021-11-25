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
        self.__obj_ts = None
        self.__obj_hra = None
        self.__obj_hrv = None

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
    def obj_ts(self):
        return self.__obj_ts

    @obj_ts.setter
    def obj_ts(self, v):
        self.__obj_ts = v

    @property
    def obj_hra(self):
        return self.__obj_hra

    @obj_hra.setter
    def obj_hra(self, v):
        self.__obj_hra = v

    @property
    def obj_hrv(self):
        return self.__obj_hrv

    @obj_hrv.setter
    def obj_hrv(self, v):
        self.__obj_hrv = v


class DomainAggr_Time(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__pid = ''
        self.__end = 0
        self.__ave = None
        self.__std = None

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
    def ave(self):
        return self.__ave

    @ave.setter
    def ave(self, v):
        self.__ave = v

    @property
    def std(self):
        return self.__std

    @std.setter
    def std(self, v):
        self.__std = v

    @property
    def cv(self):
        return self.__cv

    @cv.setter
    def cv(self, v):
        self.__cv = v


class DomainAggr_Freq(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__pid = ''
        self.__end = 0

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


class DomainAggr_NonL(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__pid = ''
        self.__end = 0
        self.__hra_pi = None
        self.__hra_gi = None
        self.__hra_si = None
        self.__hrv_sd1 = None
        self.__hrv_sd2 = None

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
    def hra_pi(self):
        return self.__hra_pi

    @hra_pi.setter
    def hra_pi(self, v):
        self.__hra_pi = v

    @property
    def hra_gi(self):
        return self.__hra_gi

    @hra_gi.setter
    def hra_gi(self, v):
        self.__hra_gi = v

    @property
    def hra_si(self):
        return self.__hra_si

    @hra_si.setter
    def hra_si(self, v):
        self.__hra_si = v

    @property
    def hrv_sd1(self):
        return self.__hrv_sd1

    @hrv_sd1.setter
    def hrv_sd1(self, v):
        self.__hrv_sd1 = v

    @property
    def hrv_sd2(self):
        return self.__hrv_sd2

    @hrv_sd2.setter
    def hrv_sd2(self, v):
        self.__hrv_sd2 = v
