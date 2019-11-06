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

    # grid = np.ones(shape=(L,L))
    # print(grid)
    # Initialize energy and magnetization
    for x in range(0, L):
        for y in range(0, L):
            init_e += -1./2 *grid[x,y] * (grid[(x+1)%L,y] + grid[(x-1)%L,y] + grid[x,(y+1)%L] + grid[x,(y-1)%L])
            init_m += grid[x,y]
    # print(init_m)
    # print('Initial energy: {}'.format(init_e))
    # print('Initial magnetization: {}'.format(init_m))
    # plt.ion()
    # plt.show()
    init_grid = grid

    E = init_e
    # print(E)
    M = init_m

    energy = 0
    energy2 = 0
    magnet = 0
    magnet2 = 0
    magnet_abs = 0

    # print('init m: {}'.format(magnet))
    # print('init m^2: {}'.format(magnet2))
    # Monte Carlo loop
    for k in prange(0,N):
        # sns.heatmap(grid, vmin=-1, vmax=1, cmap='Blues')
        # plt.pause(0.001)
        # plt.clf()
        # print(k)

        # Grid loop
        for i in prange(0,L**2):
            # Randomly proposed spin to flip
            x,y = int(np.random.uniform(0,1)*(L)), int(np.random.uniform(0,1)*(L))

            # Sum of surrounding spins
            sk = grid[(x+1)%L,y] + grid[(x-1)%L,y] + grid[x,(y+1)%L] + grid[x,(y-1)%L]
            Ediff = 2*(grid[x,y]*sk)
            deltaE = Edict[int(Ediff)]
            r = np.random.uniform(0,1)
            if r <= deltaE:
                # Flip spin
                grid[x,y] *= -1
                E += Ediff
                M += 2*grid[x,y]

            energy += E
            energy2 += E**2
            magnet += M
            magnet2 += M**2
            magnet_abs += np.abs(M)
            accepted += 1

    N = float(N-delay)
    return energy, energy2, magnet, magnet2, magnet_abs, accepted

if __name__ == '__main__':

    L = 2
    T = 1.
    N = 100000
    spins = L**2
    for i in range(0,10):
        E,E2,M,M2,Mabs, accepted = ising(L, N, T)
        N = float(N)


        Emean = E/(N*spins)
        E2mean = E2/(N*spins)
        Mmean = M/(N*spins)
        M2mean = M2/(N*spins)
        Mabsmean = Mabs/(N*spins)

        print(E/(N*spins*spins))
        print(M/(N*spins*spins))
        print((E2mean - Emean**2)/(spins*T**2))
        print((M2mean - Mmean**2)/(spins*T))
        print(Mabsmean/(spins))
        print('')

    # Emean = E/(N*spins)
    # Mmean = M/(N*spins)
    # E2mean = E2/(N*spins)
    #
    # print(Emean/(spins))
    # print(Mmean/(spins))
    # print((E2mean - Emean**2)/(spins))
    # print(E/(N*spins*spins))
    # print((E2 - E**2)/(N*spins*spins*T**2))
    # print(M/(spins*spins))
    # print((M2 - M**2)/(spins*spins*T))
    # print(Mabs/(spins*spins))
    # print(accepted)
