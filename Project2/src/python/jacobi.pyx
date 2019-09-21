import numpy as np
cimport numpy as np
from libc.math cimport sqrt, abs
from libc.time cimport time,time_t,clock ,clock_t
cimport cython

np.import_array()

@cython.boundscheck(False)
@cython.wraparound(False)
def cCreate_toeplitz(double d,double a,int  N):
    cdef size_t i
    cdef np.ndarray[double, ndim=2] toeplitz = np.empty((N,N)) 
    cdef double [:,:] A = toeplitz 
    for i in range(N):
        A[i,i] = d
    for i in range(N-1):
        A[i+1,i] = a
        A[i, i+1] = a
    
    return toeplitz

# Trust that I have coded it correctly, set cython to not 
@cython.boundscheck(False)
@cython.wraparound(False)
def cMaxElemOffDiag(double [:,:] A):
    cdef double offdiagmax = 0.0
    cdef double aij
    cdef size_t n = A.shape[0]
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
def cJacobiRotate(double [:,:] A,int k, int l): 
    cdef int n = A.shape[0]
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

def jacobiRun(double [:,:] A):
    cdef int iterations = 0
    cdef size_t row, col
    cdef double offDiagMax = cMaxElemOffDiag(A)[0]
    while(offDiagMax > 10e-9):
        iterations += 1
        offDiagMax, row, col = cMaxElemOffDiag(A)
        A = cJacobiRotate(A,row, col)
    return iterations ,A