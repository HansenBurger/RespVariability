from os import stat_result
from pathlib import Path, PurePath
import numpy as np


class RecordFucBasic():
    def __init__(self) -> None:
        pass


class FileLocBuild(RecordFucBasic):
    def __init__(self, cwd, obj_0, obj_1):
        super().__init__()
        self.__cwd = cwd  # PATH
        self.__obj_0 = obj_0
        self.__obj_1 = obj_1

    def __Folder(self, main_loc, time_info, rid):
        parents_2 = Path(main_loc) if not isinstance(main_loc,
                                                     PurePath) else main_loc
        parents_1 = (str(time_info.year) + str(time_info.month).rjust(2, '0'))
        parents_0 = rid
        folder_loc = parents_2 / parents_1 / parents_0

        return folder_loc

    def ZifLoc(self):
        parent_loc = self.__Folder(self.__cwd, self.__obj_0.time,
                                   self.__obj_0.rid)
        self.__obj_1.zif_loc = parent_loc / (self.__obj_0.rid + '.zif')

    def ZdtLoc(self):
        parent_loc = self.__Folder(self.__cwd, self.__obj_0.time,
                                   self.__obj_0.rid)
        self.__obj_1.zdt_loc = parent_loc / (self.__obj_0.zdt + '.zdt')

    def ZpxLoc(self):
        parent_loc = self.__Folder(self.__cwd, self.__obj_0.time,
                                   self.__obj_0.rid)
        self.__obj_1.zpx_loc = parent_loc / (self.__obj_0.zpx + '.zpx')


class OutputCheck(RecordFucBasic):
    def __init__(self, obj):
        super().__init__()
        self.__obj = obj
        self.__size_min = 100

    def ZifContentCheck(self, func):
        default = None
        if self.__obj.zif_loc.stat().st_size >= self.__size_min:
            return func(self.__obj.zif_loc)
        else:
            return default

    def ZdtHeaderCheck(self, func):
        default = {}
        if self.__obj.zdt_loc.stat().st_size >= self.__size_min:
            return func(self.__obj.zdt_loc)[0]
        else:
            return default

    def ZpxParaCheck(self, func):
        default = {}
        if self.__obj.zpx_loc.stat().st_size >= self.__size_min:
            return func(self.__obj.zpx_loc)[0]
        else:
            return default

    def ZdtPointCheck(self, func):
        default = [[], [], [], [], [], 0]
        if self.__obj.zdt_loc.stat().st_size >= self.__size_min:
            return func(self.__obj.zdt_loc)
        else:
            return default


class Calculation(RecordFucBasic):
    def __init__(self, obj_0, obj_1):
        super().__init__()
        self.__obj_0 = obj_0
        self.__obj_1 = obj_1
        self.__time_tag = [0, 1800, 3600]

    def __LocatSimiTerms(self, list_main, list_depend):
        index_list = []
        for i in list_depend:
            clo_value = min(list_main, key=lambda x: abs(x - i))
            clo_index = np.where(list_main == clo_value)[0][0]
            index_list.append(clo_index)

        return index_list

    def __DelAttri(self):
        del self.__obj_0.vent_type
        del self.__obj_0.vent_mode
        del self.__obj_0.mand_type

    def VMlistBuild(self, func):
        para_index = self.__obj_0.para_ind * np.array(
            1 / self.__obj_0.sample_rate)
        para_select_indexs = self.__LocatSimiTerms(para_index, self.__time_tag)
        machine = self.__obj_0.machine
        machine_name = machine.split('-')[0]

        for i in para_select_indexs:
            vent_mode = func(machine_name, self.__obj_0.vent_type[i].item(),
                             self.__obj_0.vent_mode[i].item(),
                             self.__obj_0.mand_type[i].item())

            self.__obj_1.v_m_list.append(vent_mode)

        self.__DelAttri()

    def SetsBuild(self, st_list):
        para_index = self.__obj_0.para_ind * np.array(
            1 / self.__obj_0.sample_rate)
        para_select_indexs = self.__LocatSimiTerms(para_index, self.__time_tag)

        st_select_list = [int(st_list[i].item()) for i in para_select_indexs]
        return st_select_list

    def SetSum(self, st_list_0, st_list_1):
        st_array_0 = np.array(st_list_0)
        st_array_1 = np.array(st_list_1)
        st_result = st_array_0 + st_array_1

        return st_result.tolist()

    def VMtimeBuild(self):
        vent_still_time = round(
            self.__obj_0.start_ind[-1] * 1 /
            self.__obj_0.sample_rate) if self.__obj_0.start_ind else 0
        self.__obj_1.still_time = vent_still_time

    def FlowtimeBuild(self):
        vent_still_time = round(
            len(self.__obj_0.s_F) * 1 /
            self.__obj_0.sample_rate) if self.__obj_0.s_F else 0
        self.__obj_1.still_time = vent_still_time