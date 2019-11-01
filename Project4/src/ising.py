import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import seaborn as sns
from numba import jit, prange

def ising(L,N,T):
    B = 1./T
    J = 1

    # Energy differences
    Edict = {}
    for E in [-8*J,-4*J,0,4*J,8*J]:
        Edict[E] = np.exp(-B*E)
    # print(Edict)

    # Initialize grid with random configuration
    grid = np.zeros(shape=(L,L))
    grid = np.ones(shape=(L,L))
    # for i in range(0, L):
    #     for j in range(0, L):
    #         # Switch to better random number generator
    #         r = random.uniform()
    #         if r < 0.5:
    #             lattice[i,j] = 1
    #         else:
    #             lattice[i,j] = -1
    # plt.ion()
    # plt.show()
    for k in prange(0,N):
        # sns.heatmap(lattice, vmin=-1, vmax=1, cmap='Blues')
        # plt.pause(0.001)
        # plt.clf()
        # print(k)
        for i in prange(0,L**2):
            print(random.uniform()*(L-1))
            x,y = int(random.uniform()*(L)), int(random.uniform()*(L))
            print(x,y)
            # print('x+1: {},y+1: {}'.format(x+1,y+1))

            # if x+1 >= L:
            #     x = 0
            #     # print('x+1 >= L')
            # elif x == 0:
            #     x = L-2
            #     # print(x)
            #     # print('x-1 <0')
            # elif y+1 >= L:
            #     # print('y+1>L')
            #     y = 0
            # elif y == 0:
            #     y = L-2
            # # print('x+1: {},y+1: {}'.format(x+1,y+1))
            # if cx == 0 and cy == L-1:
                # print(2*(-lattice[cx,cy])*(lattice[x+1,y] + lattice[x-1,y] + lattice[x,y+1] + lattice[x,y-1]))
            sk = grid[(x+1)%L,y] + grid[(x-1)%L,y] + grid[x,(y+1)%L] + grid[x,(y-1)%L]
            Ediff = 2*(-grid[x,y]*sk)
            Ed = Edict[Ediff]
            p = np.exp(-Ed/T)
            r = random.uniform()
            if Ed < 0:
                lattice[x,y] *=-1
                E += Ed
            elif r < p:
                lattice[x,y] *= -1
                E += Ed

    return E/(L**2*N)

if __name__ == '__main__':
    for i in range(0,10):
        print(ising(4,100,1))
        print(ising(4,100,1))
