import func


def WaveInfo_ReadCount(pid):
    func.TableBuild(pid)
    func.BinaryRead()
    func.Calculate()
    outcome = func.Agger()
    return outcome.resp_t, outcome.rr


def FreqPreProcess(a_0, a_1, plot_save):
    interp_rate = 100  # Hz
    resample_rate = 4  # Hz

    #---- Workflow present ----#

    slice_cut = slice(20, 50, 1)  # WaveSlice
    process_freq = func.FreqPreMethod(a_0, a_1, slice_cut)
    process_plot = func.PlotMain(plot_save)

    process_freq.InitTimeSeries()
    process_freq.InterpValue(interp_rate)
    process_freq.Resampling(resample_rate)

    data_info = {
        'type':
        [process_freq.df_raw, process_freq.df_interp, process_freq.df_sample],
        'name': ['raw_scatter', 'interp_scatter', 'resample_scatter']
    }

    for i in range(len(data_info['name'])):
        data = data_info['type'][i]
        save_name = data_info['name'][i]
        process_plot.lmplot('time', 'value', data, save_name)

    #---- FFT Preprepare ----#

    slice_full = slice(0, 300, 1)
    pre_freq = func.FreqPreMethod(a_0, a_1, slice_full)
    pre_freq.InterpValue(interp_rate)
    pre_freq.Resampling(resample_rate)

    return pre_freq.df_sample, resample_rate


def FreqGenerate(data, fs, plot_save):
    process_trans = func.FreqTransMethod(data['value'], fs)
    process_plot = func.PlotMain(plot_save)

    process_plot.lineplot('time', 'value', data, 'origin_ts')

    process_trans.FFT_Bi()
    process_plot.lineplot('freq', 'range', process_trans.fft_bi, 'FFT_Bi')

    process_trans.FFT_Si()
    process_plot.lineplot('freq', 'range', process_trans.fft_si, 'FFT_Si')

    process_trans.PS_Si()
    process_plot.lineplot('freq', 'range', process_trans.ps_si, 'PS_Si')


def main():
    save_main = r'C:\Users\HY_Burger\Desktop\Project\RespVariability\TestCode\freq test\fig'
    ind, tar = WaveInfo_ReadCount(4694544)
    ts_data, Fs = FreqPreProcess(ind, tar, save_main)
    FreqGenerate(ts_data, Fs, save_main)


def SigleCheck(pid):
    func.TableBuild(pid)
    func.BinaryRead()
    func.Calculate()
    outcome = func.Agger()
    rsbi = outcome.rsbi
    rsbi_ = func.np.sort(rsbi)
    rr_ = outcome.rr
    mid_ = round(func.np.median(rsbi), 2)
    mean = round(func.np.mean(rsbi), 2)
    pass


if __name__ == '__main__':
    main()
    # SigleCheck(241852)