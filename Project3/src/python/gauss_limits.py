import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


N = 40
r = np.linspace(-2,2,N)

R1,R2 = np.meshgrid(r,r)

def func(r1,r2):
    f = 0
    # print(np.abs(r2-r1))
    if np.abs(r1-r2) > 10**-20:
        f = np.exp(-4*(r1+r2))/np.abs(r2-r1)
    # else:
    #     f = np.exp(-4*(r1+r2))/10**-15
    return f

# Z = func(R1,R2)
Z = np.zeros(shape=(N,N))
for i in range(N):
    for j in range(N):
        Z[i,j] = func(r[i],r[j])

ax = plt.axes(projection='3d')
# ax.scatter3D(R1,R2,Z)
ax.plot_surface(R1,R2,np.log10(Z))
zticks = [1e-11,1e-10,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3]
ax.set_zticks(np.log10(zticks))
ax.set_zticklabels(zticks)

plt.show()
