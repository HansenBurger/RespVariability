class DomainBasic():
    def __init__(self) -> None:
        pass


class DomainResp(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__RR = 0
        self.__V_T_i = 0
        self.__V_T_e = 0
        self.__VE = 0
        self.__wob = 0
        self.__wob_a = 0
        self.__wob_b = 0
        self.__mp_jm = 0
        self.__mp_jl = 0
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
    def wob_a(self):
        return self.__wob_a

    @wob_a.setter
    def wob_a(self, v):
        self.__wob_a = v

    @property
    def wob_b(self):
        return self.__wob_b

    @wob_b.setter
    def wob_b(self, v):
        self.__wob_b = v

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

    @property
    def rsbi(self):
        return self.__rsbi

    @rsbi.setter
    def rsbi(self, v):
        self.__rsbi = v


class DomainAverage(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__RR = 0
        self.__V_T = 0
        self.__VE = 0
        self.__wob = 0
        self.__rsbi = 0
        self.__mp_jm = 0
        self.__mp_jl = 0

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


class DomainStanDev(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__RR = 0
        self.__V_T = 0
        self.__VE = 0
        self.__wob = 0
        self.__rsbi = 0
        self.__mp_jm = 0
        self.__mp_jl = 0

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


class DomainTS(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__ave = None
        self.__std = None
        self.__cv = None

    @property
    def ave(self):
        return self.__ave

    @ave.setter
    def ave(self, obj):
        self.__ave = obj

    @property
    def std(self):
        return self.__std

    @std.setter
    def std(self, obj):
        self.__std = obj

    @property
    def cv(self):
        return self.__cv

    @cv.setter
    def cv(self, obj):
        self.__cv = obj


class DomainHRA(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__pi = None
        self.__gi = None
        self.__si = None

    @property
    def pi(self):
        return self.__pi

    @pi.setter
    def pi(self, obj):
        self.__pi = obj

    @property
    def gi(self):
        return self.__gi

    @gi.setter
    def gi(self, obj):
        self.__gi = obj

    @property
    def si(self):
        return self.__si

    @si.setter
    def si(self, obj):
        self.__si = obj


class DomainHRV(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__sd1 = None
        self.__sd2 = None

    @property
    def sd1(self):
        return self.__sd1

    @sd1.setter
    def sd1(self, obj):
        self.__sd1 = obj

    @property
    def sd2(self):
        return self.__sd2

    @sd2.setter
    def sd2(self, obj):
        self.__sd2 = obj
