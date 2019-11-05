from plot import *
from ising import ising
import numpy as np
from numba import njit, prange
import time





@njit(parallel=True)
def phase_transitions(L,lenL,T,lenT, delay=0):
    E = np.zeros(shape=(lenL,lenT))
    E2 = np.zeros(shape=(lenL,lenT))
    M = np.zeros(shape=(lenL,lenT))
    M2 = np.zeros(shape=(lenL,lenT))
    accepted = 0
    for i in prange(lenT):
        for j in prange(lenL):
            E[j,i], E2[j,i],M[j,i], M2[j,i], accepted = ising(L[j],cycles,T[i], delay=delay)
            E[j,i] = E[j,i]/L[j]**2
            M[j,i] = M[j,i]/L[j]**2
            E2[j,i] = E2[j,i]/L[j]**2
            M2[j,i] = M2[j,i]/L[j]**2
    return E,E2,M,M2

if __name__ == '__main__':
    fig1 = plt.figure()
    fig2 = plt.figure()
    fig3 = plt.figure()
    ax1 = fig1.gca()
    ax2 = fig2.gca()
    ax3 = fig3.gca()
    Tstart = 2.1
    Tend = 2.3
    dT = 0.001
    N = int((Tend-Tstart)/(dT))
    cycles = 10000
    L = np.array([40])
    lenL = len(L)
    L = np.array(L)
    print('Number of temperatures: {}'.format(N))
    print('Number of grids: {}'.format(lenL))
    print('Monte-Carlo cycles: {}'.format(cycles))
    print('Skipping first {} cycles'.format(int(cycles/10)))
    T = np.linspace(Tstart, Tend, N)
    start = time.time()
    E, E2, M, M2 = phase_transitions(L, lenL, T, N, delay=int(cycles/10))
    end = time.time()
    for i in range(lenL):
        ax3.plot(T,(M2[i,:] - M[i,:]**2)/float(cycles), marker='o',linestyle='--',label='L={}'.format(L[i]))
    ax3.legend()

    E = np.abs(E)
    M = np.abs(M)
    # print(E)
    # print(M)
    print('Time used: {}'.format(end-start))
    np.save('E.np', E)
    np.save('M.np', M)
    for i in range(lenL):
        ax1.plot(T,E[i,:], marker='o',linestyle='--',label='L={}'.format(L[i]))
        ax2.plot(T,M[i,:], marker='o',linestyle='--',label='L={}'.format(L[i]))

    ax1.legend()
    ax1.set_ylabel('Energy')
    ax2.legend()
    ax2.set_ylabel('Magnetization')
    ax3.set_ylabel('Magnetization variance')
    plt.show()
