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
    func_1.SaveLocGenerate(TableFilter.__name__)
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
    func_2.SaveLocGenerate(DataChecker.__name__)
    func_2.MainTableBuild()
    func_2.GenerateObjList()
    func_2.GenerateFileLoc()
    func_2.GetBinOutput()
    func_2.ResultGenerate()
    func_2.TableBuild()
    func_2.TableProcess()


def StProcessor():
    '''
    ---- ModeProcessor ----
        Description: Check the ventilation pattern of the PID in chronological order
        Main Form: record_chek.csv
        Result Form: records_pro_1h_ExTube.csv
        Workflow:
            1. Save table basic information to the object list after sorting by PID
            2. Correction of the exTube time for each obj and re-saving of the obj's information
            3. Generate objlist ( attributes: necessary colnames for the new table )
            4. Save output to table and store
    '''
    func_3.SaveLocGenerate(StProcessor.__name__)
    func_3.MainTableBuild()
    func_3.TableRead_GP()
    func_3.RecordValidate_GP()
    func_3.CombineRecordsToPinfo()
    func_3.ResultBuild_PID()
    func_3.ResultBuild_VM()
    func_3.ResultBuild_ST_PEEP()
    func_3.ResultBuild_ST_PS()
    func_3.ResultBuild_ST_SUMP()
    func_3.ResultBuild_ST_E_SENS()
    func_3.TableProcess_PSV(1)
    func_3.TableProcess_SumP10(1)
    func_3.TableProcess_SumP12(1)
    #func_3.TbaleProcess_PEEPInvalid()


def main():
    print('I am the storm that is approooooaching !')
    TableFilter
    DataChecker
    StProcessor()


if __name__ == '__main__':
    main()