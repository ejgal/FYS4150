import sys
import numpy as np
import matplotlib.pyplot as plt
import time

n = int(sys.argv[1])
start = 0
end = 1

def f(x):
    return 100*np.exp(-10*x)

def u(x):
    return 1 - (1 - np.exp(-10))* x - np.exp(-10*x)

x = np.linspace(start, end, n+1)
h = (end - start) / n

a = - np.ones(n-1)
b = 2 * np.ones(n)
c = - np.ones(n-1)
bt = np.zeros(n)
gt = np.zeros(n)

g = f(x[1:])*h**2
v = np.zeros(n)

bt[0] = b[0]
gt[0] = g[0]*a[0]/b[0]

start_time = time.time()

for i in range(1, n):
    bt[i] = b[i] - a[i-1] * c[i-1] / bt[i-1]
    gt[i] = g[i] - a[i-1] * gt[i-1] / bt[i-1]

for i in reversed(range(0, n-1)):
    v[i] = gt[i]/bt[i+1] - c[i]*v[i+1]/bt[i+1]

elapsed_time = time.time() - start_time
print('Elapsed time: {}, algorithm: {}, n={}'.format(elapsed_time, sys.argv[0].split('.')[0], n))


# w = np.zeros(n+1)
# w[1:] = v
# plt.plot(x, u(x))
# plt.plot(x, w)
# plt.savefig('plots/' + plotfile)
