import numpy as np
import cythonJacobi
import numbaJacobi
import pythonJacobi
import pytest


def __calAnalyticEigenVals(d, a, N):
    x = np.zeros(N)
    for i in range(1,N+1):
        x[i-1] = d + 2*a*np.cos((i*np.pi)/(N+1))
    return x
@pytest.mark.parametrize("prog", [cythonJacobi, numbaJacobi, pythonJacobi])
def test_MaxElemOffDiag(prog):

    np.random.seed(126)

    rand_mat = np.random.randint(1,100,(4,4)).astype(float)
    rand_mat[3,3] = 99 #Diagonal element has the highest values, 
    rand_mat[3,2] = 98
    N = rand_mat.shape[0]
    assert prog.maxElemOffDiag(rand_mat,N)[0] == 98
@pytest.mark.parametrize("prog", [cythonJacobi, numbaJacobi, pythonJacobi])
def test_rotation(prog):

    A = np.array([[3,2,4,5],
                    [2,5,3,4],
                    [4,3,2,6],
                    [5,4,6,2]]).astype(float)
    Before = np.copy(A)[0:2,0:2]
    N = A.shape[0]
    RotA = prog.jacobiRotate(A,3,2,N)
    Unchanged = RotA[0:2,0:2]
    for i in range(2):
        for j in range(2):
            assert Before[i,j] == Unchanged[i,j]
@pytest.mark.parametrize("prog", [cythonJacobi, numbaJacobi, pythonJacobi])
def test_Eigenvalues(prog):
    N = 20


    h = 1./(N)
    d = 2./(h**2)
    a = -1./(h**2)
    eigValsAnalytic =  __calAnalyticEigenVals(d, a, N)

    A = prog.create_toeplitz(d, a, N)
    offDiagMax = prog.maxElemOffDiag(A,N)[0]
    iterations = 0
    while(offDiagMax > 10e-9):
        iterations += 1
        offDiagMax, row, col = prog.maxElemOffDiag(A, N)
        A =prog.jacobiRotate(A,row, col, N)
    eigValsAnalytic = __calAnalyticEigenVals(d, a, N)
    
    assert np.sum(np.sort(np.diag(A)) - eigValsAnalytic) < 10e-6


if __name__ == "__main__":
    versions = [cythonJacobi, numbaJacobi, pythonJacobi]
    for version in versions:
        test_MaxElemOffDiag(version)
        test_rotation(version)
        test_Eigenvalues(version)
    
