import table_func as func
'''
---- DataFilter ----
Description: Screen and maintain "data records" according to extraction time requirements
ExTube Form: 病人基本信息.csv (patients first ex-tube info till 2020.12)
Record Form: DATA.csv (patients records info till 2020.10)
ParaInfo Form: 拔管SBT_氧疗开始结束_条件拔管_条件撤机_条件SBT_再插管_再上机_通气时间大于2天小于90天.csv
Result Forms:
    PID missing: table_pid_miss.csv
    Condition filter not met: table_time_miss.csv
    Condition filter met: table_filted_r.csv
    Effective data records: table_filted_c.csv
    Ineffective data records: table_filted_lack.csv
Workflow:
    1. Generate DataFrame on demand
    2. Filter to get the index of the table
    3. Generate a table based on index and save it
'''


def DataFilter():
    func.SaveLocGenerate()
    func.RecordTableBuild()
    func.DependTableBuild()
    func.ParaTableBuild()
    func.TableExpansion()
    func.TableFilt()
    func.TableSave()
    func.TableProcess()


DataFilter()
