import numpy as np
import matplotlib.pyplot as plt
import one_dimension as od
from test_one_dim import relative_error


def error_jacobi_periodic():
    abserrors = []
    relerrors = []
    nxs = np.logspace(1, 2, 10)
    for nx in nxs:
        print(nx)
        nx = int(nx)
        # nx = int(nx)
        dx = 1/nx
        print('nx: {}, dx: {}'.format(nx, dx))
        x = np.linspace(0, 1 - dx, nx)

        n = 1
        k = 2*n*np.pi
        psi = np.zeros(nx)
        sol = -1/k**2 * np.cos(k*x)
        zeta = np.cos(k*x)
        od.poisson1d_periodic(psi, zeta, dx, nx, iter=3e4, target=1e-8)
        # err = np.max(np.abs(sol[1:-1] - psi[1:-1]))
        # relerr = relative_error(sol, psi)
        abserr = np.max(np.abs(sol - psi))
        print('Abs err jacobi 1d periodic: {}'.format(abserr))
        abserrors.append(abserr)
        relerr = relative_error(sol, psi)
        relerrors.append(relerr)
        print('Rel err jacobi 1d periodic: {}'.format(relerr))
        # plt.plot(x, sol)
        # plt.plot(x, psi)
        # plt.show()
    return abserrors, relerrors, nxs
    # plt.plot(nxs, abserrors, marker='x')
    # plt.grid()
    # plt.xscale('log')
    # plt.yscale('log')
    # plt.show()


def error_jacobi_bounded():
    abserrors = []
    relerrors = []
    nxs = np.logspace(1, 2, 10)
    for nx in nxs:

        nx = int(nx)
        dx = 1/(nx - 1)
        x = np.linspace(0, 1, nx)

        a = 2
        c0 = a/12 - 1/2
        c1 = 0
        s = 1 - a*x**2
        sol = x**2/2. - a*x**4/12 + c0*x + c1

        p = np.zeros(nx)
        p = od.poisson1d_bounded(p, s, dx, nx, target=1e-8, iter=1e5)
        relerr = relative_error(sol, p)
        abserr = np.max(np.abs(sol - p))
        print('Abs err jacobi 1d bounded: {}'.format(abserr))
        abserrors.append(abserr)
        relerrors.append(relerr)
    return abserrors, relerrors, nxs
    # plt.plot(nxs, abserrors, marker='x')
    # plt.grid()
    # plt.xscale('log')
    # plt.yscale('log')
    # plt.show()


if __name__ == '__main__':
    error_jacobi_periodic()
    error_jacobi_bounded()
