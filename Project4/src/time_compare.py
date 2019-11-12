import time
import numpy as np
from phase_transitions import phase_transitions

import os
if __name__ == '__main__':



    # L = np.array([40,60,80,100])
    L = np.array([10,20])
    lenL = len(L)
    lenT = 32
    T = np.linspace(1, 2.4, lenT)
    cycles = 100000
    delay=0
    # Warmup
    phase_transitions(L,lenL,T,lenT, 100,0, delay=delay)


    print('start')
    start = time.time()
    phase_transitions(L,lenL,T,lenT, cycles,0, delay=delay)
    time_unpara = time.time() - start

    print(time_unpara)
    # print('start paralllel')
    # os.environ["NUMBA_DISABLE_PARALLEL"] = "0"
    # start = time.time()
    # phase_transitions(L,lenL, T,lenT, cycles,0,delay=delay)
    # time_para = time.time() - start
    #
    # print(time_para)
    # # print(time_unpara)
