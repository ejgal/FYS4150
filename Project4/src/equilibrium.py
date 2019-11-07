from ising import ising
import numpy as np
import matplotlib.pyplot as plt
from plot import *




L = 20
N = 30
cycles = np.logspace(2,5,N)


fig1 = plt.figure()
fig2 = plt.figure()
fig3 = plt.figure()

ax1 = fig1.gca(xscale='log')#,yscale='log')
ax2 = fig2.gca(xscale='log')#,yscale='log')
ax3 = fig3.gca(xscale='log')#, yscale='log')

for T, marker in zip([1., 2.4], ['s','o']):

    E,E2,M,M2, accepted = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)
    for i in range(0,len(cycles)):
        print('T: {}, cycle: {}/{}'.format(T, int(cycles[i]), cycles[-1]))
        E[i], E2[i],M[i], M2[i], Mabs, accepted[i] = ising(L,cycles[i],T)

    spins = L**2
    Emean = E/(cycles*spins)
    E2mean = E2/(cycles*spins)
    Mmean = M/(cycles*spins)
    M2mean = M2/(cycles*spins)
    Mabsmean = Mabs/(cycles*spins)
    # (E2mean - Emean**2)/(spins*T**2))
    # print((M2mean - Mmean**2)/(spins*T))

    ax1.plot(cycles, np.abs(Emean/L**2), label='T={}'.format(T))

    # ax1.plot(cycles, E, marker=marker, linestyle='--', label=r'|E|/L$^2$, T={}'.format(T))
    plt.xlabel('Monte-Carlo cycles')
    ax3.plot(cycles, accepted/cycles[i], label='accepted states, T={}'.format(T))

    ax2.plot(cycles, np.abs(Mmean/L**2), marker=marker, linestyle='--', label='|M|/L$^2$, T={}'.format(T))
    plt.xlabel('Monte-Carlo cycles')
ax1.legend()
ax2.legend()
ax3.legend()
plt.show()
