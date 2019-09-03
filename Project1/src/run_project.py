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



ns = [10**i for i in range(1, 7)]


with open(DATADIR + 'thomas.csv', 'w') as file:
    file.write('n, run time\n')

with open(DATADIR + 'toeplitz.csv', 'w') as file:
    file.write('n, run time\n')


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
        file.write('{},{}\n'.format(n, elapsed_time))

    plt.plot(x, u(x), '+')
    plt.plot(x, v)
    plt.savefig(PLOTDIR + "thomas_{}.png".format(n))
    plt.clf()

    # Run algorithm for special case of a töeplitz matrix
    x = np.linspace(0, 1, n+2)
    v = np.zeros(n+2)
    start_time = time.time()
    v[1:-1] = toeplitz(2, f, n)
    elapsed_time = time.time() - start_time
    with open(DATADIR + "toeplitz.csv", 'w') as file:
        file.write('{},{}\n'.format(n, elapsed_time))

    plt.plot(x, u(x), '+')
    plt.plot(x, v)
    plt.savefig(PLOTDIR + "toeplitz_{}.png".format(n))
    plt.clf()
