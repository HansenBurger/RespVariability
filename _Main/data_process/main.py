import table_func as func_1
import record_func as func_2
import vent_func as func_3


def TableFilter():
    '''
    ---- TableFilter ----
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
    func_1.SaveLocGenerate()
    func_1.RecordTableBuild()
    func_1.DependTableBuild()
    func_1.ParaTableBuild()
    func_1.TableExpansion()
    func_1.TableFilt()
    func_1.TableSave()
    func_1.TableProcess()


def DataChecker():
    '''
    ---- DataChecker ----
        Description: Check basic information of records for further screening
        Main Form: table_filted_c.csv
        Result Form: record_check.csv
        Workflow:
            1. Generate objlist by Main Form (match one object per row)
            2. Save the necessary read info for each object
            3. Caculate "vent still time" and "vent mode every 30 min"
            4. Save output to table and store
    '''
    func_2.SaveLocGenerate()
    func_2.MainTableBuild()
    func_2.GenerateObjList()
    func_2.GenerateFileLoc()
    func_2.GetBinOutput()
    func_2.TableBuild()


def main():
    func_3.SaveLocGenerate()
    func_3.MainTableBuild()
    func_3.GenerateObjList_gp()
    func_3.ValidateObjList_gp()
    func_3.GenerateObjList_pid()
    func_3.TableBuild()
    func_3.TableProcess_1h()


if __name__ == '__main__':
    main()
