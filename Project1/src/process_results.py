import pandas as pd
import matplotlib.pyplot as plt

DATADIR = '../processed_data/'


# Import results
thomas = pd.read_csv('../data/thomas.csv', names=['thomas'], index_col=0, header=None, skiprows=1)
toeplitz = pd.read_csv('../data/toeplitz.csv', names=['toeplitz'], index_col=0, header=None, skiprows=1)
lu = pd.read_csv('../data/LU_timing.csv', names=['lu'],index_col=0, header=None, skiprows=1)

# Concatenate data frames and set index name
df = pd.concat([thomas, toeplitz, lu], axis=1)
df.index.name='n'

# Write summary of algorithm times
df.to_csv(DATADIR + 'algorithm_time.csv', float_format='%.3e')

# Normalize all values by n and write to file
df.div(df.index.to_series(), axis=0).to_csv(DATADIR + 'normalized.csv', float_format='%.3e')

# Compare run times and write to file
df['thomas/toeplitz'] = df['thomas']/df['toeplitz']
df['lu/toeplitz'] = df['lu']/df['toeplitz']
df.to_csv(DATADIR + 'comparison.csv', columns=['thomas/toeplitz', 'lu/toeplitz'], float_format='%.3e')
