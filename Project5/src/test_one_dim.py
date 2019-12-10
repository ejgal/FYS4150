import numpy as np
import one_dimension as od
import matplotlib.pyplot as plt


def test_jacobi_1d_periodic():
    dx = 1/40
    nx = int(1/dx)
    x = np.linspace(0, 1 - dx, nx)

    n = 1
    k = 2*n*np.pi
    psi = np.zeros(nx)
    sol = -1/k**2 * np.cos(k*x)
    zeta = np.cos(k*x)
    od.poisson1d_periodic(psi, zeta, dx, nx, target=1e-6)
    err = np.max(np.abs(sol[1:-1] - psi[1:-1]))
    print(err)
    print(sol)


def test_jacobi_1d_dirichlet():
    # http://ammar-hakim.org/sj/je/je11/je11-fem-poisson.html
    dx = 1/40.
    nx = int(1/dx + 1)
    x = np.linspace(0, 1, nx)

    a = 2
    c0 = a/12 - 1/2
    c1 = 0
    s = 1 - a*x**2

    p = np.zeros(nx)
    p = od.poisson1d_bounded(p, s, dx, nx, target=1e-8, iter=1e5)
    psi = x**2/2. - a*x**4/12 + c0*x + c1
    relerr = np.max(np.abs(psi[1:-1] - p[1:-1])/psi[1:-1])
    assert(relerr > 1e-15)


if __name__ == '__main__':

    test_jacobi_1d_dirichlet()
    test_jacobi_1d_periodic()
