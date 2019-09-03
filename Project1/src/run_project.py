import sys
import matplotlib.pyplot as plt
import time
import numpy as np
from linalg import toeplitz, thomas

PLOTDIR = '../figures/'
DATADIR = '../data/'

n = int(sys.argv[1])

def f(x):
    return 100*np.exp(-10*x)

def u(x):
    """
    Analytic solution
    """
    return 1 - (1 - np.exp(-10))* x - np.exp(-10*x)



# Run thomaz algorithm
x = np.linspace(0, 1, n+2)
v = np.zeros(n+2)
a = -np.ones(n)
b = 2*np.ones(n)
c = -np.ones(n)
start_time = time.time()
v[1:-1] = thomas(a, b, c, f, n)
elapsed_time = time.time() - start_time
with open(DATADIR + "thomas.dat", 'w') as file:
    file.write('Run time: {}, n={}'.format(elapsed_time, n))

plt.plot(x, v)
plt.plot(x, u(x))
plt.show()

# Run algorithm for special case of a töeplitz matrix
x = np.linspace(0, 1, n+2)
v = np.zeros(n+2)
v[1:-1] = toeplitz(2, f, n)
plt.plot(x, v)
plt.plot(x, u(x))
# plt.show()
