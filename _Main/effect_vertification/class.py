import sys, pathlib

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code.Fundal import BinImport


class Static:

    sample_dict = {}
    __total_success = 0
    __total_failure = 0

    def __init__(self):
        pass


class Record(Static):
    def __init__(self, zif_loc):
        self.zif_loc = zif_loc
