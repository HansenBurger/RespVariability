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
                'name': 'WeanData'
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
            'record ID': 'Record_id',
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
            'CV RR': 'RR_3',
            'CV V_T': 'V_T_3',
            'CV VE': 'VE_3',
            'CV WOB': 'WOB_3',
            'CV RSBI': 'RSBI_3',
            'CV MP(Jm) d': 'MP_jm_3_d',
            'CV MP(JL) d': 'MP_jl_3_d',
            'CV MP(Jm) t': 'MP_jm_3_t',
            'CV MP(JL) t': 'MP_jl_3_t',
            'Median RR': 'RR_4',
            'Median V_T': 'V_T_4',
            'Median VE': 'VE_4',
            'Median WOB': 'WOB_4',
            'Median RSBI': 'RSBI_4',
            'Median MP(Jm) d': 'MP_jm_4_d',
            'Median MP(JL) d': 'MP_jl_4_d',
            'Median MP(Jm) t': 'MP_jm_4_t',
            'Median MP(JL) t': 'MP_jl_4_t',
            'Average RR': 'RR_1',
            'Average V_T': 'V_T_1',
            'Average VE': 'VE_1',
            'Average WOB': 'WOB_1',
            'Average RSBI': 'RSBI_1',
            'Average MP(Jm) d': 'MP_jm_1_d',
            'Average MP(JL) d': 'MP_jl_1_d',
            'Average MP(Jm) t': 'MP_jm_1_t',
            'Average MP(JL) t': 'MP_jl_1_t',
            'Standev RR': 'RR_2',
            'Standev V_T': 'V_T_2',
            'Standev VE': 'VE_2',
            'Standev WOB': 'WOB_2',
            'Standev RSBI': 'RSBI_2',
            'Standev MP(Jm) d': 'MP_jm_2_d',
            'Standev MP(JL) d': 'MP_jl_2_d',
            'Standev MP(Jm) t': 'MP_jm_2_t',
            'Standev MP(JL) t': 'MP_jl_2_t',
            'HRV RR': ['RR_SD1', 'RR_SD2'],
            'HRV V_T': ['VT_SD1', 'VT_SD2'],
            'HRV VE': ['VE_SD1', 'VE_SD2'],
            'HRV WOB': ['WOB_SD1', 'WOB_SD2'],
            'HRV RSBI': ['RSBI_SD1', 'RSBI_SD2'],
            'HRV MP(JL) d': ['MPJL_SD1_d', 'MPJL_SD2_d'],
            'HRV MP(Jm) d': ['MPJm_SD1_d', 'MPJm_SD2_d'],
            'HRV MP(JL) t': ['MPJL_SD1_t', 'MPJL_SD2_t'],
            'HRV MP(Jm) t': ['MPJm_SD1_t', 'MPJm_SD2_t'],
            'HRA RR': ['RR_PI', 'RR_GI', 'RR_SI'],
            'HRA V_T': ['VT_PI', 'VT_GI', 'VT_SI'],
            'HRA VE': ['VE_PI', 'VE_GI', 'VE_SI'],
            'HRA WOB': ['WOB_PI', 'WOB_GI', 'WOB_SI'],
            'HRA RSBI': ['RSBI_PI', 'RSBI_GI', 'RSBI_SI'],
            'HRA MP(JL) d': ['MPJL_PI_d', 'MPJL_GI_d', 'MPJL_SI_d'],
            'HRA MP(Jm) d': ['MPJm_PI_d', 'MPJm_GI_d', 'MPJm_SI_d'],
            'HRA MP(JL) t': ['MPJL_PI_t', 'MPJL_GI_t', 'MPJL_SI_t'],
            'HRA MP(Jm) t': ['MPJm_PI_t', 'MPJm_GI_t', 'MPJm_SI_t'],
        }

        self.save_table_name = {
            'result: linear PSV': 'Records_halfh_PSV_linear',
            'result: nonlinear PSV': 'Records_halfh_PSV_nonlinear',
            'result: linear sumP10': 'Records_halfh_sumP10_PSV_linear',
            'result: linear sumP12': 'Records_halfh_sumP12_PSV_linear',
            'result: nonlinear sumP12': 'Records_halfh_sumP12_PSV_nonlinear'
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
