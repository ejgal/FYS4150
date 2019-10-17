import numpy as np
import matplotlib.pyplot as plt

def f(x1,y1,z1,x2,y2,z2):
    f_value = 0
    r1 = np.sqrt(x1**2+y1**2+z1**2)
    r2 = np.sqrt(x2**2+y2**2+z2**2)
    distance_squared = (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2
    distance = np.sqrt(distance_squared)
    f_value = np.exp(-4*(r1+r2))/distance
    return f_value



N = 100000

X = np.zeros(N)

a = -2
b = 2

for i in range(N):
    x1 = np.random.uniform(a,b)
    y1 = np.random.uniform(a,b)
    z1 = np.random.uniform(a,b)
    x2 = np.random.uniform(a,b)
    y2 = np.random.uniform(a,b)
    z2 = np.random.uniform(a,b)

    X[i] = f(x1,y1,z1,x2,y2,z2)

X = X*4**6
Xmean = np.sum(X)/len(X)
# sample_variance = np.sum(X)/float(N) - Xmean**2
# sample_variance = np.sum(X**2)/float(N**2) - Xmean**2/float(N)
# sample_variance = (np.sum(X**2) - np.sum(X))/float(N)#**2
sample_variance = (np.sum(X**2)/float(N) - (np.sum(X)/float(N))**2)/float(N)

print('Sample variance: {}'.format(sample_variance))
print('Sample standard deviation: {}'.format(np.sqrt(sample_variance)))
print('Xmean: {}'.format(Xmean))
analytical = 5*np.pi**2/16**2
error = analytical - Xmean
print('Analytical: {:.5f}'.format(analytical))
print('Error: {:.5f}'.format(error))

import pandas as pd
df = pd.DataFrame(data=X/float(N))
print(df.var())
print(df.std())

# plt.plot(np.linspace(0,1,N),X)
# plt.show()
