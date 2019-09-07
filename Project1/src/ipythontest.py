import pandas as pd
thomas = pd.read_csv('../data/thomas.csv')
toeplitz = pd.read_csv('../data/toeplitz.csv')
thomas
toeplitz
runtime_ratio = thomas.loc[:][' run time (s)'] / toeplitz.loc[:][' run time (s)']
runtime_ratio
runtime_ratio.plot()
pd.plot()
runtime_ratio.plot('x')
runtime_ratio.plot('--')
runtime_ratio.plot(style='--')
runtime_ratio.plot(style='o')
# %history -f ./ipythontest.py
