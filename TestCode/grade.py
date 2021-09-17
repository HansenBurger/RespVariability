import numpy as np

xuewei_xuefen = np.array([3.0, 3.0, 3.0, 3.0, 2.0, 1.0])
nxuewei_xuefen = np.array([3.0, 2.0, 3.0, 2.0, 2.0])

xuewei_grade = np.array([3.5, 3.2, 1.8, 2.3, 2.0, 3.5])
nxuewei_grade = np.array([2.9, 4.3, 2.95, 4.2, 3.6])

xuewei = xuewei_grade * xuewei_xuefen
nxuewei = nxuewei_grade * nxuewei_xuefen

up = np.sum(xuewei) * 0.7 + np.sum(nxuewei) * 0.3
down = np.sum(xuewei_xuefen) * 0.7 + np.sum(nxuewei_xuefen) * 0.3

result = up / down
print(result)