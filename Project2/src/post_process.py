import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('../data/test.dat',index_col=0, header=0)
print(df)


# Groupby same index in case of data containing several runs for each n
df = df.groupby(level=0).mean()

# (df['iterations']).plot()
compare = (df['iterations']/df.index**2)
mean = compare.mean()
df['iterations'].plot(label="Iterations")
plt.plot(df.index, mean*df.index**2, label="Mean iterations n^2")
plt.legend()
plt.show()

plt.plot(mean*df.index**2 - df['iterations'])
plt.show()

# compare = (df['iterations']/df.index**3)
# compare.plot(marker='o', linestyle='')
# plt.axhline(compare.mean(),linestyle='--')
# # plt.axhline(compare.mean()-compare.std(), linestyle='--')
# # plt.axhline(compare.mean()+compare.std(), linestyle='--')
#
# # compare.mean().plot()
# plt.show()

# df['jacobi'].plot(logy=True)
# plt.show()
#
# df['armadillo'].plot(logy=True)
# plt.show()
