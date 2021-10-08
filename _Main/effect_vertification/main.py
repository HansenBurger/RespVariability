import func


def TableProcessing_RecordGeneration(switch=True):
    func.MainTableBuild() if switch else func.TestTableBuild()
    func.GenerateObjList()
    func.GenerateFileLoc()
    func.GetBinOutput()


def RespCalculation_RespAnalysis():
    func.Calculate()
    func.MethodAverage()
    func.MethodStanDev()
    func.MethodHRA()


def Table_GraphGenerationPreservation():
    func.SaveLocGenerate()
    func.ResultAggregate()
    func.SaveTableBuild()
    func.SaveGraphs()


def main():
    TableProcessing_RecordGeneration()
    RespCalculation_RespAnalysis()
    Table_GraphGenerationPreservation()


if __name__ == '__main__':
    print('main function running')
    main()