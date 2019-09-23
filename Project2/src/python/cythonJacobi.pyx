import numpy as np
cimport numpy as cnp
from libc.math cimport sqrt, abs
from libc.time cimport time,time_t,clock ,clock_t
from cython.view cimport array as cvarray
cimport cython

cnp.import_array()

@cython.boundscheck(False)
@cython.wraparound(False)
def create_toeplitz(double d,double a, int  N):
    cdef int i
    cdef cnp.ndarray[double, ndim=2] toeplitz = np.zeros((N,N),
    dtype=np.float64)
#    toeplitz = cvarray(shape=(N,N), itemsize=sizeof(double), format='d')
    cdef double [:,:] A = toeplitz
     
    for i in range(N):
        A[i,i] = d
    for i in range(N-1):
        A[i+1,i] = a
        A[i, i+1] = a
    return A

# Trust that I have coded it correctly, set cython to not 
@cython.boundscheck(False)
@cython.wraparound(False)
def maxElemOffDiag(double [:,:] A, int n):
    cdef double offdiagmax = 0.0
    cdef double aij
    cdef size_t i, j, row, col
    for i in range(n):
        for j in range(n):
            aij = abs(A[i,j])
            if (i!=j and aij >= offdiagmax):
                offdiagmax = aij
                row = i; col = j

    return offdiagmax, row, col

@cython.boundscheck(False)
@cython.wraparound(False)  
def jacobiRotate(double [:,:] A,int k, int l, int n): 
    cdef size_t i
    cdef double tau, t, c, s, a_kk, a_ll
    if (A[k,l] != 0.0):
        tau = (A[l,l] - A[k,k])/(2*A[k,l])

        if(tau >= 0):
            t = 1.0/(tau + sqrt(1.0 + tau*tau))
        else:
            t = -1.0/(-tau + sqrt(1.0 + tau*tau))
        c = 1/sqrt(1+t*t)
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

def jacobiRun(double[:,:] A, int N):
    cdef int n = N
    cdef int iterations = 0
    cdef int row, col
    cdef double offDiagMax = maxElemOffDiag(A, n)[0]
    while(offDiagMax > 10e-9):
        iterations += 1
        offDiagMax, row, col = maxElemOffDiag(A, n)
        A = jacobiRotate(A,row, col, n)

    return A, iterations