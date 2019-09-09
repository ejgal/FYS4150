import numpy as np
import time

def thomas(a, b, c, f, n, runs=1):
    """
    Solve the equation Av = g where A is a square tridiagonal matrix, and
    g = f * square(step_size).

    Arguments:
    a - array of size n-1 with the lower diagonal elements
    b - array of size n with the diagonal elements
    c - array of size n-1 with the upper diagonal elements
    f - function
    n - size of matrix
    runs - number of times to run the algorithm

    Returns solution v and average algorithm run time.
    """

    algo_time = 0

    for run in range(1, runs+1):
        v = np.zeros(n)
        bt = np.zeros(n)
        gt = np.zeros(n)
        x = np.linspace(0, 1, n)
        h = 1./(n+1)
        g = f(x)*h**2
        bt[0] = b[0]
        gt[0] = g[0]*a[0]/b[0]

        start_time = time.time()
        for i in range(1, n):
            bt[i] = b[i] - a[i-1] * c[i-1] / bt[i-1]
            gt[i] = g[i] - a[i-1] * gt[i-1] / bt[i-1]

        v[n-1] = gt[n-1]/bt[n-1]
        for i in reversed(range(0, n-1)):
            v[i] = (gt[i] - c[i]*v[i+1])/bt[i]
        algo_time += time.time() - start_time
    average_algo_time = algo_time / float(runs)
    return v, average_algo_time

def toeplitz(f, n, runs):
    """
    Solve the equation Av = g where A is a toeplitz matrix
    with upper and lower tridiagonal elements = -1, and
    diagonal elements = 2. g = f * square(step_size).

    Arguments:

    runs - number of times to run the algorithm


    Return solution v and algorithm run time.
    """

    algo_time = 0

    for run in range(1, runs+1):
        # initialize arrays for storing solution
        # and
        v = np.zeros(n)
        gt = np.zeros(n)
        x = np.linspace(0, 1, n)
        h = 1./(n+1)
        g = f(x)*h**2

        # Precalculate new diagonal elements
        analytic_diagonal = lambda i: (i+1)/i
        dt = analytic_diagonal(np.linspace(1, n, n))

        gt[0] = - g[0]/2.
        z = 1./dt
        start_time = time.time()
        for i in range(1, n):
            gt[i] = g[i] + gt[i-1]*z[i-1]

        v[n-1] = gt[n-1]*z[n-1]
        for i in reversed(range(0, n-1)):
            v[i] = (gt[i] + v[i+1]) * z[i]
        algo_time += time.time() - start_time
    average_algo_time = algo_time/float(runs)
    return v, average_algo_time

def build_toeplitz(a,b,c,n):
    """
    Return toeplitz matrix of size n*n

    a - constant value of lower diagonal
    b - constant value of diagonal
    c - constant value of upper diagonal
    """
    A = np.zeros(shape=(n,n))
    for i in range(0,n):
        for j in range(0,n):
            if i == j+1:
                A[i][j] = a
            if i == j-1:
                A[i][j] = c
            if i == j:
                A[i][j] = b
    return A
