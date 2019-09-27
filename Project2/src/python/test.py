import numpy as np
import numbaJacobi
import pythonJacobi
import pytest
import cythonJacobi

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
    rand_mat[2,3] = 98
    N = rand_mat.shape[0]
    assert prog.maxElemOffDiag(rand_mat,N)[0] == 98

testsetup = [(cythonJacobi, 200),
             (numbaJacobi, 200),
              (pythonJacobi, 20)]

@pytest.mark.parametrize("prog, N" , testsetup)
def test_Eigenvalues(prog, N):
    N = N

    h = 1./(N)
    d = 2./(h**2)
    a = -1./(h**2)
    eigValsAnalytic =  __calAnalyticEigenVals(d, a, N)
    calcEigVals = np.sort(prog.run(N, a, d)[1])

    assert np.allclose(calcEigVals, eigValsAnalytic)
    
