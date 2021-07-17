from copy import deepcopy


def FromkeysReid(dict_name):
    '''
    mainfunc: creat a dict by list and re_id each variable
    '''

    dict_ = dict.fromkeys(dict_name)
    for i in dict_name:
        tmp = []
        dict_[i] = deepcopy(tmp)

    return dict_