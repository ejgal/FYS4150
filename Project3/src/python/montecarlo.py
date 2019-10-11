import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



from numba import jit

N = int(10**6)
totalSum = 0
a,b = -2,2

@jit(nopython=True)
def integrate(N):
    totalSum = 0
    for i in range(N):
        x1 = np.random.uniform(a,b)
        y1 = np.random.uniform(a,b)
        z1 = np.random.uniform(a,b)
        x2 = np.random.uniform(a,b)
        y2 = np.random.uniform(a,b)
        z2 = np.random.uniform(a,b)


        r1 = np.sqrt(x1**2+y1**2+z1**2)
        r2 = np.sqrt(x2**2+y2**2+z2**2)
        distance = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
        if distance > 10**-10:
            func = np.exp(-4*(r1+r2))/distance
            totalSum += func
    return totalSum


width = b-a
result = width**6*integrate(N)/float(N)
analytical = 5*np.pi**2/16**2
error = analytical - result

print('Analytical: {:.5f}'.format(analytical))
print('Result: {:.5f}'.format(result))
print('Error: {:.5f}'.format(error))
