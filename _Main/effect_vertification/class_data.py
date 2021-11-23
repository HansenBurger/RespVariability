class DataBasic():
    def __init__(self) -> None:
        pass


class DataStatic(DataBasic):
    def __init__(self):
        super().__init__()

        self.file_loc_dict = {
            'main table': {
                'category': 'FormRoute',
                'name': 'ProcessForm'
            },
            'data folder': {
                'category': 'SampleDataRoute',
                'name': 'FiltedData'
            },
            'save form': {
                'category': 'ResultRoute',
                'name': 'FormFolder'
            },
            'save graph': {
                'category': 'ResultRoute',
                'name': 'GraphFolder'
            }
        }

        self.table_col_map = {
            'patient ID': 'PID',
            'record time': 'Resp_t',
            'record ID': 'Resp_id',
            'zdt name': 'zdt_1',
            'zpx name': 'zpx_1',
            'exTube end': 'endo_end'
        }

        self.time_col_name = [
            'Resp_t', 'end_time', 'Heart_t', 'endo_t', 'SBT_time'
        ]

        self.output_name_map = {
            'machine name': 'machineType',
            'sample rate': 'RefSampleRate',
            'para data index': 'uiDataIndex',
            'sampling sites': 0,
            'flowrate': 2,
            'pressure': 3,
            'volume': 4,
        }

        self.result_name_map = {
            'patient ID': 'PID',
            'exTube end': 'endo_end',
            'Average RR': 'RR_1',
            'Average V_T': 'V_T_1',
            'Average VE': 'VE_1',
            'Average WOB': 'WOB_1',
            'Average RSBI': 'RSBI_1',
            'Average MP(Jm)': 'MP_jm_1',
            'Average MP(JL)': 'MP_jl_1',
            'Standev RR': 'RR_2',
            'Standev V_T': 'V_T_2',
            'Standev VE': 'VE_2',
            'Standev WOB': 'WOB_2',
            'Standev RSBI': 'RSBI_2',
            'Standev MP(Jm)': 'MP_jm_2',
            'Standev MP(JL)': 'MP_jl_2',
            'HRV RR': ['RR_SD1', 'RR_SD2'],
            'HRV V_T': ['VT_SD1', 'VT_SD2'],
            'HRV VE': ['VE_SD1', 'VE_SD2'],
            'HRV WOB': ['WOB_SD1', 'WOB_SD2'],
            'HRV RSBI': ['RSBI_SD1', 'RSBI_SD2'],
            'HRV MP(JL)': ['MPJL_SD1', 'MPJL_SD2'],
            'HRV MP(Jm)': ['MPJm_SD1', 'MPJm_SD2'],
            'HRA RR': ['RR_PI', 'RR_GI', 'RR_SI'],
            'HRA V_T': ['VT_PI', 'VT_GI', 'VT_SI'],
            'HRA VE': ['VE_PI', 'VE_GI', 'VE_SI'],
            'HRA WOB': ['WOB_PI', 'WOB_GI', 'WOB_SI'],
            'HRA RSBI': ['RSBI_PI', 'RSBI_GI', 'RSBI_SI'],
            'HRA MP(JL)': ['MPJL_PI', 'MPJL_GI', 'MPJL_SI'],
            'HRA MP(Jm)': ['MPJm_PI', 'MPJm_GI', 'MPJm_SI'],
        }

        self.save_table_name = {
            'result: linear sumP10': 'Records_1h_sumP10_PSV_linear',
            'result: linear sumP12': 'Records_1h_sumP12_PSV_linear',
            'result: nonlinear sumP12': 'Records_1h_sumP12_PSV_nonlinear'
        }


class DataDynamic(DataBasic):
    def __init__(self):
        super().__init__()
        self.__df = None
        self.__df_new = None
        self.__save_form_loc = ''
        self.__save_graph_loc = ''
        self.__objlist_table = []
        self.__objlist_record = []
        self.__time_results = []
        self.__freq_results = []
        self.__nonl_results = []

    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, df):
        self.__df = df

    @property
    def df_new(self):
        return self.__df_new

    @df_new.setter
    def df_new(self, df):
        self.__df_new = df

    @property
    def save_form_loc(self):
        return self.__save_form_loc

    @save_form_loc.setter
    def save_form_loc(self, v):
        self.__save_form_loc = v

    @property
    def save_graph_loc(self):
        return self.__save_graph_loc

    @save_graph_loc.setter
    def save_graph_loc(self, v):
        self.__save_graph_loc = v

    @property
    def objlist_table(self):
        return self.__objlist_table

    @objlist_table.setter
    def objlist_table(self, list_):
        self.__objlist_table = list_

    @property
    def objlist_record(self):
        return self.__objlist_record

    @objlist_record.setter
    def objlist_record(self, list_):
        self.__objlist_record = list_

    @property
    def time_results(self):
        return self.__time_results

    @time_results.setter
    def time_results(self, list_):
        self.__time_results = list_

    @property
    def freq_results(self):
        return self.__freq_results

    @freq_results.setter
    def freq_results(self, list_):
        self.__freq_results = list_

    @property
    def nonl_results(self):
        return self.__nonl_results

    @nonl_results.setter
    def nonl_results(self, list_):
        self.__nonl_results = list_
