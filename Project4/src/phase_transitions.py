from plot import *
from ising import ising,write_header,write_run,expectation_values
import numpy as np
from numba import jit,njit, prange
import time



@njit(parallel=True)
def phase_transitions(L,lenL,T,lenT, filename,ordered,delay=0):
    E = np.zeros(shape=(lenL,lenT))
    M = np.zeros(shape=(lenL,lenT))
    Mabs = np.zeros(shape=(lenL,lenT))
    cv = np.zeros(shape=(lenL,lenT))
    suscept = np.zeros(shape=(lenL,lenT))
    accepted = np.zeros(shape=(lenL,lenT))

    for i in prange(lenT):
        for j in prange(lenL):
            values, acc = ising(L[j],cycles,T[i], ordered=ordered,delay=delay)
            expect = expectation_values(values, cycles,L[j],T[i], delay)
            E[j,i] = expect[0]
            M[j,i] = expect[1]
            Mabs[j,i] = expect[2]
            cv[j,i] = expect[3]
            suscept[j,i] = expect[4]
            accepted[j,i] = acc

    return E,M,Mabs,cv,suscept,accepted

if __name__ == '__main__':

    filename = '../data/test_parallel.csv'
    Tstart = 1.5
    Tend = 3.0
    dT = 0.1
    N = int((Tend-Tstart)/(dT))
    cycles = 500000
    ordered = 0
    delay = 400000
    L = np.array([20])
    lenL = len(L)
    L = np.array(L)
    T = np.linspace(Tstart, Tend, N)
    lenT = N

    print('#T={}'.format(N))

    E,M,Mabs,cv,suscept,accepted = phase_transitions(L,lenL, T,lenT, filename, ordered=ordered,delay=delay)

    write_header(filename)
    for i in range(lenT):
        for j in range(lenL):
            expect = np.array([E[j,i],M[j,i],Mabs[j,i],cv[j,i],suscept[j,i]])
            write_run(filename, expect, T[i],L[j],ordered,cycles,delay,accepted[j,i])
