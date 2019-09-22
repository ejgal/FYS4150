import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('../data/test.dat',index_col=0, header=0)
print(df)


# Groupby same index
df = df.groupby(level=0).mean()
print(df['iterations']/df.index**2)

df['jacobi'].plot(logy=True)
# df['armadillo'].plot(logy=True)
plt.show()

(df['jacobi']/df['armadillo']).plot(logy=True)
plt.show()
