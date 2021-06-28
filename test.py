from numpy.lib.function_base import percentile

# from Code import BinImport_c
"""
 BinImport_c test fail
"""
from Code.Fundal import BinImport
from Code.Fundal import ReadSamplerate as RS
import numpy as np
from matplotlib import pyplot as plt
from Code import PointProcess as PP

zdt_loc = r"Data\Sample\Heart\ZU09BFB62105060253I_000.zdt"
zpx_loc = r"Data\Sample\Heart\ZU09BFB62105060253I_000.zpx"

zdt = r"Data\Sample\Resp\ZP0EBD1119121701RIA_223.zdt"

para_info = BinImport.ImportPara(zpx_loc)[0]
wave_header = BinImport.ImportWaveHeader(zdt_loc)[0]
data_engine = BinImport.ImportWaveHeader(zdt_loc)[1]
head_size = wave_header["HeaderSize"].item()
channel_cnt = wave_header["ChannelCnt"].item()
machine_type = wave_header["Reserved1"][0].item()
# refSamplerate = RS.ReadSamplerate(machine_type)

with open(zdt_loc, "rb") as fid:
    fid.seek(head_size)
    data_info = np.fromfile(fid, np.uint16).tolist()
    data_info = np.array(data_info)

# print(len(data_info) % channel_cnt)
# len_ = round(len(data_info) / channel_cnt) * channel_cnt
# data_info = data_info[0:len_]

if len(data_info) % channel_cnt != 0:
    len_ = int(len(data_info) / channel_cnt) * channel_cnt
    data_info = data_info[:len_]

row_num = int(len(data_info) / channel_cnt)
column_num = channel_cnt

wave_data = np.reshape((data_info - 32768) / 100, (row_num, column_num)).T

# plt.plot(wave_data[1])
# plt.show()

wave_data = PP.PointProcessing(zdt)
a = 1
