import numpy as np
import timeit
cimport numpy as cnp
cimport cython
from libc.math cimport sqrt, abs

from libc.time cimport clock ,clock_t

cdef class CythonJacobi:
    cdef double offdiagmax
    cdef int row, col, n, iterations
    cdef double [:,:] A
    cdef double epsilon, 
    
    @cython.profile(False)
    def __init__(self,int N ,double a, double d, double epsilon=1e-9):
        self.row = 0
        self.n = N
        self.offdiagmax = 0.0
        self.col = 0
        self.iterations = 0
        self.A = self.create_toeplitz(d, a, self.n)
        self.epsilon = epsilon
    @cython.profile(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)    
    cdef double [:,:] create_toeplitz(self,double d,double a, int  N):
        cdef int i
        cdef double [:,:] A = np.zeros((N,N), dtype=np.float64)

        for i in range(N):
            A[i,i] = d
        for i in range(N-1):
            A[i+1,i] = a
            A[i, i+1] = a
        return A

    # Trust that I have coded it correctly, set cython to not 
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.initializedcheck(False)
    cdef void maxElemOffDiag(self,double [:,:] A, int N):
        self.offdiagmax = 0
        cdef int n = N
        cdef double aij
        cdef size_t i, j
        for i in range(n):
            for j in range(i,n):
                aij = abs(A[i,j])
                if (i!=j and aij >= self.offdiagmax):
                    self.offdiagmax = aij
                    self.row = i; self.col = j
    
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.cdivision(True)
    @cython.initializedcheck(False)
    cdef void jacobiRotate(self,double [:,:] A,int k, int l, int n): 
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
    
    @cython.initializedcheck(False)
    cdef void run(self):
        self.iterations = 0
        self.maxElemOffDiag(self.A, self.n)
        while(self.offdiagmax >= self.epsilon):
            self.iterations += 1 
            self.jacobiRotate(self.A, self.row, self.col, self.n)
            self.maxElemOffDiag(self.A, self.n)

    
    cpdef void runJacobi(self):
        self.run()
    
    @property
    def getIterations(self):
        return self.iterations
    
    @property 
    def getEigenvalues(self):
        return np.sort(np.diag(self.A))
    
    def calcOffDiagMax(self, double [:,:] A, int N):
        self.maxElemOffDiag(A, N)
        return self.offdiagmax


def run(N, a, d): 
    cdef CythonJacobi run = CythonJacobi(N, a, d)
    run.runJacobi()
    return run.getIterations, run.getEigenvalues

#This function is stupid, let it be for now to have compability with 
#the other python programss
def maxElemOffDiag(double [:,:] testA, int N):
    cdef CythonJacobi maxoffdiag = CythonJacobi(10, 1, 2)
    maxoffd = maxoffdiag.calcOffDiagMax(testA, N)
    return maxoffd, None, None