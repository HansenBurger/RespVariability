import re
from typing import Pattern

record_info = {
    'pid': [1, 'PID'],
    'name': [1, 'NAME'],
    'age': [1, 'AGE'],
    'gender': [1, 'SEX'],
    'remark': [1, 'REMARK'],
    'dept': [1, 'DEPT'],
    'rid': [1, 'RID'],
    'machineType': [0, 'NAME'],
    'bed': [1, 'BED'],
    'time': [1, 'TIME']
}

file_loc = r"C:\Main\Data\_\Baguan\Records\202010\ZU09B42320101201EJY\ZU09B42320101201EJY.zif"

count = 0

patt = r"\"(.*)\" : \"(.*)\""
dict_num = 3
dict_list = []
return_dict = {}

with open(file_loc, 'rb') as fp:

    dict_tmp = {}
    # line = fp.readline()  # skip the 1st line(not able to decode)

    while dict_num != 0:

        try:
            line = fp.readline().decode('gbk')  # transfer to string

            if '}' in line:
                dict_list.append(dict_tmp)
                dict_num = dict_num - 1
                dict_tmp = {}
                continue

            elif '{' not in line:
                list_ = list(re.findall(patt, line)[0])  # 0:key, 1:value
                key = list_[0]
                value = list_[1]

                if not value:
                    value = None

                dict_tmp[key] = value
        except:
            continue

    record_name = list(record_info.keys())

    for i in record_name:
        return_dict[i] = dict_list[record_info[i][0]][record_info[i][1]]

print(1)

