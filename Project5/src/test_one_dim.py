import numpy as np
import one_dimension as od
import matplotlib.pyplot as plt


def relative_error(solution, approx):
    error = 0
    for i in range(0, len(solution)):
        if np.abs(solution[i]) > 1e-10:
            err = np.abs((solution[i] - approx[i])/solution[i])
            if err > error:
                error = err
    return error


def test_jacobi_1d_periodic():
    dx = 1/40
    nx = int(1/dx)
    x = np.linspace(0, 1 - dx, nx)

    n = 1
    k = 2*n*np.pi
    psi = np.zeros(nx)
    sol = -1/k**2 * np.cos(k*x)
    zeta = np.cos(k*x)
    od.poisson1d_periodic(psi, zeta, dx, nx, target=1e-8)
    # err = np.max(np.abs(sol[1:-1] - psi[1:-1]))
    relerr = relative_error(sol, psi)
    assert(relerr < 1e-2)


def test_jacobi_1d_dirichlet():
    # http://ammar-hakim.org/sj/je/je11/je11-fem-poisson.html
    dx = 1/40.
    nx = int(1/dx + 1)
    x = np.linspace(0, 1, nx)

    a = 2
    c0 = a/12 - 1/2
    c1 = 0
    s = 1 - a*x**2
    sol = x**2/2. - a*x**4/12 + c0*x + c1

    p = np.zeros(nx)
    p = od.poisson1d_bounded(p, s, dx, nx, target=1e-8, iter=1e5)
    relerr = relative_error(sol, p)
    assert(relerr < 1e-2)
    print(relerr)


def test_periodic():
    dx = 1/40
    nx = int(1/dx)
    x = np.linspace(0, 1 - dx, nx)
    t = 5
    dt = 0.1
    psi, zeta, = od.periodic(dx, t, dt=dt, init=od.sine, advance=od.centered, save=False)
    n = 2
    k = 2*np.pi*n
    omega = - 1/k
    sol = np.sin(k*x - omega*t)
    rel_err = relative_error(sol, psi)
    assert(rel_err < 1e-1)


def test_bounded():
    dx = 1/40.
    nx = int(1/dx) + 1
    x = np.linspace(0, 1, nx)
    t = 5
    n = 2
    k = np.pi*n

    dt = 0.1
    psi, zeta = od.bounded(dx, t, dt=dt, init=od.sine, advance=od.centered, save=False)
    omega = - 1/(2*k)
    sol = 2*np.sin(k*x)*np.cos(k*x - omega*t)
    rel_err = relative_error(sol, psi)
    assert(rel_err < 1e-1)


if __name__ == '__main__':
    test_bounded()
    test_periodic()
    # test_jacobi_1d_dirichlet()
    # test_jacobi_1d_periodic()
