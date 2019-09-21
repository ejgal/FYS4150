import numpy as np
import jacobi
def __calAnalyticEigenVals(d, a, N):
    x = np.zeros(N)
    for i in range(1,N+1):
        x[i-1] = d + 2*a*np.cos((i*np.pi)/(N+1))
    return x

 def test_MaxElemOffDiag():
    np.random.seed(126)
    A = np.array([[1,4],[4,1]])

    A = create_toeplitz(-1,2,10)

    rand_mat = np.random.randint(1,100,(4,4)).astype(float)
    rand_mat[3,3] = 99 #Diagonal element has the highest values, 
    rand_mat[3,2] = 98
    assert cmaxElemOffDiag(rand_mat)[0] == 98

def test_rotation():

    A = np.array([[3,2,4,5],
                     [2,5,3,4],
                     [4,3,2,6],
                     [5,4,6,2]])
    Before = np.copy(A)[0:2,0:2]
    RotA = jacobiRotate(A,3,2)
    Unchanged = RotA[0:2,0:2]
    for i in range(2):
        for j in range(2):
            assert Before[i,j] == Unchanged[i,j]

def test_Eigenvalues():
    N = 20


    h = 1./(N)
    d = 2./(h**2)
    a = -1./(h**2)
    eigValsAnalytic =  calAnalyticEigenVals(d, a, N)

    A = jacobi.cCreate_toeplitz(d, a, N)
    start = np.copy(A)
    offDiagMax = jacobi.cMaxElemOffDiag(A)[0]
    iterations = 0
    while(offDiagMax > 10e-9):
        iterations += 1
        offDiagMax, row, col = jacobi.cMaxElemOffDiag(A)
        A =jacobi.cJacobiRotate(A,row, col)
    
    eigValsAnalytic = __calAnalyticEigenVals(d, a, N)
    
    assert np.sum(np.sort(np.diag(A)) - eigValsAnalytic) < 10e-9

test_Eigenvalues()


if __name__ == "__main__":
    #test_MaxElemOffDiag()
    #test_rotation()
    test_Eigenvalues()
    
