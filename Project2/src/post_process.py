import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


# Plot style
mpl.rc('xtick', labelsize=16)
mpl.rc('ytick', labelsize=16)
mpl.rc('figure', figsize=[16,10])
mpl.rc('legend', fontsize=14)
mpl.rc('axes', labelsize=18)
mpl.rc('savefig', dpi=140)

# Set directories
DATADIR = '../data/'
PLOTDIR = '../figures/'

# Set data files
cp5_100 = (DATADIR+'cpp_5_100.dat')
cp100_350 = (DATADIR+'cpp_100_350.dat')
py_5_100 =  (DATADIR+'python_5_100.dat')
fpy_100_350 = (DATADIR + 'fpython_100_350.dat')





# Calculate and plot relative speedup compared to python
dfc = pd.read_csv(cp5_100, index_col=0, header=0)
df = pd.read_csv(py_5_100, index_col=0, header=0)

df['c++'] = dfc['jacobi']
df['rel speed Numba'] = df['python']/df[' numba']
df['rel speed Cython'] = df['python']/df[' cython']
df['rel speed c++'] = df['python']/df['c++']

a = np.unique(df['rel speed c++'].keys())
plt.clf()
for key in a:
    plt.scatter(key,df['rel speed c++'][key].mean(), marker = 'x', s=70,color = 'slateblue')
    plt.scatter(key,df['rel speed Cython'][key].mean(), marker = '^',s=70, color = 'darkviolet')
    plt.scatter(key,df['rel speed Numba'][key].mean(), marker = '+', s=70 ,color = 'purple')
plt.legend(('c++', 'cython', 'numba'))
plt.xlabel('N')
plt.ylabel('Relative Speedup compared to python')
plt.grid()
plt.savefig(PLOTDIR+'avgspeed.png')




# Plot speeds of c++, cython and numba for large N
dfc = pd.read_csv(cp100_350, index_col=0, header=0)
df1 = pd.read_csv(DATADIR + 'fpython_100_350.dat', index_col=0, header=0)
df1['c++'] = dfc['jacobi']

a = np.unique(df1['c++'].keys())
plt.clf()
for key in a:
    plt.scatter(key, df1['c++'][key].mean(), marker ='x',s=70 ,color = 'slateblue')
    plt.scatter(key, df1[' numba'][key].mean(), marker='+',s=70, color = 'indigo')
    plt.scatter(key,df1[' cython'][key].mean(), marker ='^',s=70 ,color ='darkviolet')
plt.legend(('c++', 'cython', 'numba'))
plt.grid()
plt.xlabel('N')
plt.ylabel('Seconds')
plt.savefig(PLOTDIR+'speedComp_100_350.png')


# Calculate and plot relative speedup compared to c++
df1['rel speed Numba'] = df1['c++']/df1[' numba']
df1['rel speed Cython'] = df1['c++']/df1[' cython']
plt.clf()
for key in a:
    plt.scatter(key, df1['rel speed Numba'][key].mean(), marker='+',s=70, color = 'indigo')
    plt.scatter(key,df1['rel speed Cython'][key].mean(), marker ='^',s=70 ,color ='darkviolet')
plt.legend(('numba', 'cython'))
plt.xlabel('N')
plt.ylabel('Relative Speedup compared to c++')
plt.grid()
plt.savefig(PLOTDIR+'speedCompC++_100_350.png')
plt.clf()

# Analyze c++ and armadillo run times
dfs = []
for filename in [cp5_100, cp100_350]:
    df = pd.read_csv(filename, index_col=0, header=0)
    dfs.append(df)
df = pd.concat(dfs)
df = df.groupby(level=0).mean()

# Plot comparison of jacobis method and eig_sym
plt.scatter(df.index, df['jacobi']/df['armadillo'])
plt.grid()
plt.savefig(PLOTDIR+'compare_arma_cpp.png')
plt.clf()

# Find value that iterations/n**2 converges to
mean = (df.loc[200:,'iterations']/df.loc[200:,'iterations'].index**2).mean()

# Plot iterations divided by n**2
scaled = df['iterations']/df.index**2
plt.scatter(df.index ,scaled, marker='x', s=70, color='slateblue', label='c++')
plt.axhline(mean, label='{:.2f}'.format(mean))

plt.legend()
plt.xlabel('N')
plt.ylabel(r'Iterations/N$^2$')
plt.grid()
plt.savefig(PLOTDIR + 'iterations_compare_n2.png')
plt.clf()


# Number of iterations
plt.scatter(df.index ,df['iterations'], marker='x', s=70, color='slateblue')
# plt.plot(df.index, mean*df.index**2, label='{:.3f}n^2'.format(mean),linestyle='--')
plt.grid()
plt.ylabel('Iterations')
plt.legend(['Iterations c++'])
# ax = plt.gca()
# ax.set_yscale('log')
plt.savefig(PLOTDIR+'iterations.png')
plt.clf()
