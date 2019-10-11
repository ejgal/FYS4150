import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from numba import jit




@jit(nopython=True)
def integrate(N):
    totalSum = 0
    for i in range(N):
        r1 = np.random.exponential()
        r2 = np.random.exponential()
        t1 = np.random.uniform(0,np.pi)
        t2 = np.random.uniform(0,np.pi)
        phi1 = np.random.uniform(0,2*np.pi)
        phi2 = np.random.uniform(0,2*np.pi)

        cosbeta = np.cos(t1)*np.cos(t2) + np.sin(t1)*np.sin(t2)*np.cos(phi1-phi2)
        distance = np.sqrt(r1**2 + r2**2 - 2*r1*r2*cosbeta)

        if distance > 10**-10:
            jacobian = r1**2*r2**2*np.sin(t1)*np.sin(t2)
            func = np.exp(-4*(r1+r2))/distance
            totalSum = totalSum + jacobian*func/(np.exp(-r1)*np.exp(-r2))

    return totalSum


N = int(10**8)

result = np.pi*np.pi*2*np.pi*2*np.pi*integrate(N)/float(N)
analytical = 5*np.pi**2/16**2
error = analytical - result

print('Analytical: {:.9f}'.format(analytical))
print('Result: {:.9f}'.format(result))
print('Error: {:.9f}'.format(error))
