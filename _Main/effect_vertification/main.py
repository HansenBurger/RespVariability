import func as func


def main():
    func.SaveLocGenerate()
    func.MainTableBuild()
    #   func.TestTableBuild()
    func.GenerateObjList()
    func.GenerateFileLoc()
    func.GetBinOutput()
    func.Calculate()
    func.MethodAverage()
    func.MethodStanDev()
    func.ResultAggregate()
    func.SaveTableBuild()
    func.SaveGraphs()


if __name__ == '__main__':
    print('main function running')
    main()