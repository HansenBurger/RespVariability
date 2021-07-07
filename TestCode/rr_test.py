from genericpath import getsize
from sys import path
from numpy.lib.shape_base import _put_along_axis_dispatcher
from pandas.core.dtypes.missing import isna
from Code import PointProcess, InIReaWri
import os
import pandas as pd
from sklearn.metrics import roc_curve, auc, r2_score
from matplotlib import pyplot as plt
import numpy as np

zdt_folder_loc = (
    InIReaWri.ConfigR("SampleDataRoute", "LargeSample_rsbi", conf=None) + "zdt"
)
zpx_folder_loc = (
    InIReaWri.ConfigR("SampleDataRoute", "LargeSample_rsbi", conf=None) + "zpx"
)

test_loc = InIReaWri.ConfigR("FileTestRoute", "WaveRead_zdt", conf=None)
form_loc = InIReaWri.ConfigR("FormRoute", "RsbiAnalysis", conf=None)

# info_list = PointProcess.PointProcessing(test_loc)

y_true = []
y = []
y_score = []
poslabel = 1


def FileCompare(file_name, folder_loc):
    # TODO compare the file name with id in form, return info about with or without
    for f in os.listdir(folder_loc):
        file_loc = os.path.join(folder_loc, f)
        if f.split(".")[0] == file_name and os.path.getsize(file_loc) != 0:
            return 1
    return 0


def RrCounter(info_list):
    index = info_list[0]
    sample_rate = info_list[5]

    breath_num = len(index)
    breath_time = index[-1] * (1 / sample_rate)

    if breath_time == 0:
        RR = 0
    else:
        RR = round(breath_num / (breath_time / 60), 2)

    return RR


df = pd.read_csv(form_loc)
for i in range(50):
    zdt_name = df.loc[i, "zdt_1"]
    endo_end = df.loc[i, "endo_end"]

    if FileCompare(zdt_name, zdt_folder_loc):
        file_loc = os.path.join(zdt_folder_loc, zdt_name) + ".zdt"
        file_info = PointProcess.PointProcessing(file_loc)
        if not len(file_info[0]):
            RR_tmp = -1
        else:
            RR_tmp = RrCounter(file_info)

        y.append(RR_tmp)
    else:
        y.append(-1)

    y_true.append(int(endo_end))

print(1)

y_ = []
y_true_ = []

# for i in range(len(y)):
#     if y[i] not in [-1, 0]:
#         if not y_true[i]:
#             y_tmp = score_simo(20, y[i])
#         else:
#             y_ymp = score_simo(30, y[i])
#         y_.append(y_tmp)
#         y_true_.append(y_true[i])
#     else:
#         continue


fpr, tpr, thersholds = roc_curve(y_true, y_score, poslabel)

roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, "k--", label="ROC (area = {0:.2f})".format(roc_auc), lw=2)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")  # 可以使用中文，但需要导入一些库即字体
plt.title("ROC Curve")
plt.legend(loc="lower right")
plt.show()


# start_index = info_list[0]
# F = info_list[2]
# P = info_list[3]
# V = info_list[4]
# ref_samplerate = info_list[5]

# still_time = 1 / ref_samplerate
# total_time = still_time * start_index[-1]
# RR = np.array([])

# for i in range(len(start_index) - 1000):
#     RR_tmp = round((start_index[i + 1] - start_index[i]) * still_time, 2)
#     RR = np.append(RR, RR_tmp)

# fig, axs = plt.subplots(3)
# fig.suptitle("RR")
# axs[0].plot(RR)
# plt.show()


# print(total_time, len(start_index) / 60)

