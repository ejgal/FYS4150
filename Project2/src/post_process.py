import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

DATADIR = '../data/'
PLOTDIR = '../figures/'

cp5_100 = (DATADIR+'cpp_5_100.dat')
cp100_350 = (DATADIR+'cpp_100_350.dat')
py_5_100 =  (DATADIR+'python_5_100.dat')
fpy_100_350 = (DATADIR + 'fpython_100_350.dat')

dfc = pd.read_csv(cp5_100, index_col=0, header=0)

df = pd.read_csv(py_5_100, index_col=0, header=0)
df['c++'] = dfc['jacobi']
df['rel speed Numba'] = df['python']/df[' numba']
df['rel speed Cython'] = df['python']/df[' cython']
df['rel speed c++'] = df['python']/df['c++']


# Plot relative speedup compared to python
matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)
a = np.unique(df['rel speed c++'].keys())
plt.figure(figsize=(16,10))
for key in a:
#     plt.errorbar(key,df['rel speed c++'][key].mean(), df['rel speed c++'][key].std(),color ='grey')
    plt.scatter(key,df['rel speed c++'][key].mean(), marker = 'x', s=70,color = 'slateblue')
#     plt.errorbar(key,df['rel speed Cython'][key].mean(), df['rel speed Cython'][key].std(), color ='grey')
    plt.scatter(key,df['rel speed Cython'][key].mean(), marker = '^',s=70, color = 'darkviolet')
    plt.scatter(key,df['rel speed Numba'][key].mean(), marker = '+', s=70 ,color = 'purple')
#     plt.errorbar(key,df['rel speed Numba'][key].mean(), df['rel speed Numba'][key].std(), color ='grey')
# plt.title('Average Speedup compared to Python', )
plt.legend(('c++', 'cython', 'numba'), prop={'size': 14})
plt.xlabel('N', fontsize=18)
plt.ylabel('Relative Speedup compared to python',fontsize=18)
plt.grid()
plt.savefig(PLOTDIR+'avgspeed.png',dpi =140)






# Plot speeds of c++ cython and numba for large n
dfc = pd.read_csv(cp100_350, index_col=0, header=0)
df1 = pd.read_csv(DATADIR + 'fpython_100_350.dat', index_col=0, header=0)
df1['c++'] = dfc['jacobi']
# df.keys()
a = np.unique(df1['c++'].keys())
plt.figure(figsize=(16,10))

for key in a:
    plt.scatter(key, df1['c++'][key].mean(), marker ='x',s=70 ,color = 'slateblue')
    plt.scatter(key, df1[' numba'][key].mean(), marker='+',s=70, color = 'indigo')
    plt.scatter(key,df1[' cython'][key].mean(), marker ='^',s=70 ,color ='darkviolet')
plt.legend(('c++', 'cython', 'numba'), prop={'size': 14})
plt.grid()
plt.xlabel('N', fontsize=18)
plt.ylabel('Seconds',fontsize=18)
plt.savefig(PLOTDIR+'speedComp_100_350.png',dpi =140)


# Plot relative speedup compared to c++
df1['rel speed Numba'] = df1['c++']/df1[' numba']
df1['rel speed Cython'] = df1['c++']/df1[' cython']
plt.figure(figsize=(16,10))
for key in a:
    plt.scatter(key, df1['rel speed Numba'][key].mean(), marker='+',s=70, color = 'indigo')
    plt.scatter(key,df1['rel speed Cython'][key].mean(), marker ='^',s=70 ,color ='darkviolet')

plt.legend(('numba', 'cython'), prop={'size': 14})
plt.xlabel('N', fontsize=18)
plt.ylabel('Relative Speedup compared to c++',fontsize=18)
plt.grid()
plt.savefig(PLOTDIR+'speedCompC++_100_350.png',dpi=140)



# Analyze c++ and armadillo run times
dfs = []
for filename in [cp5_100, cp100_350]:
    df = pd.read_csv(filename, index_col=0, header=0)
    dfs.append(df)
df = pd.concat(dfs)

# Groupby same index in case of data containing several runs for each n
df = df.groupby(level=0).mean()


# Iterations divided by n**2
plt.clf()
plt.scatter(df.index ,df['iterations']/df.index**2)
plt.grid()
plt.savefig(PLOTDIR + 'iterations_compare_n2.png')

# Find value that iterations/n**2 converges to
mean = (df.loc[200:,'iterations']/df.loc[200:,'iterations'].index**2).mean()
print('Mean: {}'.format(mean))

# Number of iterations
plt.clf()
df['iterations'].plot(label='Iterations')
plt.plot(df.index, mean*df.index**2, label='{:.3f}n^2'.format(mean),linestyle='--')
plt.grid()
plt.ylabel('Iterations')
plt.legend()
plt.savefig(PLOTDIR+'iterations.png')
plt.clf()



plt.clf()
plt.scatter(df.index, df['jacobi']/df['armadillo'])
# (df['jacobi']/df['armadillo']).plot(loglog=True)#loglog=True)
plt.grid()
plt.savefig(PLOTDIR+'compare_arma_cpp.png')
