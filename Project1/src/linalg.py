import numpy as np

def thomas(a, b, c, f, n):
    v = np.zeros(n)
    bt = np.zeros(n)
    gt = np.zeros(n)
    x = np.linspace(0, 1, n)
    h = 1./(n+1)
    g = f(x)*h**2

    bt[0] = b[0]
    gt[0] = g[0]*a[0]/b[0]
    for i in range(1, n):
        bt[i] = b[i] - a[i-1] * c[i-1] / bt[i-1]
        gt[i] = g[i] - a[i-1] * gt[i-1] / bt[i-1]

    v[n-1] = gt[n-1]/bt[n-1]
    for i in reversed(range(0, n-1)):
        v[i] = gt[i]/bt[i+1] - c[i]*v[i+1]/bt[i+1]
    return v

def toeplitz(b, f, n):
    v = np.zeros(n)
    bt = np.zeros(n)
    gt = np.zeros(n)
    x = np.linspace(0, 1, n)
    h = 1./(n+1)
    g = f(x)*h**2

    bt[0] = b
    gt[0] = - g[0]/b

    for i in range(1, n):
        z = 1. / bt[i-1]
        bt[i] = b - z
        gt[i] = g[i] + gt[i-1]*z

    v[n-1] = gt[n-1]/bt[n-1]
    for i in reversed(range(0, n-1)):
        v[i] = (gt[i] + v[i+1]) / bt[i-1]
    return v

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
                A[i][j] = b
            if i == j:
                A[i][j] = c
    return A
