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
# plt.rc('figure', figsize=(14,10))
import warnings
warnings.filterwarnings('ignore')
import analytic as a
```

```python
def plot_relative_error(datafile,T = 1.0,L=2,window=1,ordered=0):
    df = pd.read_csv(datafile)
    cv = a.cv(T)/L**2
    E = a.expected_energy(T)/L**2
    Mabs = a.expected_magnetization(T)/L**2
    suscept = a.susceptibility(T)/L**2


    sel = df.loc[(df['T'] == T) & (df['ordered']==ordered)]
    sel['compare_cv'] = np.abs(sel['cv'] - cv)/np.abs(cv)
    sel['compare_E'] = np.abs(sel['E'] - E)/np.abs(E)
    sel['compare_Mabs'] = np.abs(sel['Mabs'] - Mabs)/np.abs(Mabs)
    sel['compare_suscept'] = np.abs(sel['suscept'] - suscept)/np.abs(suscept)
    
    

    fig, ax = plt.subplots(1)
    ax.tick_params(left=True,right=True,which='both')
    ax.tick_params(labelleft =True, labelright=True)
    cols = ['compare_E','compare_cv','compare_Mabs','compare_suscept']
    
    for col in cols:
        sel.rolling(window).mean().plot('cycles',col,linestyle='--',logx=True,logy=True, ax=ax)
    plt.grid()
    plt.title('ordered: {} T: {}'.format(ordered, T))

```

```python
win = 5
file = '../data/equi_L2_large_6_delay.csv'
plot_relative_error(file,T=1.0,window=win)

file2 = '../data/equi_L2_large_6.csv'
plot_relative_error(file2,T=1.0,window=win)
```
