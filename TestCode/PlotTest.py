import numpy as np
import sys, pathlib
from copy import deepcopy
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

sys.path.append(str(pathlib.Path.cwd().parents[0]))

from Code import PointProcess as PP
from Code import InIReaWri
from Code.Fundal import BinImport

np.warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

# zdt_loc = r"Data\Sample\Resp\ZP0EBD1119121701RIA_223.zdt"
zdt_loc = InIReaWri.ConfigR("FileTestRoute", "WaveRead_zdt", conf=None)
zpx_loc = InIReaWri.ConfigR('FileTestRoute', 'WaveRead_zpx', conf=None)

info_list = PP.PointProcessing(zdt_loc)

wave_data = np.array([[0], [], []])

zpx_out = BinImport.ImportPara(zpx_loc)

# TODO 更改array下的每一个元素的地址

start_index = info_list[0]
start_index[-1]
F = info_list[2]
P = info_list[3]
V = info_list[4]

for i in range(start_index[51], start_index[100]):
    wave_data[0] = np.append(wave_data[0], F[i])
    wave_data[1] = np.append(wave_data[1], P[i])
    wave_data[2] = np.append(wave_data[2], V[i])

rect_height = np.max(wave_data[0]) - np.min(wave_data[0])
plt_range = len(wave_data[0])
rect_y = np.min(wave_data[0])
fig, axs = plt.subplots(3)
fig.suptitle("F & P & V")
# axs[0].add_patch(
#     Rectangle((start_index[65], rect_y), (start_index[69] - start_index[65]),
#               rect_height,
#               color='red',
#               alpha=0.5))
axs[0].plot(wave_data[0])
axs[1].plot(wave_data[1])
axs[2].plot(wave_data[2])
plt.gcf().set_size_inches(30, 6)
plt.show()
pass
plt.savefig('test.png', bbox_inches='tight', format='png', dpi=600)
