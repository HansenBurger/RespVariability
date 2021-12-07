import func


def TableProcessing_RecordGeneration(switch=True):
    func.SaveLocGenerate('effection_PSV_ICU4')
    func.MainTableBuild() if switch else func.TestTableBuild()
    func.GenerateObjList()
    func.GenerateFileLoc()


def RecordReading_RespCalculation():
    func.GetBinOutput()
    func.Calculate()
    func.RespValidity()


def Linear_Analysis_Preservation():
    func.MethodTS()
    func.TimeAggregate()
    func.TimeDomainTableBuild('result: linear PSV')
    # func.LinearGraph()


def Nonlinear_Analysis_Preservation():
    # func.ScatterPlotPer()
    func.MethodHRA()
    func.MethodHRV()
    func.NonlinearAggregate()
    func.NonlinearTableBuild('result: nonlinear PSV')
    # func.NonlinearGraph()


def main():
    TableProcessing_RecordGeneration()
    RecordReading_RespCalculation()
    Linear_Analysis_Preservation()
    Nonlinear_Analysis_Preservation()


if __name__ == '__main__':
    print('main function running')
    main()