import pandas as pd
import pathlib, sys
from domain_class import Domain1, Domain2, DomainAgger

sys.path.append(str(pathlib.Path.cwd().parents[1]))
from Code import FormProcess, InIReaWri
'''
1. 表的预处理，根据domain剔除不必要column，时间转换
2. series转list，生成domain1 obj
3. 地址拼接，找到zdt文件
4. 二进制文件读取+点处理
5. 存入agger，进入bussiness2计算处理
'''

column_names = ['PID', 'Record_t', 'Resp_id', 'zdt_1', 'zpx_1', 'endo_end']
time_columns = ['Record_t', 'Resp_id', 'endo_end']


def FormProcess(df, col_name, time_col):
    df = df.loc[col_name]
    FormProcess.TimeShift(df, time_col)