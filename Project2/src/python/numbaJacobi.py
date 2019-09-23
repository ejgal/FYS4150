from numba import jit
import numpy as np

@jit(nopython=True) 
def create_toeplitz(d, a,N):
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = d
    for i in range(N-1):
        A[i+1,i] = a
        A[i, i+1] = a
    
    return A

@jit(nopython=True) 
def maxElemOffDiag(A ,N):
    offdiagmax = 0.0
    n = N
    for i in range(n):
        for j in range(n):
            aij = np.abs(A[i,j])
            if (i!=j and aij >= offdiagmax):
                offdiagmax = aij
                row = i; col = j;

    return offdiagmax, row, col


@jit(nopython=True) 
def jacobiRotate(A, k, l, N): 
    n = N
    if (A[k,l] != 0.0):
        tau = (A[l,l] - A[k,k])/(2*A[k,l])

        if(tau >= 0):
            t = 1.0/(tau + np.sqrt(1.0 + tau*tau))
        else:
            t = -1.0/(-tau + np.sqrt(1.0 + tau*tau))
        c = 1/np.sqrt(1+t*t)
        s = c*t
    else:
        c = 1.0
        s = 0.0
    a_kk = A[k,k]
    a_ll = A[l,l]
    A[k,k] = c*c*a_kk - 2.0*c*s*A[k,l] + s*s*a_ll #Adding shit to the diagonals
    A[l,l] = s*s*a_kk + 2.0*c*s*A[k,l] + c*c*a_ll
    A[k,l] = 0.0  #Since our matrix is symmetric
    A[l,k] = 0.0
    for i in range(n):
        if (i != k and i != l):
            a_ik = A[i,k]
            a_il = A[i,l]
            A[i,k] = c*a_ik - s*a_il
            A[k,i] = A[i,k]
            A[i,l] = c*a_il + s*a_ik
            A[l,i] = A[i,l]
    return A

def jacobiRun(A, N):
    interations = 0
    offDiagMax = maxElemOffDiag(A, N)[0]
    while(offDiagMax > 10e-9):
        interations += 1
        offDiagMax, row, col = maxElemOffDiag(A,N)
        A = jacobiRotate(A,row,col,N)
    return A, interations