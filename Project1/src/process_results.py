import pandas as pd
import matplotlib.pyplot as plt

# Directory for storing output
DATADIR = '../processed_data/'

# Import results
TDMA = pd.read_csv('../data/TDMA.csv', names=['TDMA'], index_col=0, header=None, skiprows=1)
TDCMAitz = pd.read_csv('../data/TDCMA.csv', names=['TDCMA'], index_col=0, header=None, skiprows=1)
lu = pd.read_csv('../data/LU_timing.csv', names=['LU'],index_col=0, header=None, skiprows=1)

# Concatenate data frames and set index name
df = pd.concat([TDMA, TDCMAitz, lu], axis=1)
df.index.name='N'

# Write summary of algorithm times
df.to_csv(DATADIR + 'algorithm_time.csv', float_format='%.3e')

# Normalize all values by n and write to file
df.div(df.index.to_series(), axis=0).to_csv(DATADIR + 'normalized.csv', float_format='%.3e')

# Compare run times and write to file
df['TDMA/TDCMA'] = df['TDMA']/df['TDCMA']
df['LU/TDCMA'] = df['LU']/df['TDCMA']
df.to_csv(DATADIR + 'comparison.csv', columns=['TDMA/TDCMA', 'LU/TDCMA'], float_format='%.3e')

# Plot relative error
error = pd.read_csv('../data/relative_error.csv', index_col=0)
error.plot(loglog=True)
plt.savefig('../figures/relative_error.png')
