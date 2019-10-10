import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numba import jit
import numpy.polynomial.laguerre as laguerre
from computationalLib import pylib



N = 30
x,w  = laguerre.laggauss(N)
lib = pylib()
theta,wtheta = lib.gausLegendre(0,2*np.pi,N)
phi,wphi = lib.gausLegendre(0,np.pi,N)
# print(x, w)
# print(theta, wtheta)
# print(phi, wphi)
@jit(nopython=True)
def integrate():
    totalSum = 0
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    for m in range(N):
                        for n in range(N):
                            r1 = x[i]
                            r2 = x[j]
                            t1 = theta[k]
                            t2 = theta[l]
                            phi1 = phi[m]
                            phi2 = phi[n]
                            cosbeta = np.cos(t1)*np.cos(t2) + np.sin(t1)*np.sin(t2)*np.cos(phi1-phi2)
                            distance = np.sqrt(r1**2 + r2**2 - 2*r1*r2*cosbeta)
                            weight =  w[i]*w[j]*wtheta[k]*wtheta[l]*wphi[m]*wphi[n]
                            jacobian = r1**2*r2**2*np.sin(t1)*np.sin(t2)
                            if distance > 10**-10:
                                func = np.exp(-3*(r1+r2))/distance
                                totalSum = totalSum + weight*jacobian*func
        print(i)
    return totalSum


result = integrate()
analytical = 5*np.pi**2/16**2
error = analytical - result

print('Analytical: {:.5f}'.format(analytical))
print('Result: {:.5f}'.format(result))
print('Error: {:.5f}'.format(error))
