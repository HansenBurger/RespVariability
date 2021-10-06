import numpy as np


class Calculation():
    def __init__(self) -> None:
        pass

    def FirstLastDetect(self, p_1, p_2):
        min_gap = 50
        max_gap = 450
        gap = abs(p_2 - p_1)

        if gap < min_gap or gap > max_gap or gap == 0:
            return False
        else:
            return True

    def StraightLineDetect(self, array_):
        if np.array_equal(array_):
            return False
        else:
            return True


class MainCalculation(Calculation):
    def __init__(self, obj_1, obj_2):
        super().__init__()
        self.__obj1 = obj_1
        self.__obj2 = obj_2

    def __GapDetection(self, p_1, p_2):
        min_gap = 50
        max_gap = 450
        gap = abs(p_2 - p_1)

        if gap < min_gap or gap > max_gap or gap == 0:
            return False
        else:
            return True

    def __LineDetection(self, array_):
        if np.array_equal(array_):
            return False
        else:
            return True

    def RR(self):

        min_s = 60
        RR_s = []

        for i in range(len(self.__obj1.p_start)):

            p_0 = self.__obj1.p_start[i]
            p_1 = self.__obj1.p_end[i]
            f_wave = np.array(self.__obj1.s_F[p_0:p_1])

            if self.__GapDetection(p_0, p_1) and self.__LineDetection(f_wave):
                RR = min_s / ((p_1 - p_0) * 1 / self.__obj1.sample_rate)
                RR_s.append(RR)
