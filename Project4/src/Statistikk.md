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
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline
```

```python
df = pd.read_csv('../../data/equi_long3.csv')
df
```

```python

df['E'] = np.abs(df['E'])
sel = df.loc[(df['ordered']==0) & (df['T']==2.4)]
sel.plot('cycles','E',logx=True,logy=True)

sel.plot('cycles','suscept',logx=True,logy=True)
sel.plot('cycles','cv',logx=True,logy=True)
```

```python

fig, ax = plt.subplots(1)
fig,ax2 = plt.subplots(1)
for L in [40,60,80,100]:
    sel = df.loc[df['spins']==L**2]
    print(sel.std())
    sel.plot('T','cv',ax=ax)
    sel.plot('T','Mabs',ax=ax2)

```
