class DomainBasic():
    def __init__(self) -> None:
        pass


class DomainTimeSeries(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__RR = 0
        self.__V_T = 0
        self.__VE = 0
        self.__wob = 0
        self.__rsbi = 0
        self.__mp_jl = 0
        self.__mp_jm = 0

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

    @property
    def mp_jm(self):
        return self.__mp_jm

    @mp_jm.setter
    def mp_jm(self, v):
        self.__mp_jm = v

    @property
    def mp_jl(self):
        return self.__mp_jl

    @mp_jl.setter
    def mp_jl(self, v):
        self.__mp_jl = v


class DomainNonlinear(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__RR = 0
        self.__V_T = 0
        self.__VE = 0
        self.__wob = 0
        self.__rsbi = 0
        self.__mp_jl = 0
        self.__mp_jm = 0

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

    @property
    def mp_jm(self):
        return self.__mp_jm

    @mp_jm.setter
    def mp_jm(self, v):
        self.__mp_jm = v

    @property
    def mp_jl(self):
        return self.__mp_jl

    @mp_jl.setter
    def mp_jl(self, v):
        self.__mp_jl = v
