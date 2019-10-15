import numpy as np
import matplotlib.pyplot as plt

def f(r1,r2,t1,t2,phi1,phi2):
    f_value = 0
    cosbeta = np.cos(t1)*np.cos(t2) + np.sin(t1)*np.sin(t2)*np.cos(phi1-phi2)
    distance_squared = r1**2 + r2**2 - 2*r1*r2*cosbeta

    # if distance_squared > 10**-10:
    distance = np.sqrt(distance_squared)
    jacobi = r1**2*r2**2*np.sin(t1)*np.sin(t2)
    f_value = 4*np.pi**4*jacobi/(distance*16)
    return f_value


N = 100000

X = np.zeros(N)

for i in range(N):
    r1 = np.random.exponential(scale=1/4.)
    r2 = np.random.exponential(scale=1/4.)
    t1 = np.random.uniform(0,np.pi)
    t2 = np.random.uniform(0,np.pi)
    phi1 = np.random.uniform(0,2*np.pi)
    phi2 = np.random.uniform(0,2*np.pi)

    X[i] = f(r1,r2,t1,t2,phi1,phi2)

Xmean = np.sum(X)/len(X)
print(Xmean**2)
# sample_variance = (np.sum(X**2)/float(N) - Xmean**2)
# sample_variance = (np.sum(X**2) - np.sum(X))/float(N)**2
# sample_variance = np.sum(X**2)/float(N) - (np.sum(X)/float(N))**2
sample_variance = (np.sum(X**2)/float(N) - (np.sum(X)/float(N))**2)/float(N)
print('Sample variance: {}'.format(sample_variance))
print('Sample standard deviation: {}'.format(np.sqrt(sample_variance)))
print('Xmean: {}'.format(Xmean))
analytical = 5*np.pi**2/16**2
error = analytical - Xmean
print('Analytical: {:.5f}'.format(analytical))
print('Error: {:.5f}'.format(error))

import pandas as pd
df = pd.DataFrame(data=X)
var = df.var().values[-1]
X = X/float(N)
# print(df.var().values[-1]/float(N))
var = df.var().values[-1]/float(N)
print(var)
print(np.sqrt(var))
# print(df)
# df.hist()
# plt.show()
# plt.plot(np.linspace(0,1,N),X)
# plt.show()
