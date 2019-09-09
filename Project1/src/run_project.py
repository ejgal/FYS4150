# -*- coding: utf-8 -*-
#!/usr/bin/env python2
"""
Script for running our experiment

Takes three command line arguments:

First argument, the highest exponent determining the
highest dimmension of our n x n matrix.

Second argument, determining the exponent of highest dimmension
of our n x n matrix, when using LU decomposition. Note: Demands a
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
from linalg import TDCMA, TDMA, build_toeplitz

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


# Write headers to output files
with open(DATADIR + 'TDMA.csv', 'w') as file:
    file.write('n,run time (s)\n')

with open(DATADIR + 'TDCMA.csv', 'w') as file:
    file.write('n,run time (s)\n')

with open(DATADIR + 'relative_error.csv', 'w') as file:
    file.write('$log_{10}$(h), max(relative error)\n')

with open(DATADIR + 'LU_timing.csv', 'w') as file:
    file.write('n,run time (s)\n')


for n in [10, 100, 1000]:
    x = np.linspace(0, 1, n+2)
    v = np.zeros(n+2)
    a = -np.ones(n)
    b = 2*np.ones(n)
    c = -np.ones(n)
    v[1:-1], elapsed_time = TDMA(a, b, c, f, n)
    plt.plot(x, v, label='n={}'.format(n))

plt.plot(x, u(x), '--', label='Analytic')
plt.legend()
plt.savefig(PLOTDIR + 'TDMA.png')
plt.clf()

ns = [10**i for i in range(1, exponent+1)]
for n in ns:
    # Run thomaz algorithm
    x = np.linspace(0, 1, n+2)
    v = np.zeros(n+2)
    a = -np.ones(n)
    b = 2*np.ones(n)
    c = -np.ones(n)
    v[1:-1], elapsed_time = TDMA(a, b, c, f, n, runs)

    # Write results to file
    with open(DATADIR + "TDMA.csv", 'a') as file:
        file.write('{},{:.2e}\n'.format(n, elapsed_time))

    # Calculate relative error
    h = 1./(n+1)
    # analytic = u(x[int(n/10.):-1])
    # numeric = v[int(n/10.):-1]
    analytic = u(x[1:-1])
    numeric = v[1:-1]
    relative_error = np.max(np.abs((analytic - numeric)/analytic))
    with open(DATADIR + 'relative_error.csv', 'a') as file:
        file.write('{:.10e}, {:.10e}\n'.format(h, relative_error))
    # plt.plot(x[1:-1], analytic-numeric)
    # plt.show()
    # Run algorithm for our töeplitz matrix
    x = np.linspace(0, 1, n+2)
    v = np.zeros(n+2)
    v[1:-1], elapsed_time = TDCMA(f, n, runs)

    # Write results to file
    with open(DATADIR + "TDCMA.csv", 'a') as file:
        file.write('{},{:.2e}\n'.format(n, elapsed_time))


# Run LU decomposition and back substitution
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

    # Write results to file
    with open(DATADIR + "LU_timing.csv", 'a') as file:
            file.write('{},{:.2e}\n'.format(n, average_algo_time))

# Write input parameters to file
with open(DATADIR + 'last_run.txt', 'w') as file:
    file.write('exponent: {}\n'.format(exponent))
    file.write('lu_exponent: {}\n'.format(lu_exponent))
    file.write('runs: {}\n'.format(runs))
