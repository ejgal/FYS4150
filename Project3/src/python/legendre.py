import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numba import jit


from computationalLib import pylib

def integrand(x1,y1,z1,x2,y2,z2):
    r1 = np.sqrt(x[i]**2+x[j]**2+x[k]**2)
    r2 = np.sqrt(x[l]**2+x[m]**2+x[n]**2)
    distance = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
    return np.exp(-4*(r1+r2))/distance


lib = pylib()
N = 5

rmax = 2
x,w = lib.gausLegendre(-rmax,rmax,N)
print(x,w)


@jit(nopython=True)
def integrate():
    totalSum = 0
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    for m in range(N):
                        for n in range(N):
                            r1 = np.sqrt(x[i]**2+x[j]**2+x[k]**2)
                            r2 = np.sqrt(x[l]**2+x[m]**2+x[n]**2)
                            distance = np.sqrt((x[i]-x[l])**2 + (x[j]-x[m])**2 + (x[k]-x[n])**2)
                            weight =  w[i]*w[j]*w[k]*w[l]*w[m]*w[n]

                            if distance > 10**-10:
                                totalSum += weight*np.exp(-4*(r1+r2))/distance
        print(i)
    return totalSum


result = integrate()
analytical = 5*np.pi**2/16**2
error = analytical - result

print('Analytical: {:.5f}'.format(analytical))
print('Result: {:.5f}'.format(result))
print('Error: {:.5f}'.format(error))
