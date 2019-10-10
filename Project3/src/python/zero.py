import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



n = 100
r = np.linspace(0,2,n)
r1,r2 = np.meshgrid(r,r)
# z = np.exp(-4*(r1+r2))/(np.abs(r1-r2))
z = np.zeros((n,n))

for i in range(n):
    for j in range(n):
        if np.abs(r[i]-r[j]) > 10**-10:
            z[i,j] = np.exp(-4*(r[i]+r[j]))/(r[i]-r[j])




fig = plt.figure()
ax = fig.gca(projection='3d')

print(z)


ax.plot_surface(r1,r2,z)
plt.show()
