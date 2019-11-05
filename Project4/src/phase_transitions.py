from plot import *
from ising import ising
import numpy as np



# if __name__ == '__main__':

fig1 = plt.figure()
fig2 = plt.figure()
ax1 = fig1.gca(xscale='log')#,yscale='log')
ax2 = fig2.gca(xscale='log')
Tstart = 2.0
Tend = 2.3
dT = 0.01
N = int((Tend-Tstart)/(dT))
T = np.linspace(Tstart, Tend, N)
cycles = 1000


for L in [40,60,80,100]:
    E,E2,M,M2, accepted = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)
    for i in range(0,len(T)):
        print('T: {:.2f}, L: {}'.format(T[i],L))
        E[i], E2[i],M[i], M2[i], accepted[i] = ising(L,cycles,T[i])

    E = np.abs(E)/L**2
    M = np.abs(M)/L**2

    ax1.plot(T, E, linestyle='--', marker='o', label=r'|E|/L$^2$, L={}'.format(L))
    ax2.plot(T, M, linestyle='--', marker='s', label=r'|M|/L$^2$. L={}'.format(L))
ax1.legend()
ax2.legend()
plt.show()
