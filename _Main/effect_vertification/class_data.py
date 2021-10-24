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
                'name': 'FormFolder_new'
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
            'HRA RR': ['RR_PI', 'RR_GI', 'RR_SI'],
            'HRA V_T': ['V_T_PI', 'V_T_GI', 'V_T_SI'],
            'HRA VE': ['VE_PI', 'VE_GI', 'VE_SI'],
            'HRA WOB': ['WOB_PI', 'WOB_GI', 'WOB_SI'],
            'HRA RSBI': ['RSBI_PI', 'RSBI_GI', 'RSBI_SI'],
        }

        self.save_table_name = {
            'result linear': 'Pro_1h_ExTube_linear',
            'result nonlinear': 'Pro_1h_ExTube_nonlinear'
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
        self.__linear_results = []
        self.__nonlinear_results = []

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
    def linear_results(self):
        return self.__linear_results

    @linear_results.setter
    def linear_results(self, list_):
        self.__linear_results = list_

    @property
    def nonlinear_results(self):
        return self.__nonlinear_results

    @nonlinear_results.setter
    def nonlinear_results(self, list_):
        self.__nonlinear_results = list_