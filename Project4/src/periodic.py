import numpy as np
import matplotlib.pyplot as plt
L = 4

grid = np.zeros(L)
for i in range(0,L):
    grid[i] = i
print(grid)

N = 10
result = np.zeros(N)

for i in range(0,N):
    x = int(np.random.uniform()*(L))
    left = x-1
    right = x+1
    correctleft = (left % L)# - L)%L
    correctright = (right % L -L)%L
    print('left: {}, correct left: {}'.format(left, correctleft))
    print('right: {}, correct right: {}'.format(right, correctright))


    result[i] = grid[correctleft]
    # print(grid[cx])

#
# plt.hist(result)
# plt.show()
