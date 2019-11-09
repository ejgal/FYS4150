---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.2.4
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- #region {"toc": true} -->
<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"></ul></div>
<!-- #endregion -->

```python
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
%matplotlib inline
```

```python
from glob import glob
files = glob('../data/dist_20_600000_*')
for file in sorted(files[:]):
    print(file)
```

```python
# df.rolling(10000).mean().plot()
# df.plot(kind='hist')

df = pd.read_csv('../data/dist_20.csv')
index = []
for T in df['T']:
    index.append('{:.2f}'.format(T))
df.index = index
print(df.loc[:,'cv'])

    
df2 = pd.read_csv('../data/dist_dist.csv',index_col=0)


num_bins = int(1+3.3*np.log(len(df2)))
for T in df.index:
    label = 'T={} ,cv={:.2f}'.format(T,df.loc[T,'cv'])
    df2[T].hist(density=True, bins=num_bins,label=label, alpha=0.8)
# df2.hist(density=True, bins=num_bins,label='awd')
plt.legend()
plt.yscale('log')
# fig, ax = plt.subplots(1)
# files = sorted(glob('../data/dist_20_*'))
# dists = []
# for file in files:
#     dist = np.load(file)
#     dists.append(dist)
# #     df = pd.DataFrame(dist)
# #     df = df/20**2
# #     num_bins = int(1+3.3*np.log(len(df)))
# #     df.hist(density=True, bins=num_bins,ax=ax,alpha=0.5)
# print(pd.DataFrame(dists.transpose()))


```

```python

df2 = pd.read_csv('../data/dist_dist.csv',index_col=0)
mean = np.abs(df2.rolling(1000).mean())

```

```python
import seaborn as sns
corr = df2.corr()
display(corr)
corr = np.log(corr)
sns.heatmap(corr)
```

```python
df = pd.read_csv('../data/equi_long2.csv')
```

```python
df['ratio'] = df['accepted']/(df['spins']*df['cycles'])

ratio1 = df.loc[(df['T']==1.0) & (df['ordered']==1)]
ratio2 = df.loc[(df['T']==2.4) & (df['ordered']==1)]
fig, ax = plt.subplots(1)
ratio1.plot('cycles','ratio',ax=ax,logx=True)
ratio2.plot('cycles','ratio',ax=ax,logx=True)
```

```python
mean = df.loc[(df['ordered']==1)].groupby('T').mean()
print(mean)
print(mean.index)
mean.plot(mean.index,'ratio')
```

```python
%matplotlib notebook
df = pd.read_csv('../data/longrun2.csv')
df['ratio'] = df['accepted']/(df['spins']*df['cycles'])


print(df.max())

ratio2 = df.loc[(df['T']==2.4) & (df['ordered']==1)]
fig, ax = plt.subplots(1)
df.loc[df['spins']==10000].plot('T','ratio')
# df.plot('T','ratio',logx=True,logy=True, ax=ax)
# df['line'] = df['T']
# df.plot('T','line',ax=ax)
# df.plot('T','cv',ax=ax)
plt.axvline(2.269)
```

```python
df = pd.read_csv('../data/longrun2.csv')
df['ratio'] = df['accepted']/(df['spins']*df['cycles'])
display(df.loc[df['spins']==10000].max())
```
