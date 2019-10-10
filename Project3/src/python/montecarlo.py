import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from computationalLib import pylib

# def integrand(x1,y1,z1,x2,y2,z2):
#     r1 = np.sqrt(x[i]**2+x[j]**2+x[k]**2)
#     r2 = np.sqrt(x[l]**2+x[m]**2+x[n]**2)
#     distance = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
#     return np.exp(-4*(r1+r2))/distance
# # n = 1000


# lib = pylib()


from numba import jit

N = 100000
totalSum = 0

@jit(nopython=True)
def integrate():
    totalSum = 0
    for i in range(N):
        x1 = np.random.uniform(-1,1)
        y1 = np.random.uniform(-1,1)
        z1 = np.random.uniform(-1,1)
        x2 = np.random.uniform(-1,1)
        y2 = np.random.uniform(-1,1)
        z2 = np.random.uniform(-1,1)




        r1 = np.sqrt(x1**2+y1**2+z1**2)
        r2 = np.sqrt(x2**2+y2**2+z2**2)
        distance = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
        totalSum += np.exp(-4*(r1+r2))/distance
    return totalSum


result = integrate()/float(N)
analytical = 5*np.pi**2/16**2
error = analytical - result

print('Analytical: {:.5f}'.format(analytical))
print('Result: {:.5f}'.format(result))
print('Error: {:.5f}'.format(error))


# @jit(nopython=True)
# def integrate():
#     totalSum = 0
#     for i in range(N):
#         for j in range(N):
#             for k in range(N):
#                 for l in range(N):
#                     for m in range(N):
#                         for n in range(N):
#                             r1 = np.sqrt(x[i]**2+x[j]**2+x[k]**2)
#                             r2 = np.sqrt(x[l]**2+x[m]**2+x[n]**2)
#                             distance = np.sqrt((x[i]-x[l])**2 + (x[j]-x[m])**2 + (x[k]-x[n])**2)
#                             weight =  w[i]*w[j]*w[k]*w[l]*w[m]*w[n]
#
#                             if distance > 10**-10:
#                                 totalSum += weight*np.exp(-4*(r1+r2))/distance
#         print(i)
#     return totalSum
#
# result = integrate()
# analytical = 5*np.pi**2/16**2
# error = analytical - result
#
# print('Analytical: {:.5f}'.format(analytical))
# print('Result: {:.5f}'.format(result))
# print('Error: {:.5f}'.format(error))
# # n = 1000
# # r = np.linspace(-1,1,n)
# # r1,r2 = np.meshgrid(r,r)
# # # z = np.exp(-4*(r1+r2))/(np.abs(r1-r2))
# # z = np.zeros((n,n))
# #
# # for i in range(n):
# #     for j in range(n):
# #         if np.abs(r[i]-r[j]) > 10**-10:
# #             z[i,j] = np.exp(-4*(r[i]+r[j]))/(r[i]-r[j])
# #
# #
# #
# #
# # fig = plt.figure()
# # ax = fig.gca(projection='3d')
# #
# # ax.plot_surface(r1,r2,z)
# # plt.show()
