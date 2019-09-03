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

b = 2
bt = np.zeros(n)
gt = np.zeros(n)

g = f(x[1:])*h**2
v = np.zeros(n)

bt[0] = b
gt[0] = - g[0]/b

start_time = time.time()

for i in range(1, n):
    z = 1. / bt[i-1]
    bt[i] = b - z
    gt[i] = g[i] + gt[i-1]*z

for i in reversed(range(0, n-1)):
    v[i] = (gt[i] + v[i+1]) / bt[i-1]

elapsed_time = time.time() - start_time
print('Elapsed time: {}, algorithm: {}, n={}'.format(elapsed_time, sys.argv[0].split('.')[0], n))

udisc = u(x[1:-1])
rel_err = np.abs((v[:-1] - udisc)/udisc)
# print(np.max(np.log10(rel_err)))
# print(np.log10(h))
# eps = np.log10(rel_err)
# print(np.max(eps))
# print(eps)
# plt.plot(x, u(x))
# plt.plot(x[1:], v)
# plt.show()
# plt.savefig('plots/' + plotfile)
