import numpy as np
import cythonJacobi_test
import numbaJacobi
import pythonJacobi
import pytest
import cythonJacobi

def __calAnalyticEigenVals(d, a, N):
    x = np.zeros(N)
    for i in range(1,N+1):
        x[i-1] = d + 2*a*np.cos((i*np.pi)/(N+1))
    return x
@pytest.mark.parametrize("prog", [cythonJacobi_test, numbaJacobi, pythonJacobi])
def test_MaxElemOffDiag(prog):

    np.random.seed(126)

    rand_mat = np.random.randint(1,100,(4,4)).astype(float)
    rand_mat[3,3] = 99 #Diagonal element has the highest values, 
    rand_mat[2,3] = 98
    N = rand_mat.shape[0]
    assert prog.maxElemOffDiag(rand_mat,N)[0] == 98

testsetup = [(cythonJacobi_test, 200, True),
             (numbaJacobi, 200, False),
              (pythonJacobi, 20, False)]

@pytest.mark.parametrize("prog, N, Cython" , testsetup)
def test_Eigenvalues(prog, N, Cython):
    N = N

    h = 1./(N)
    d = 2./(h**2)
    a = -1./(h**2)
    eigValsAnalytic =  __calAnalyticEigenVals(d, a, N)
    if Cython:
        calcEigVals = np.sort(prog.run(N, a, d)[1])
    else:
        A = prog.create_toeplitz(d, a, N)
        offDiagMax = prog.maxElemOffDiag(A,N)[0]
        iterations = 0
        while(offDiagMax > 1e-9):
            iterations += 1
            offDiagMax, row, col = prog.maxElemOffDiag(A, N)
            A =prog.jacobiRotate(A,row, col, N)
        calcEigVals = np.sort(np.diag(A))
    
    assert np.allclose(calcEigVals, eigValsAnalytic)
    
