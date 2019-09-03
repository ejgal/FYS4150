import sys
import matplotlib.pyplot as plt
import time
import numpy as np
from linalg import toeplitz, thomas

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

ns = [10**i for i in range(1, exponent+1)]
print(ns)

with open(DATADIR + 'thomas.csv', 'w') as file:
    file.write('n, run time (s)\n')

with open(DATADIR + 'toeplitz.csv', 'w') as file:
    file.write('n, run time (s)\n')

with open(DATADIR + 'relative_error.csv', 'w') as file:
    file.write('$log_{10}$(h), max(relative error)\n')


for n in ns:
    # Run thomaz algorithm
    x = np.linspace(0, 1, n+2)
    v = np.zeros(n+2)
    a = -np.ones(n)
    b = 2*np.ones(n)
    c = -np.ones(n)
    start_time = time.time()
    v[1:-1] = thomas(a, b, c, f, n)
    elapsed_time = time.time() - start_time
    with open(DATADIR + "thomas.csv", 'a') as file:
        file.write('{},{:.2e}\n'.format(n, elapsed_time))

    # plt.plot(x, u(x), '+')
    # plt.plot(x, v)
    # plt.savefig(PLOTDIR + "thomas_{}.png".format(n))
    # plt.clf()
    # Calculate relative error

    h = 1./(n+1)
    relative_error = np.max(np.abs((u(x[1:-1])-v[1:-1])/u(x[1:-1])))
    print(np.log10(h), np.log10(relative_error))
    with open(DATADIR + 'relative_error.csv', 'a') as file:
        file.write('{:.2f}, {:.2f}\n'.format(np.log10(h), np.log10(relative_error)))



    # Run algorithm for special case of a töeplitz matrix
    x = np.linspace(0, 1, n+2)
    v = np.zeros(n+2)
    start_time = time.time()
    v[1:-1] = toeplitz(2, f, n)
    elapsed_time = time.time() - start_time
    with open(DATADIR + "toeplitz.csv", 'a') as file:
        file.write('{},{:.2e}\n'.format(n, elapsed_time))
    # plt.plot(x, u(x), '+')
    # plt.plot(x, v)
    # plt.savefig(PLOTDIR + "toeplitz_{}.png".format(n))
    # plt.clf()
