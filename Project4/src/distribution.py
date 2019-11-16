import numpy as np
import pandas as pd
from numba import jit,njit, prange

from settings import *
from ising import ising,write_header,write_run,expectation_values
from parser import phase_parser
from timing import estimate_time

if __name__ == '__main__':

    L = 20
    N = 1e6
    spins = L**2
    delay = 0
    ordered = 0
    filename='../data/dist'
    textfile = filename + '_{}.csv'.format(int(L))
    distfile = filename + '_dist.csv'
    write_header(textfile)

    Tstart = 1
    Tstop = 2.4
    # dT = 0.1
    # lenT = int((Tstop-Tstart)/(dT))
    lenT = 6
    T = np.linspace(Tstart, Tstop, lenT)

    distributions = []
    for i in range(lenT):
        values, accepted, distribution = ising(L, N, T[i], ordered=ordered,delay=delay,distribution=True)
        expect = expectation_values(values, N,L,T[i])
        distributions.append(pd.DataFrame(distribution))
        write_run(textfile,expect, T[i],L,ordered,N,delay,accepted)
    distributions = pd.concat(distributions,axis=1)
    temps = []
    for temp in T:
        temps.append('{:.2f}'.format(temp))
    distributions.columns = temps
    distributions.to_csv(distfile)
