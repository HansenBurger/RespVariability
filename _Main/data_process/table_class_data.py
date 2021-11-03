class TableDataBasic():
    def __init__(self) -> None:
        pass


class DataStatic(TableDataBasic):
    def __init__(self):
        super().__init__()
        self.file_loc_dict = {
            'concat': {
                'category': 'FormRoute',
                'name': 'MainDataForm',
                'dropcol': ['Resp_t'],
                'sortcol': 'PID'
            },
            'baguan': {
                'category': 'FormRoute',
                'name': 'BaguanForm',
                'sortcol': 'PID'
            },
            'para': {
                'category': 'FormRoute',
                'name': 'RecordForm',
                'sortcol': 'PID'
            },
            'save_form': {
                'category': 'ResultRoute',
                'name': 'FormFolder'
            }
        }

        self.timecol_name = [
            'Record_t', 'Resp_t', 'Heart_t', 'endo_t', 'SBT_time'
        ]

        self.colmap_concat = {
            'patient_id': 'PID',
            'record_id': 'Record_id',
            '记录时间_1': 'Resp_t',
            'RID_1': 'Resp_id',
            'zdt_1': 'zdt_1',
            'zpx_1': 'zpx_1',
            'RID_2': 'Heart_id',
            '记录时间_2': 'Heart_t',
            'zdt_2': 'zdt_2',
            'zpx_2': 'zpx_2'
        }

        self.colmap_baguan = {
            'PID': 'PID',
            'ExTime': 'endo_t',
            'ExtubeStatus': 'endo_end',
            'SBTInfo': 'SBT_info',
            'SBTTime': 'SBT_time',
            'SBTType': 'SBT_type'
        }

        self.colmap_para = {
            'PID': 'PID',
            'ICU': 'ICU',
            'StatusInfo': 'Status',
            'RecordTime': 'Record_t'
        }

        self.filt_result = [
            'pid_miss_index', 'time_miss_index', 'filt_index_a',
            'filt_index_b', 'copy_times', 'end_time'
        ]

        self.save_table_name = {
            'table filt ex1': 'table_pid_miss',
            'table filt ex2': 'table_time_miss',
            'table filt in': 'table_filted_r',
            'table valid': 'table_filted_c',
            'table invalid': 'table_filted_lack'
        }

        # The columnorder after filt
        self.col_name = [
            'PID', 'ICU', 'Record_id', 'Resp_t', 'end_time', 'Resp_id',
            'zdt_1', 'zpx_1', 'Heart_id', 'Heart_t', 'zdt_2', 'zpx_2',
            'endo_t', 'endo_end', 'SBT_info', 'SBT_time', 'SBT_type'
        ]


class DataDynamic(TableDataBasic):
    def __init__(self):
        super().__init__()
        self.__save_loc = ''
        self.__record_df = None  # data record form (DataFrame): df
        self.__depend_df = None  # baguan info form (DataFrame): df
        self.__para_df = None  # para form (DataFrame): df
        self.__result_dict = {}  # index info after filt
        self.__filt_df = None

    @property
    def save_loc(self):
        return self.__save_loc

    @save_loc.setter
    def save_loc(self, df):
        self.__save_loc = df

    @property
    def record_df(self):
        return self.__record_df

    @record_df.setter
    def record_df(self, df):
        self.__record_df = df

    @property
    def depend_df(self):
        return self.__depend_df

    @depend_df.setter
    def depend_df(self, df):
        self.__depend_df = df

    @property
    def para_df(self):
        return self.__para_df

    @para_df.setter
    def para_df(self, df):
        self.__para_df = df

    @property
    def result_dict(self):
        return self.__result_dict

    @result_dict.setter
    def result_dict(self, dict_):
        self.__result_dict = dict_

    @property
    def filt_df(self):
        return self.__filt_df

    @filt_df.setter
    def filt_df(self, df):
        self.__filt_df = df