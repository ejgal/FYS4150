import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from numba import jit, prange


@jit(nopython=True)
def ising(L,N,T, delay=0):
    B = 1./T
    J = 1
    # Energy differences
    Edict = {}
    for energy in [-8,-4,0,4,8]:
        Edict[energy] = np.exp(-B*energy)
    init_e = 0
    init_m = 0
    accepted = 0
    # Initialize grid with random configuration
    grid = np.zeros(shape=(L,L))
    for x in range(0, L):
        for y in range(0, L):
            r = np.random.uniform(0,1)
            if r < 0.5:
                grid[x,y] = 1
            else:
                grid[x,y] = -1
    # Initialize energy and magnetization
    for x in range(0, L):
        for y in range(0, L):
            init_e += 1./2 *grid[x,y] * (grid[(x+1)%L,y] + grid[(x-1)%L,y] + grid[x,(y+1)%L] + grid[x,(y-1)%L])
            init_m += grid[x,y]
    init_grid = grid
    # print('Initial energy: {}'.format(init_e))
    # print('Initial magnetization: {}'.format(init_m))
    # plt.ion()
    # plt.show()
    energy = init_e
    energy2 = init_e**2
    magnet = init_m
    magnet2 = magnet**2
    for k in prange(0,N):
        # sns.heatmap(grid, vmin=-1, vmax=1, cmap='Blues')
        # plt.pause(0.001)
        # plt.clf()
        # print(k)
        for i in prange(0,L**2):
            x,y = int(np.random.uniform(0,1)*(L)), int(np.random.uniform(0,1)*(L))
            sk = grid[(x+1)%L,y] + grid[(x-1)%L,y] + grid[x,(y+1)%L] + grid[x,(y-1)%L]
            Ediff = 2*(grid[x,y]*sk)
            deltaE = Edict[int(Ediff)]
            p = deltaE
            r = np.random.uniform(0,1)

            if r <= p:
                grid[x,y] *= -1
                if k >= delay:
                    energy += -2*deltaE
                    energy2 += energy**2
                    magnet += 2*grid[x,y]
                    magnet2 += magnet**2
                    accepted += 1
                continue

            # Not necessary?
            if Ediff <= 0:
                print('Ediff')
                grid[x,y] *=-1
                energy += 2*deltaE
                energy2 += energy**2
                continue

    N = float(N-delay)
    return energy/(N), energy2/(N), magnet/N, magnet2/N, accepted

if __name__ == '__main__':

    L = 20
    N = 5
    T = np.linspace(1.75,2,N)
    cycles = 10000
    for i in range(N):
        print(i)
        E,E2,M,M2,d = ising(L, cycles, 1., 1000)
        plt.scatter(T[i],M)
    plt.show()
