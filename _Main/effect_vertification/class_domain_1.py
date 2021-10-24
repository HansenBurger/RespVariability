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


class DomainHRA(DomainBasic):
    def __init__(self):
        super().__init__()
        self.__RR_s = {}
        self.__V_T_s = {}
        self.__VE_s = {}
        self.__wob_s = {}
        self.__rsbi_s = {}

    @property
    def RR_s(self):
        return self.__RR_s

    @RR_s.setter
    def RR_s(self, dict_):
        self.__RR_s = dict_

    @property
    def V_T_s(self):
        return self.__V_T_s

    @V_T_s.setter
    def V_T_s(self, dict_):
        self.__V_T_s = dict_

    @property
    def VE_s(self):
        return self.__VE_s

    @VE_s.setter
    def VE_s(self, dict_):
        self.__VE_s = dict_

    @property
    def wob_s(self):
        return self.__wob_s

    @wob_s.setter
    def wob_s(self, dict_):
        self.__wob_s = dict_

    @property
    def rsbi_s(self):
        return self.__rsbi_s

    @rsbi_s.setter
    def rsbi_s(self, dict_):
        self.__rsbi_s = dict_