class Domain:
    def __init__(self) -> None:
        pass


class Domain1(Domain):
    def __init__(self):
        super().__init__()
        self.__pid = 0
        self.__resp_id = ""
        self.__zdt_1 = ""
        self.__zpx_1 = ""
        self.__endo_end = 0

    @property
    def pid(self):
        return self.__pid

    @pid.setter
    def pid(self, num):
        self.__pid = num

    @property
    def resp_id(self):
        return self.__resp_id

    @resp_id.setter
    def resp_id(self, string):
        self.__resp_id = string

    @property
    def zdt_1(self):
        return self.__zdt_1

    @zdt_1.setter
    def zdt_1(self, string):
        self.zdt_1 = string

    @property
    def zpx_1(self):
        return self.__zpx_1

    @zpx_1.setter
    def zpx_1(self, string):
        self.zpx_1 = string

    @property
    def endo_end(self):
        return self.__endo_end

    @endo_end.setter
    def endo_end(self, bool_n):
        self.__endo_end = bool_n


class Domain2(Domain):
    def __init__(self):
        super().__init__()
        self.__p_s = []
        self.__s_F = []
        self.__s_P = []
        self.__s_V = []

    @property
    def p_s(self):
        return self.__p_s

    @p_s.setter
    def p_s(self, list_):
        self.__p_s = list_

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


class DomainAgger(Domain):
    def __init__(self):
        super().__init__()
        self.__RR = 0.0
        self.__MV = 0.0
        self.__tidal = 0.0
        self.__min_vent = 0.0

    @property
    def RR(self):
        return self.__RR

    @RR.setter
    def RR(self, v):
        self.__RR = v

    @property
    def MV(self):
        return self.__MV

    @MV.setter
    def MV(self, v):
        self.__MV = v

    @property
    def tidal(self):
        return self.__tidal

    @tidal.setter
    def tidal(self, v):
        self.__tidal = v

    @property
    def min_vent(self):
        return self.__min_vent

    @min_vent.setter
    def min_vent(self, v):
        self.__min_vent = v
