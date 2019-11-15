import time
import numpy as np
from phase_transitions import phase_transitions

import os
if __name__ == '__main__':
    """
    Compare timings with and without parallelization.
    Found no way to disable njit(parallel=True) -> need to uncomment this line
    in phase_transitions.py.
    """

    # Run small grids and few T. Make sure lenT is divisible by number of cores.
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
    elapsed = time.time() - start
    print(elapsed)
