import pandas as pd
import matplotlib.pyplot as plt


DATADIR = '../../data/'
FIGDIR = '../../figures/'

filename = DATADIR + 'montecarlo.csv'

df = pd.read_csv(filename)#, index_col=0)
print(df)

# loglog plot of standard deviation
ax1 = df.plot.scatter('N','std_importance', loglog=True, color='r', label='std_importance')
df.plot.scatter('N','std_brute',loglog=True, ax=ax1, color='b', label='std_brute')
plt.show()


# Error plot
ax2 = df.plot.scatter('N','error_importance', logx=True, color='r', label='error_importance')
df.plot.scatter('N','error_brute', ax=ax2,logx=True, color='b', label='error_brute')
plt.show()

# Plot error with bars - not very useful
# ax1 = df.plot.bar('N', 'error_importance',yerr='std_importance',alpha=0.5, align='center')
# df.plot.bar('N','error_brute',yerr='std_brute', align='center',alpha=0.5, ax=ax1, color='r')
# plt.show()


# Plot error divided by standard deviation
df['err_div_std_brute'] = df['error_brute'] / df['std_brute']
df['err_div_std_importance'] = df['error_importance'] / df['std_importance']
ax = df.plot.scatter('N','err_div_std_brute',logx=True,color='b')
df.plot.scatter('N','err_div_std_importance',logx=True, ax=ax, color='r')
plt.show()
