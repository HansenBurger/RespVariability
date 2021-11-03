from copy import deepcopy
from functools import wraps
from time import time


def FromkeysReid(dict_name):
    '''
    mainfunc: creat a dict by list and re_id each variable
    '''

    dict_ = dict.fromkeys(dict_name)
    for i in dict_name:
        tmp = []
        dict_[i] = deepcopy(tmp)

    return dict_


def measure(func):
    '''
    mainfunc: count time consuming of the function
    '''
    @wraps(func)
    def _time_it(*args, **kwargs):
        print(func.__name__, 'starts running...')
        start = int(round(time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time() * 1000)) - start
            print(f"Total execution time: {end_ if end_ > 0 else 0} ms\n")

    return _time_it


def InfoSave(file_loc, content):
    '''
    mainfunc: open the file and save the content
    '''
    f = open(file_loc, "w")
    f.write(content)
    f.close()