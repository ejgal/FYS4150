import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numba import jit, njit, prange



@jit(nopython=True)
def estimator_spherical(r1,r2,t1,t2,phi1,phi2):
    """
    """

    function_value = 0
    cosbeta = np.cos(t1)*np.cos(t2) + np.sin(t1)*np.sin(t2)*np.cos(phi1-phi2)
    distance_squared = r1**2 + r2**2 - 2*r1*r2*cosbeta
    if distance_squared > 10**-10:
        distance = np.sqrt(distance_squared)
        prefactor = np.pi**4 / 4.
        jacobi = r1**2*r2**2*np.sin(t1)*np.sin(t2)
        function_value = prefactor*jacobi/distance
    return function_value


@jit(nopython=True)
def estimator(x1,x2,y1,y2,z1,z2):
    function_value = 0
    r1 = np.sqrt(x1**2+y1**2+z1**2)
    r2 = np.sqrt(x2**2+y2**2+z2**2)

    distance = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
    if distance > 10**-10:
        function_value = np.exp(-4*(r1+r2))/distance
    return function_value





@njit(parallel=True)
def montecarlo_brute(N,a,b):
    """

    """
    Sum = 0
    Sum_squared = 0
    width = b-a
    probfactor = width**6
    for i in prange(N):
        x1 = np.random.uniform(a,b)
        y1 = np.random.uniform(a,b)
        z1 = np.random.uniform(a,b)
        x2 = np.random.uniform(a,b)
        y2 = np.random.uniform(a,b)
        z2 = np.random.uniform(a,b)


        r1 = np.sqrt(x1**2+y1**2+z1**2)
        r2 = np.sqrt(x2**2+y2**2+z2**2)
        fx = probfactor*estimator(x1,x2,y1,y2,z1,z2)
        Sum += fx
        Sum_squared += fx**2
    Sum = Sum/float(N)
    Sum_squared = Sum_squared/float(N)
    return Sum, Sum_squared




@njit(parallel=True)
def montecarlo_importance(N):
    """

    """

    Sum = 0
    Sum_squared = 0

    for i in prange(N):
        r1 = np.random.exponential(scale=1/4.)
        r2 = np.random.exponential(scale=1/4.)
        t1 = np.random.uniform(0,np.pi)
        t2 = np.random.uniform(0,np.pi)
        phi1 = np.random.uniform(0,2*np.pi)
        phi2 = np.random.uniform(0,2*np.pi)
        fx = estimator_spherical(r1,r2,t1,t2,phi1,phi2)
        Sum += fx
        Sum_squared += fx**2
    Sum = Sum/float(N)
    Sum_squared = Sum_squared/float(N)
    return Sum, Sum_squared





def print_results(Sum, Sum_squared):
    variance = (Sum_squared - (Sum**2))/float(N)
    analytical = 5*np.pi**2/16**2
    error = analytical - Sum
    print('Analytical: {:.9f}'.format(analytical))
    print('Result: {:.9f}'.format(Sum))
    print('Error: {:.9f}'.format(error))
    print('Standard deviation: {}'.format(np.sqrt(variance)))
    print('\n\n')

def variance(Sum, Sum_squared, N):
    return (Sum_squared - (Sum**2))/float(N)



std = []
error = []
analytical = 5*np.pi**2/16**2

Ns = [10**n for n in range(3,11)]
for N in Ns:
    print(N)
    s1,s2 = montecarlo_brute(N,-2,2)
    print_results(s1,s2)
    std.append(np.sqrt(variance(s1,s2,N)))
    error.append(analytical - s1)
    # s1,s2 = montecarlo_importance(N)
    # print_results(s1,s2)
print(std)
plt.plot(Ns, std)
plt.xscale("log")
plt.show()

print(error)

plt.plot(Ns, np.abs(error))
plt.xscale("log")
plt.show()
