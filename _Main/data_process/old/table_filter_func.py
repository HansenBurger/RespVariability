from datetime import timedelta


def TimeFilter(df_1, df_2, namelist=['patient_id', '记录时间_1', '拔管时间', 'Index']):
    '''
    df_1: df_concat (DataFrame)
    df_2: df_baguan (DataFrame)
    namelist: Column names for operation dependencies (list)
    '''

    #   拔管时间间隔
    time_gap_hours = 2
    time_gap_minutes = 10

    result_1 = []
    result_2 = []
    result_3 = []
    result_4 = []

    gp_1 = df_1.groupby(namelist[0])
    gp_2 = df_2.groupby(namelist[0])

    for pid in df_2[namelist[0]].unique():

        try:
            df_tmp_gp1 = gp_1.get_group(pid)
            df_tmp_gp2 = gp_2.get_group(pid)

            df_tmp_gp1 = df_tmp_gp1.sort_values(by=namelist[1], ascending=True)
            df_tmp_gp2 = df_tmp_gp2.sort_values(by=namelist[2], ascending=True)

        except:
            result_1.append(pid)
            print('pid missing: ', pid)
            continue

        for i in df_tmp_gp2.index:

            index_tmp_list = []

            time_layer = df_tmp_gp2.loc[i, namelist[2]]
            time_gap = timedelta(hours=time_gap_hours,
                                 minutes=time_gap_minutes).seconds

            for j in df_tmp_gp1.index:

                time_ = df_tmp_gp1.loc[j, namelist[1]]

                time_differ = (time_layer - time_).total_seconds()
                # count the differ include date(not seconds)

                if time_differ >= 0 and time_differ <= time_gap:
                    loc = df_tmp_gp1.loc[j, namelist[3]]
                    index_tmp_list.append(loc)
                    # if j + 1 <= df_tmp_gp1.index.max():
                    #     time_gap_post = (df_tmp_gp1.loc[j + 1, namelist[1]] -
                    #                  time_layer).total_seconds()
                    # else:
                    #     time_gap_post = None
                    # result_4.append(time_gap_post)

                if time_ > time_layer:
                    if index_tmp_list != []:
                        result_4.append([(time_ - time_layer).total_seconds(),
                                         i])
                    break

            tmp = df_tmp_gp2.loc[i, namelist[3]]

            if not index_tmp_list:
                result_2.append(tmp)
                print('baguan info miss: ', tmp)
            else:
                index_tmp_list.append(tmp)
                result_3.append(index_tmp_list)

    return result_1, result_2, result_3, result_4


def TableBuild1(*args):
    '''
    args[0]: filted_index_list(list)
    args[1]: df_concat(DataFrame)
    args[2]: df_baguan(DataFrame)
    args[3]: combine_name_map(dict)
    args[4]: concat_name_map(dict)
    args[5]: filted_save_dict(dict)
    '''

    list_ = args[0]  # 筛选后得到的序列list
    df_1 = args[1]  # 被筛选的表
    df_2 = args[2]  # 筛选依据表
    map_1 = args[3]  # 生成表命名映射
    map_2 = args[4]
    save_ = args[5]

    for i in list_:

        copy_times = len(i[:-1])
        df_1_id = i[:-1]
        df_2_id = i[-1]

        df_1_info = df_1.loc[df_1_id]
        df_2_info = df_2.iloc[df_2_id]

        map_name_1 = list(map_1.keys())
        map_name_2 = list(map_2.keys())

        for j in map_name_1:

            tmp = []

            if j in map_name_2:
                tmp.append(df_1_info[map_1[j]].tolist())
                save_[j].extend(tmp[0])

            else:
                for t in range(copy_times):
                    tmp.append(df_2_info[map_1[j]])
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
