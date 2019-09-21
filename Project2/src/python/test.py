import numpy as np


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


if __name__ == "__main__":
    test_MaxElemOffDiag()
    test_rotation()
    
