# -*- coding: utf-8 -*-
"""
Script for running our experiment

Takes three command line arguments:

First argument, the highest exponent determining the highest dimmension 
of our n x n matrix.

Second argument, determining the exponent of highest dimmension 
of our n x n matrix, when using LU decomposition. Note: Demanding a 
lof of memory if set to 5 or higher.

Third argument, how many times each run should be executed
more runs would give accurate timings of each algorithm.

    python2 run_project.py 6 4 10

"""
import sys
import matplotlib.pyplot as plt
import time
import numpy as np

from computationalLib import pylib
from linalg import toeplitz, thomas, build_toeplitz

PLOTDIR = '../figures/'
DATADIR = '../data/'

def f(x):
    return 100*np.exp(-10*x)

def u(x):
    """
    Analytic solution
    """
    return 1 - (1 - np.exp(-10))* x - np.exp(-10*x)


exponent = int(sys.argv[1])
lu_exponent = int(sys.argv[2])
runs = int(sys.argv[3])

ns = [10**i for i in range(1, exponent+1)]

with open(DATADIR + 'thomas.csv', 'w') as file:
    file.write('n, run time (s)\n')

with open(DATADIR + 'toeplitz.csv', 'w') as file:
    file.write('n, run time (s)\n')

with open(DATADIR + 'relative_error.csv', 'w') as file:
    file.write('$log_{10}$(h), max(relative error)\n')

with open(DATADIR + 'LU_timing.csv', 'w') as file:
    file.write('n, run time (s)\n')


for n in [10, 100, 1000]:
    x = np.linspace(0, 1, n+2)
    v = np.zeros(n+2)
    a = -np.ones(n)
    b = 2*np.ones(n)
    c = -np.ones(n)
    v[1:-1], elapsed_time = thomas(a, b, c, f, n)
    plt.plot(x, v, label='n={}'.format(n))

plt.plot(x, u(x), '--', label='Analytic')
plt.legend()
plt.savefig(PLOTDIR + 'thomas.png')
plt.clf()


for n in ns:
    # Run thomaz algorithm
    x = np.linspace(0, 1, n+2)
    v = np.zeros(n+2)
    a = -np.ones(n)
    b = 2*np.ones(n)
    c = -np.ones(n)
    v[1:-1], elapsed_time = thomas(a, b, c, f, n, runs)

    with open(DATADIR + "thomas.csv", 'a') as file:
        file.write('{},{:.2e}\n'.format(n, elapsed_time))

    plt.plot(x, u(x), '+')
    plt.plot(x, v)
    plt.savefig(PLOTDIR + "thomas_{}.png".format(n))
    plt.clf()
    # Calculate relative error

    h = 1./(n+1)
    relative_error = np.max(np.abs((u(x[1:-1])-v[1:-1])/u(x[1:-1])))
    with open(DATADIR + 'relative_error.csv', 'a') as file:
        file.write('{:.2f}, {:.2e}\n'.format(np.log10(h), np.log10(relative_error)))



    # Run algorithm for our töeplitz matrix
    x = np.linspace(0, 1, n+2)
    v = np.zeros(n+2)
    v[1:-1], elapsed_time = toeplitz(f, n, runs)
    with open(DATADIR + "toeplitz.csv", 'a') as file:
        file.write('{},{:.2e}\n'.format(n, elapsed_time))
    plt.plot(x, u(x), '+')
    plt.plot(x, v)
    plt.savefig(PLOTDIR + "toeplitz_{}.png".format(n))
    plt.clf()

ns = [10**i for i in range(1, lu_exponent+1)]

for n in ns:
    algo_time = 0
    for run in range(1, runs+1):
        h = 1./(n+1)
        x = np.linspace(0, 1, n+2)
        u = f(x)*h**2
        A = build_toeplitz(-1, 2, -1, n)
        lib = pylib()
        start = time.time()
        A, index, t = lib.luDecomp(A)
        lib.luBackSubst(A, index, u[1:-1])
        algo_time += time.time() - start
    average_algo_time = algo_time/float(runs)
    with open(DATADIR + "LU_timing.csv", 'a') as file:
            file.write('{},{:.2e}\n'.format(n, average_algo_time))
