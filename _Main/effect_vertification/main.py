import func


def TableProcessing_RecordGeneration(switch=True):
    func.SaveLocGenerate('effection_sumP10')
    func.MainTableBuild() if switch else func.TestTableBuild()
    func.GenerateObjList()
    func.GenerateFileLoc()


def RecordReading_RespCalculation():
    func.GetBinOutput()
    func.Calculate()
    func.RespValidity()


def Linear_Analysis_Preservation():
    func.MethodAverage()
    func.MethodStanDev()
    func.LinearAggregate()
    func.LinearTableBuild()
    func.LinearGraph()


def Nonlinear_Analysis_Preservation():
    func.ScatterPlotPer()
    func.MethodHRA()
    func.NonlinearAggregate()
    func.NonlinearTableBuild()
    func.NonlinearGraph()


def main():
    TableProcessing_RecordGeneration()
    RecordReading_RespCalculation()
    Linear_Analysis_Preservation()
    # Nonlinear_Analysis_Preservation()


if __name__ == '__main__':
    print('main function running')
    main()