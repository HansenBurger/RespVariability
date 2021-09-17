from datetime import timedelta


def TimeFilter(df_1, df_2, namelist=['patient_id', 'PID', '记录时间_1', 'ExTime']):
    '''
    df_1: df_concat (DataFrame)
    df_2: df_baguan (DataFrame)
    namelist: Column names for operation dependencies (list)
    '''

    #   拔管时间间隔
    time_gap_hours = 3
    time_gap_minutes = 10

    result_1 = []
    result_2 = []
    result_3 = {'a_indexs': [], 'b_index': []}

    gp_1 = df_1.groupby(namelist[0])
    gp_2 = df_2.groupby(namelist[1])

    for pid in df_2[namelist[1]].unique():

        try:
            df_tmp_gp1 = gp_1.get_group(pid)
            df_tmp_gp2 = gp_2.get_group(pid)

        except:
            result_1.append(LocatIndex(df_2, namelist[1], pid)[0])
            print('pid missing: ', pid)
            continue

        df_tmp_gp1 = df_tmp_gp1.sort_values(by=namelist[2], ascending=True)
        df_tmp_gp2 = df_tmp_gp2.sort_values(by=namelist[3], ascending=True)

        for i in df_tmp_gp2.index:

            index_tmp_list = []

            time_layer = df_tmp_gp2.loc[i, namelist[3]]
            time_gap = timedelta(hours=time_gap_hours,
                                 minutes=time_gap_minutes).seconds

            for j in df_tmp_gp1.index:

                time_cur = df_tmp_gp1.loc[j, namelist[2]]
                time_differ = (time_layer - time_cur).total_seconds()
                # count the differ include date(not seconds)

                if time_differ >= 0 and time_differ <= time_gap:
                    index_tmp_list.append(j)

                if time_cur > time_layer:
                    break

            if not index_tmp_list:
                result_2.append(i)
                print('baguan info miss: ', i)
            else:
                result_3['a_indexs'].append(index_tmp_list)  # record index
                result_3['b_index'].append(i)  # baguan index

    return result_1, result_2, result_3


def TableBuild1(*args):
    '''
    args[0]: filted_index_list(list)
    args[1]: df_concat(DataFrame)
    args[2]: df_baguan(DataFrame) 
    args[3]: concat_name_map(dict)
    args[4]: baguan_name_map(dict)
    args[5]: filted_save_dict(dict)
    '''

    dict_ = args[0]  # 筛选后得到的序列dict
    df_1 = args[1]  # 被筛选的表
    df_2 = args[2]  # 筛选依据表
    map_1 = args[3]  # 映射1
    map_2 = args[4]  # 映射2
    save_ = args[5]

    dict_key = list(dict_.keys())  # result_dict key name

    for i in range(len(dict_[dict_key[0]])):

        df_1_id = dict_[dict_key[0]][i]
        df_2_id = dict_[dict_key[1]][i]
        copy_times = len(df_1_id)

        df_1_info = df_1.loc[df_1_id]  # multi
        df_2_info = df_2.iloc[df_2_id]  # single

        main_name = list(save_.keys())
        map_name_1 = list(map_1.keys())
        map_name_2 = list(map_2.keys())

        for j in main_name:

            tmp = []

            if j in map_name_1:
                tmp = df_1_info[map_1[j]].tolist()

            elif j in map_name_2[1:]:
                tmp = [df_2_info[map_2[j]]] * copy_times

            save_[j].extend(tmp)


def TableBuild2(*args):
    '''
    args[0]: time_miss_index(list)
    args[1]: df_baguan(DataFrame)
    args[2]: baguan_name_map(dict)
    args[3]: time_miss_dict(dict)
    '''

    list_ = args[0]
    df = args[1]
    map_ = args[2]
    save_ = args[3]

    for i in list_:

        df_info = df.iloc[i]
        map_name = list(map_.keys())

        for j in map_name:

            save_[j].append(df_info[map_[j]])
