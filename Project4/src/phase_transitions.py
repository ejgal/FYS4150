from plot import *
from ising import ising,write_header,write_run,expectation_values
import numpy as np
from numba import jit,njit, prange
import time



@njit(parallel=True)
def phase_transitions(L,lenL,T,lenT, filename,ordered,delay=0):
    # E = np.zeros(shape=(lenL,lenT))
    # E2 = np.zeros(shape=(lenL,lenT))
    # M = np.zeros(shape=(lenL,lenT))
    # M2 = np.zeros(shape=(lenL,lenT))
    # accepted = np.zeros(shape=(lenL,lenT))

    for i in prange(lenT):
        for j in range(lenL):
            values, acc = ising(L[j],cycles,T[i], ordered=ordered,delay=delay)
            # expect = expectation_values(values, cycles,L[j],T[i])
            # E[j,i], E2[j,i] = expect[0:2]
            # M[j,i], M2[j,i] = expect[2:4]
            # # Mabs[j,i] = expect[5]
            # accepted[j,i] = acc

    # return E,E2,M,M2,accepted
if __name__ == '__main__':
    filename = '../data/test_parallel.csv'
    # write_header(filename)
    Tstart = 2.1
    Tend = 2.3
    dT = 0.05
    N = int((Tend-Tstart)/(dT))
    cycles = 500000
    L = np.array([40])
    lenL = len(L)
    L = np.array(L)
    T = np.linspace(Tstart, Tend, N)
    lenT = N

    phase_transitions(L,lenL, T,lenT, filename, ordered=0,delay=0)
    # print(phase_transitions.parallel_diagnostics(level=4))

    # E,E2,M,M2,accepted = phase_transitions(L,lenL, T,lenT, filename, ordered=0,delay=0)
    # for i in range(lenT):
    #     for j in range(lenL):
    #         expect = np.array([E[j,i],E2[j,i],M[j,i],M2[j,i],1])
    #         write_run(filename, expect, 1,1,1,1,1,1,1)

    # fig1 = plt.figure()
    # fig2 = plt.figure()
    # fig3 = plt.figure()
    # ax1 = fig1.gca()
    # ax2 = fig2.gca()
    # ax3 = fig3.gca()
    # Tstart = 2.1
    # Tend = 2.3
    # dT = 0.005
    # N = int((Tend-Tstart)/(dT))
    # cycles = 5000
    # L = np.array([40])
    # lenL = len(L)
    # L = np.array(L)
    # print('Number of temperatures: {}'.format(N))
    # print('Number of grids: {}'.format(lenL))
    # print('Monte-Carlo cycles: {}'.format(cycles))
    # print('Skipping first {} cycles'.format(int(cycles/10)))
    # T = np.linspace(Tstart, Tend, N)
    # start = time.time()
    # E, E2, M, M2 = phase_transitions(L, lenL, T, N, delay=int(cycles/10))
    # end = time.time()
    # for i in range(lenL):
    #     ax3.plot(T,(M2[i,:] - M[i,:]**2)/float(cycles), marker='o',linestyle=' ',label='L={}'.format(L[i]))
    # ax3.legend()
    #
    # E = np.abs(E)
    # M = np.abs(M)
    # print(E)
    # print(M)
    # for i in range(lenL):
    #     ax1.plot(T,E[i,:], marker='x',linestyle=' ',label='L={}'.format(L[i]))
    #     ax2.plot(T,M[i,:], marker='x',linestyle=' ',label='L={}'.format(L[i]))
    #
    # ax1.legend()
    # ax1.set_ylabel('Energy')
    # ax2.legend()
    # ax2.set_ylabel('Magnetization')
    # ax3.set_ylabel('Magnetization variance')
    # plt.show()
