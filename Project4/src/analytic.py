import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from settings import *

J = 1


# Bruteforce solutions

def produce_states():
    """
    Generate all states for the 2x2 system
    """
    states = []
    for i in [-1,1]:
        for j in [-1,1]:
            for k in [-1,1]:
                for l in [-1,1]:
                    state = np.array([i,j,k,l])
                    states.append(state)
    states = np.array(states)
    return states


def energy(state):
    return -2*(state[0] + state[3])*(state[2] + state[1])

def count(state):
    up = np.count_nonzero(state == 1)
    return up

def magnetization(state):
    return np.sum(state)

def probability(T,state):
    E = energy(state)
    B = 1/T
    return np.exp(-B * E)/z(T)

def susceptibility(T):
    B = 1/T
    return variance_magnetization(T)/T

def heat_capacity(T):
    B = 1/T
    return variance_energy(T)/T**2


# Analytical solutions

def z(T):
    """
    Analytical solution of partition function.
    """
    B = 1/T
    return 2*(np.exp(8*B*J) + np.exp(-8*B*J)) + 12

def variance_energy(T):
    """
    Analytical solution of energy variance.
    """
    B = 1/T
    zt = z(T)
    return 256/zt* np.cosh(8*B) - 1024/zt**2 * np.sinh(8*B)**2

def variance_magnetization(T):
    """
    Analytical solution of magnetization variance.
    """
    B = 1/T
    zt = z(T)
    return 32/zt * (np.exp(8*B) + 1) - (8/zt)**2 *(np.exp(16*B) + 4*np.exp(8*B) + 4)


def expected_magnetization(T):
    """
    Analytical solution of <|M|>
    """
    B = 1/T
    return 8*(2 + np.exp(8*B))/z(T)

def expected_energy(T):
    """
    Analytical solution of <E>
    """
    B = 1/T
    return 16*(-np.exp(8*B) + np.exp(-8*B))/z(T)





if __name__ == '__main__':

    states = produce_states()

    T = 1
    L = 2
    spins = L**2
    # Print solutions
    print('Expected energy per spin: {:.5f}'.format(expected_energy(T)/spins))
    print('Expected magnetization per spin: {:.5f}'.format(expected_magnetization(T)/spins))
    print('Heat capacity per spin: {:.5f}'.format(heat_capacity(T)/spins))
    print('Susceptibility per spin: {:.5f}'.format(susceptibility(T)/spins))


    # Produce and save table
    df = pd.DataFrame(columns=['spins','Energy','Magnetization','Degeneracy'])
    for i in range(0, len(states)):
        df.loc[i] = [count(states[i]), energy(states[i]), magnetization(states[i]), count(states[i])]
    group = df.groupby(['spins','Energy','Magnetization']).count().reset_index().sort_values(by='spins', ascending=False)
    group.rename(columns={"spins": "Number of spins up"}, inplace=True)
    group.to_csv(DATADIR + 'analytic.csv', index=False)
