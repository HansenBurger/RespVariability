import func


def WaveInfo_ReadCount(pid):
    func.TableBuild(pid)
    func.BinaryRead()
    func.Calculate()
    record = func.data.record_1
    return record


class Resp():
    def __init__(self, p_s, p_e):
        self.__p_s = p_s
        self.__p_e = p_e
        self.__p_m = 0
        self.vent_len = p_e - p_s
        self.v_t = None
        self.valid = True
        self.s_P = None
        self.s_F = None
        self.s_V = None

    def WaveInit(self, P, F, V):
        self.s_P = func.np.array(P[self.__p_s:self.__p_e])
        self.s_F = func.np.array(F[self.__p_s:self.__p_e])
        self.s_V = func.np.array(V[self.__p_s:self.__p_e])

    def __SwitchPoint(self, array_):
        interval = 15
        ind_array = func.np.where(array_[interval:] < 0)[0]
        try:
            ind = ind_array[0] + interval
        except:
            ind = None
        return ind

    def __GapDetection(self):
        min_gap = 50
        max_gap = 450
        gap = abs(self.__p_s - self.__p_e)

        if gap < min_gap or gap > max_gap or gap == 0:
            return False
        else:
            return True

    def __LineDetection(self, array_):

        if func.np.all(array_ == array_[0]):
            return False
        else:
            return True

    def __LenMatch(self, array_1, array_2):
        len_1 = array_1.shape[0]
        len_2 = array_2.shape[0]

        if len_1 != len_2:
            self.valid = False

    def __ArrayCertify(self, list_):
        list_ = [list_] if type(list_) == func.np.array else list_

        for array in list_:
            if not func.np.any(array):
                self.valid = False
                return

    def ValidityCheck(self):
        if self.__GapDetection():
            if self.__LineDetection(self.s_F) and self.__SwitchPoint(self.s_F):
                self.__p_m = self.__SwitchPoint(self.s_F) + self.__p_s
                if self.__p_m != self.__p_s:
                    m_relative = self.__p_m - self.__p_s
                    p_in = self.s_P[0:m_relative]
                    p_ex = self.s_P[m_relative:]
                    v_in = self.s_V[0:m_relative]
                    v_ex = self.s_V[m_relative:]

                    self.__ArrayCertify([p_in, p_ex, v_in, v_ex])
                    self.__LenMatch(p_in, v_in)
                    self.__LenMatch(p_ex, v_ex)

                    if v_in[-1] == 0:
                        self.valid = False

                else:
                    self.valid = False
            else:
                self.valid = False
        else:
            self.valid = False

    def Vt(self):
        self.v_t = round(
            self.s_V[self.__p_m - self.__p_s] if self.__p_m != 0 else 0, 2)

    def __Check_01(self):
        m_relative = self.__p_m - self.__p_s
        s_f = self.s_F[:]
        f_e = self.s_F[m_relative]
        return True if f_e < 0.1 * s_f.max() else False

    def __Check_02(self, sample_rate):
        T = self.vent_len * 1 / sample_rate
        T_in = (self.__p_m - self.__p_s) * 1 / sample_rate
        return True if T > 2.5 * T_in else False

    def __Check_03(self):
        m_relative = self.__p_m - self.__p_s
        v_in = self.s_V[0:m_relative]
        v_ex = self.s_V[m_relative:]
        v_t_i = v_in[-1]
        v_t_e = v_in[-1] + (v_ex[-1] if v_ex[-1] < 0 else -v_ex[-1])
        return True if v_t_i > 200 and abs(v_t_i -
                                           v_t_e) < 0.1 * v_t_i else False

    def CheckMethods(self, sr):
        if self.valid:
            self.valid = True if self.__Check_01() and self.__Check_02(
                sr) and self.__Check_03() else False
        else:
            pass


class WaveInfoTest():
    def __init__(self, wave_len) -> None:
        self.__wave_len = wave_len
        self.__resp_list = []

    @property
    def resp_list(self):
        return self.__resp_list

    def __WaveAppend(self, wave_out, wave_in):
        return func.np.append(wave_out, wave_in)

    def WaveRaw(self, flow):
        self.__s_r = flow.sample_rate
        w_s = self.__wave_len[0]
        w_e = self.__wave_len[1]
        s_F, s_P, s_V = [func.np.array([])] * 3
        for i in range(w_s, w_e, 1):
            resp = Resp(flow.p_start[i], flow.p_end[i])
            resp.WaveInit(flow.s_P, flow.s_F, flow.s_V)
            s_F = self.__WaveAppend(s_F, resp.s_F)
            s_P = self.__WaveAppend(s_P, resp.s_P)
            s_V = self.__WaveAppend(s_V, resp.s_V)
            self.__resp_list.append(resp)
        return s_F, s_P, s_V

    def WaveCheck(self):
        s_F, s_P, s_V = [func.np.array([])] * 3
        zero_init = lambda x, y: func.np.zeros(x.shape[0]) if not y else x
        for resp in self.__resp_list:
            resp.ValidityCheck()
            resp_s_F = zero_init(resp.s_F, resp.valid)
            resp_s_P = zero_init(resp.s_P, resp.valid)
            resp_s_V = zero_init(resp.s_V, resp.valid)
            s_F = self.__WaveAppend(s_F, resp_s_F)
            s_P = self.__WaveAppend(s_P, resp_s_P)
            s_V = self.__WaveAppend(s_V, resp_s_V)
        return s_F, s_P, s_V

    def WaveCheckPlus(self):
        s_F, s_P, s_V = [func.np.array([])] * 3
        zero_init = lambda x, y: func.np.zeros(x.shape[0]) if not y else x
        for resp in self.__resp_list:
            resp.ValidityCheck()
            resp.CheckMethods(self.__s_r)
            resp_s_F = zero_init(resp.s_F, resp.valid)
            resp_s_P = zero_init(resp.s_P, resp.valid)
            resp_s_V = zero_init(resp.s_V, resp.valid)
            s_F = self.__WaveAppend(s_F, resp_s_F)
            s_P = self.__WaveAppend(s_P, resp_s_P)
            s_V = self.__WaveAppend(s_V, resp_s_V)
        return s_F, s_P, s_V


def WavePlot(args):
    f = args[0]
    p = args[1]
    v = args[2]
    func.plt.figure(figsize=(16, 11))
    func.plt.suptitle('F & P & V')
    func.plt.subplot(3, 1, 1)
    func.plt.plot(f)
    func.plt.subplot(3, 1, 2)
    func.plt.plot(p)
    func.plt.subplot(3, 1, 3)
    func.plt.plot(v)
    func.plt.show()
    #func.plt.close()


flow_wh = WaveInfo_ReadCount(241852)
test_wave = WaveInfoTest([0, 20])

WavePlot(test_wave.WaveRaw(flow_wh))
WavePlot(test_wave.WaveCheck())
