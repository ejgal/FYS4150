import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from numba import jit, prange


@jit(nopython=True)
def ising(L,N,T,ordered=0,delay=0):
    B = 1./T
    J = 1

    # Energy differences
    Edict = {}
    for energy in [-8,-4,0,4,8]:
        Edict[energy] = np.exp(-B*energy)
    init_e = 0
    init_m = 0
    accepted = 0

    # Initialize grid

    # Spins pointing up
    grid = np.ones(shape=(L,L))
    if ordered == -1:
        # Spins pointing down
        grid = -grid
    elif ordered == 0:
        # Random grid
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
            init_e += -1./2 *grid[x,y] * (grid[(x+1)%L,y] + grid[(x-1)%L,y] + grid[x,(y+1)%L] + grid[x,(y-1)%L])
            init_m += grid[x,y]

    E = init_e
    M = init_m

    energy = 0
    energy2 = 0
    magnet = 0
    magnet2 = 0
    magnet_abs = 0

    # Monte Carlo loop
    for k in prange(0,N):
        # Grid loop
        for i in prange(0,L**2):
            # Randomly proposed spin to flip
            x,y = int(np.random.uniform(0,1)*(L)), int(np.random.uniform(0,1)*(L))

            # Sum of surrounding spins
            sk = grid[(x+1)%L,y] + grid[(x-1)%L,y] + grid[x,(y+1)%L] + grid[x,(y-1)%L]
            Ediff = 2*(grid[x,y]*sk)
            deltaE = Edict[int(Ediff)]
            r = np.random.uniform(0,1)

            # Metropolis algo
            if r <= deltaE:
                # Flip spin
                grid[x,y] *= -1
                E += Ediff
                M += 2*grid[x,y]
                accepted += 1

            # Update expectation values
            if k >= delay:
                energy += E
                energy2 += E**2
                magnet += M
                magnet2 += M**2
                magnet_abs += np.abs(M)

        # End grid loop
    # End Monte Carlo loop

    return np.array([energy, energy2, magnet, magnet2, magnet_abs]), accepted


@jit(nopython=True)
def expectation_values(values,N,L,T, delay=0):
    """
    Calculates various expectation values.
    """

    [E,E2,M,M2,Mabs] = values
    spins = L**2
    N = float(N - delay)
    Emean = E/(N*spins)
    E2mean = E2/(N*spins)
    Mmean = M/(N*spins)
    M2mean = M2/(N*spins)
    Mabsmean = Mabs/(N*spins)
    cv = (E2mean - Emean**2)/(spins*T**2)
    suscept = (M2mean - Mabsmean**2)/(spins*T)
    return np.array([Emean/spins, Mmean/spins, Mabsmean/spins, cv, suscept])


def write_header(filename):
    with open(filename, 'w') as file:
        file.write('T,spins,cycles,ordered,delay,E,M,Mabs,cv,suscept,accepted\n')


def write_run(filename, expect, T,L,ordered,cycles,delay,accepted):
    E,M,Mabs,cv,suscept = expect
    str = '{},{},{},{},{}'.format(T,L**2,cycles,ordered,delay)
    str += ',{},{},{},{},{},{}\n'.format(E,M,Mabs,cv,suscept, accepted)
    with open(filename, 'a') as file:
        file.write(str)



if __name__ == '__main__':

    L = 20
    T = 1.
    N = 10000
    spins = L**2
    delay = 0
    ordered = 0
    filename='../data/testfile.csv'
    write_header(filename)
    for i in range(0,1):
        values, accepted = ising(L, N, T, ordered=ordered,delay=delay)
        # print(expectation_values(values,N,L), accepted)
        expect = expectation_values(values, N,L,T)
        write_run(filename, expect, T,L,ordered,N,delay,accepted)
