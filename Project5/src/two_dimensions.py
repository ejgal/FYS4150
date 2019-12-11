import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


DATADIR = '../data/'


def sine(x, y):
    return np.sin(4*np.pi*x)*np.sin(4*np.pi*y)


def sine_der(x, y):
    return - 32*np.pi**2 * np.sin(4*np.pi*x)*np.sin(4*np.pi*y)


def poisson2d_bounded(p, b, dx, nx, target=1e-6, iter=10000):
    count = 0
    diff = 1
    ny = nx
    p[:, -1] = 0
    p[0, :] = 0
    p[-1, :] = 0
    p[:, 0] = 0

    while (diff > target and count < iter):
        diff = 0
        # p[10:15, 10:15] = 1
        pn = p.copy()
        # p[1:-1, 1:-1] = 0.25 * ((pn[1:-1, 2:] + pn[1:-1, 0:-2]) + (pn[2:, 1:-1] + pn[0:-2, 1:-1]))
        for j in range(1, nx - 1):
            for i in range(1, ny - 1):
                p[j, i] = - b[j, i] * dx**2
                p[j, i] += pn[j, i+1] + pn[j, i-1]
                p[j, i] += pn[j+1, i] + pn[j-1, i]
                p[j, i] *= 0.25
                diff += np.abs(pn[j, i] - p[j, i])  # Fix
        count += 1
        diff /= (nx**2)
        # print(diff)
        # plot2d(np.linspace(0,1,nx), np.linspace(0,1,nx), p)
        # plot2d(np.linspace(0, 1-dx, nx), np.linspace(0, 1, ny), p)
    print('Iterations: {}'.format(count))
    return p


def poisson2d_periodic(p, b, dx, nx, target=1e-6, iter=10000):
    count = 0
    diff = 1
    ny = nx + 1
    p[-1, :] = 0
    p[0, :] = 0
    while (diff > target and count < iter):
        diff = 0
        pn = p.copy()
        for i in range(0, nx):
            for j in range(1, ny - 1):
                p[j, i] = - b[j, i] * dx**2
                p[j, i] += (pn[j, (i+1) % nx] + pn[j, (i-1) % nx])
                p[j, i] += (pn[(j+1) % nx, i] + pn[(j-1) % ny, i])
                p[j, i] *= 1/4.
                diff += np.abs(pn[j, i] - p[j, i])
        count += 1
        diff /= (nx**2)
    print('Iterations: {}'.format(count))
    return p


def plot2d(x, y, p):
    fig = plt.figure(figsize=(11, 7), dpi=100)
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(x, y)
    _ = ax.plot_surface(X, Y, p[:])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    plt.show()


def bounded(dx, dt, t, save=False):
    nx = int(1/dx) + 1  # Bounded
    ny = int(1/dx) + 1  # Bounded
    nt = int(t/dt)
    x = np.linspace(0, 1, nx)
    y = np.linspace(0, 1, ny)
    X, Y = np.meshgrid(x, y)
    psi = sine(X, Y)
    zeta = sine_der(X, Y)
    zeta_nn = zeta.copy()
    zeta_n = zeta.copy()
    for n in range(nt):
        for i in range(1, nx - 1):
            for j in range(0, nx - 1):
                zeta[j, i] = zeta_nn[j, i]
                zeta[j, i] += - dt/dx * (psi[j, i+1] - psi[j, i-1])
        zeta_nn = zeta_n.copy()
        zeta_n = zeta.copy()
        psi = poisson2d_bounded(psi, zeta, dx, nx)
        if save:
            np.save(DATADIR + 'bounded/psi_{:06.2f}'.format(n), psi)
    return psi, zeta


def periodic(dx, dt, t, save=False):
    nx = int(1/dx)  # Periodic
    ny = int(1/dx) + 1  # Bounded
    nt = int(t/dt)
    x = np.linspace(0, 1 - dx, nx)
    y = np.linspace(0, 1, ny)
    X, Y = np.meshgrid(x, y)
    psi = sine(X, Y)
    zeta = sine_der(X, Y)
    zeta_nn = zeta.copy()
    zeta_n = zeta.copy()
    for n in range(nt):
        for i in range(0, nx):
            for j in range(1, ny - 1):
                zeta[j, i] = zeta_nn[j, i]
                zeta[j, i] += - dt/dx * (psi[j, (i+1) % nx] - psi[j, (i-1) % nx])
        zeta_nn = zeta_n.copy()
        zeta_n = zeta.copy()
        psi = poisson2d_periodic(psi, zeta, dx, nx)
        if save:
            np.save(DATADIR + 'periodic/psi_{:06.2f}'.format(n), psi)
    return psi, zeta


if __name__ == '__main__':
    # x = np.linspace(0, 1 - 1/40, 40)
    # y = np.linspace(0, 1, 41)
    # X, Y = np.meshgrid(x, y)
    # p = np.sin(4*np.pi*X)*np.sin(4*np.pi*Y)
    # p = sine_der(X, Y)
    # print(np.shape(p))
    # plot2d(x, y, p)
    bounded(1/40, 1, 150, save=True)
    periodic(1/40, 1, 150, save=True)
