import pandas as pd
import matplotlib.pyplot as plt
DATADIR = '../data/'
PLOTDIR = '../figures/'

df = pd.read_csv('../data/test.dat',index_col=0, header=0)


# Groupby same index in case of data containing several runs for each n
df = df.groupby(level=0).mean()
print(df)


# Number of iterations versus n
df['iterations'].plot(loglog=True,label='Iterations')
plt.grid()
plt.legend()
plt.title('Iterations needed for minimizing all nondiagonal elements below 10^-8')
plt.savefig(PLOTDIR+'iterations.png')

#
# compare = (df['iterations']/df.index**2)
# mean = compare.mean()
# df['iterations'].plot(label="Iterations")
# plt.plot(df.index, mean*df.index**2, label="Mean iterations n^2")
# plt.legend()
# plt.show()






# compare = (df['iterations']/df.index**3)
# compare.plot(marker='o', linestyle='')
# plt.axhline(compare.mean(),linestyle='--')
# # plt.axhline(compare.mean()-compare.std(), linestyle='--')
# # plt.axhline(compare.mean()+compare.std(), linestyle='--')

# # compare.mean().plot()
# plt.show()

# df['jacobi'].plot(logy=True)
# plt.show()
#

# df['jacobi'].plot()
# df['armadillo'].plot()
# (df['jacobi']/df['armadillo']).plot()
plt.clf()
(df['jacobi']/df['armadillo']).plot(loglog=True)
plt.grid()
plt.show()
# plt.plot(df.index, df.index**(16/12.))
# plt.show()
#
