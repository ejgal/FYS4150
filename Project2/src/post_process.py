import pandas as pd
import matplotlib.pyplot as plt
DATADIR = '../data/'
PLOTDIR = '../figures/'

# df = pd.read_csv('../data/test.dat',index_col=0, header=0)

dfs = []
files = []
files.append(DATADIR+'3_100_3.dat')
files.append(DATADIR+'100_200_3.dat')
files.append(DATADIR+'200_250_3.dat')

for filename in files:
    df = pd.read_csv(filename, index_col=0, header=0)
    dfs.append(df)
df = pd.concat(dfs)

# Groupby same index in case of data containing several runs for each n
df = df.groupby(level=0).mean()
print(df)


pydf = pd.read_csv(DATADIR+'pythonRuns.dat', index_col=0, header=0)

print(pydf)


# Iterations divided by n**2
(df['iterations']/df.index**2).plot()
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
(df['jacobi']/df['armadillo']).plot(loglog=True)#loglog=True)
plt.grid()
plt.savefig(PLOTDIR+'compare_arma_cpp.png')
# plt.plot(df.index, df.index**(16/12.))
# plt.show()
