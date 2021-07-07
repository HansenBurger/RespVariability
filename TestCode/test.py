from configparser import NoOptionError
from numpy.lib.function_base import percentile
import sys, os

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
print(currentdir)
print(parentdir)
# sys.path.append(parentdir)

# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from pathlib import Path
import pathlib

current_loc = Path.cwd()
print(current_loc)
print(type(pathlib.Path.cwd().parents[0]))
sys.path.append(str(current_loc.parents[0]))

from Code import InIReaWri

a = InIReaWri.ConfigR('FormRoute', 'MainDataForm', conf=None)
print(a)

# from Code.Fundal import BinImport_c
# """
#  BinImport_c test fail
# """
# from Code.Fundal import BinImport
# from Code.Fundal import ReadSamplerate as RS
# import numpy as np
# from matplotlib import pyplot as plt
# from Code import PointProcess as PP

# zdt_loc = r"Data\Sample\Heart\ZU09BFB62105060253I_000.zdt"
# zpx_loc = r"Data\Sample\Heart\ZU09BFB62105060253I_000.zpx"

# zdt = "ZG88310520080701GYH_006.zdt"

# list_ = BinImport.ImportWaveHeader(zdt)
# list_[1]
