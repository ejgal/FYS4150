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
df = pd.read_csv('../data/longrun4.csv')
```

```python
df.plot('T','cv')
```

```python
df.loc[(df['spins']==10000) & (df['T'].between(2.24,2.30))].plot('T','cv',linestyle='--')
df.loc[(df['spins']==10000) & (df['T'].between(2.24,2.30)),'cv'].var()


sel = df.loc[df['spins']==10000]
poly = np.polyfit(sel['T'],sel['cv'],4)

# print(poly)
Tmin = df['T'].min()
Tmax = df['T'].max()
T = np.linspace(2.25,2.35,100)
polynom = np.poly1d(poly)
plt.plot(T, polynom(T))
cvmax = (polynom(T).max())
plt.axhline(cvmax)
print(np.argmax(polynom(T)))
print(T[25])
# print(sel.loc[df['cv']==cvmax, 'is_closest'])

# plt.plot(sel['T']*1150**3 + sel['T']**2*(-1954) + sel['T']*1052 -182)
```
