from ising import ising, expectation_values, write_run, write_header
import numpy as np
import matplotlib.pyplot as plt
from plot import *

if __name__ == '__main__':

    filename = '../data/equilibrium.csv'
    L = 20
    N = 30
    cycles = np.logspace(2,6,N)
    delay = 0
    ordered = 0

    write_header(filename)
    for T in [1., 2.4]:
        for i in range(0,len(cycles)):
            print('T: {}, cycle: {}/{}'.format(T, int(cycles[i]), cycles[-1]))
            values, accepted = ising(L,cycles[i],T, delay=0, ordered=0)
            expect = expectation_values(values, cycles[i],L,T)
            write_run(filename, expect, T,L,ordered,cycles[i],delay,accepted)
