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
<div class="toc"><ul class="toc-item"><li><span><a href="#Hovmuller" data-toc-modified-id="Hovmuller-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Hovmuller</a></span></li><li><span><a href="#Periodic" data-toc-modified-id="Periodic-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Periodic</a></span><ul class="toc-item"><li><span><a href="#Sine" data-toc-modified-id="Sine-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Sine</a></span></li><li><span><a href="#Gaussian" data-toc-modified-id="Gaussian-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Gaussian</a></span></li></ul></li><li><span><a href="#Bounded" data-toc-modified-id="Bounded-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Bounded</a></span></li><li><span><a href="#Stability" data-toc-modified-id="Stability-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Stability</a></span></li></ul></div>
<!-- #endregion -->

```python
import numpy as np
import matplotlib.pyplot as plt
%matplotlib notebook
import pandas as pd
```

```python
# x = np.linspace(0, 1, 40)
n = 1
k = 2*n*np.pi
plt.plot(x, np.sin(n*np.pi*x))
plt.plot(x, np.cos(k*x))
plt.plot(x, np.sin(n*np.pi*x)*np.cos(k*x))
```

```python
x = np.linspace(0, 1, 40)
n = 1
k = 2*n*np.pi
plt.plot(x, np.cos(k*x))
```

```python
def compare(filename, times = [0, 10, 20, 30]):
    psi = pd.read_csv(filename, header=None, index_col=0, skiprows=6)
    print('max psi: {}'.format(np.max(psi.iloc[-1,:])))
    for t in times:
        psi.iloc[t,:].plot(label='t={}'.format(t))
    plt.legend()
    plt.grid()
```

```python
compare('../data/psi_periodic_gauss_0.08.csv', times=[100, 200, 300])
```

```python
psi = pd.read_csv('../data/psi_periodic_gauss_0.10.csv', header=None, skiprows=6, index_col=0)
psi.iloc[1400,:].plot()
```

```python
psi = pd.read_csv('../data/psi_bounded_centered_sine.csv', header=None, skiprows=6, index_col=0)
psi.iloc[0,:].plot()
psi.iloc[1200,:].plot()
```

```python
psi = pd.read_csv('../data/psi_bounded_centered_gauss.csv', header=None, skiprows=6, index_col=0)

for n in [0, 1200, 1400]:
    np.abs(psi.iloc[n,:]).plot()
```

```python
for n in [0, 300, 500,1200, 1400]:
    jn = psi.iloc[n, 1:]
    jnn = psi.iloc[n, 0:-1]
    plt.plot((jn.values-jnn.values)**2)
#     print(np.sum((jn.values-jnn.values)**2))
```

```python
psi = pd.read_csv('../data/psi_periodic_gauss_0.08.csv', header=None, skiprows=6, index_col=0)
psi.iloc[0,:].plot()
psi.iloc[1200,:].plot()
plt.plot(psi.iloc[])
```

```python
# Stable long timestep
psi = pd.read_csv('../data/psi_long_centered_stable.csv', header=None, index_col=0, skiprows=6)
plt.plot(psi.index,np.max(psi.values, axis=1), linestyle=' ', marker='s')

# Unstable long timestep
psi = pd.read_csv('../data/psi_long_centered_unstable.csv', header=None, index_col=0, skiprows=6)
plt.plot(psi.index, np.max(psi.values, axis=1), linestyle=' ', marker='x')

```

```python
# !ls -l ../data | grep long
# psi = pd.read_csv('../data/psi_long_forward_008.csv', header=None, index_col=0, skiprows=6)
# plt.plot(np.max(psi, axis=1))

psi = pd.read_csv('../data/psi_long_forward_008.csv', header=None, index_col=0, skiprows=6)
plt.plot(np.max(np.abs(psi), axis=1), label='FTCS, dt=0.08')
psi = pd.read_csv('../data/psi_long_forward_005.csv', header=None, index_col=0, skiprows=6)
plt.plot(np.max(np.abs(psi), axis=1), label='FTCS, dt=0.05')
psi = pd.read_csv('../data/psi_long_centered.csv', header=None, index_col=0, skiprows=6)
plt.plot(np.max(np.abs(psi), axis=1), label='CTCS, dt=1', alpha=0.7)
plt.grid()
plt.legend()
plt.xscale('log')
# psi = pd.read_csv('../data/psi_long_centered_stable.csv', header=None, index_col=0, skiprows=6)
# plt.plot(np.max(psi, axis=1))

# psi = pd.read_csv('../data/psi_long_centered_stable.csv', header=None, index_col=0, skiprows=6)
# plt.plot(np.max(psi, axis=1))

# psi = pd.read_csv('../data/psi_long_centered_unstable.csv', header=None, index_col=0, skiprows=6)
# plt.plot(np.max(psi, axis=1))



```

```python

fig, ax = plt.subplots(1, sharex=True, sharey=True, figsize=[8,8])
# psi = pd.read_csv('../data/psi_long_centered_stable.csv', header=None, index_col=0, skiprows=6)
# ax1.plot(np.max(np.abs(psi), axis=1))


stable_psi = pd.read_csv('../data/psi_stable_long.csv', header=None, index_col=0, skiprows=6)
ax.plot(np.max(np.abs(stable_psi), axis=1), label='dt=0.9')

# psi = pd.read_csv('../data/psi_long_centered_4_test.csv', header=None, index_col=0, skiprows=6)
# ax1.plot(np.max(np.abs(psi), axis=1), label='dt=4.00')


unstable_psi = pd.read_csv('../data/psi_unstable_long.csv', header=None, index_col=0, skiprows=6)
ax.plot(np.max(np.abs(unstable_psi), axis=1), label='dt=1.0', alpha=0.5)


ax.legend()
ax.grid()
plt.yscale('log')
plt.xscale('log')
# plt.ylim(0.5, 2)
plt.plot()
```

```python

```

```python

fig, axes = plt.subplots(2, sharex=True, sharey=True, figsize=[8,8])
ax1,ax2 = axes.flat
# psi = pd.read_csv('../data/psi_long_centered_stable.csv', header=None, index_col=0, skiprows=6)
# ax1.plot(np.max(np.abs(psi), axis=1))


psi = pd.read_csv('../data/psi_stable_long.csv', header=None, index_col=0, skiprows=6)
ax1.plot(np.max(np.abs(psi), axis=1), label='dt=0.9')

# psi = pd.read_csv('../data/psi_long_centered_4_test.csv', header=None, index_col=0, skiprows=6)
# ax1.plot(np.max(np.abs(psi), axis=1), label='dt=4.00')


psi = pd.read_csv('../data/psi_unstable_long.csv', header=None, index_col=0, skiprows=6)
ax2.plot(np.max(np.abs(psi), axis=1), label='dt=1.0')


# psi = pd.read_csv('../data/psi_long_centered_test_init63.csv', header=None, index_col=0, skiprows=6)
# ax3.plot(np.max(np.abs(psi), axis=1), label='dt=6.3')

ax1.legend()
ax2.legend(loc='center left')
# ax3.legend()
ax1.grid()
ax2.grid()
# ax3.grid()

# plt.xscale('log')
# plt.yscale('log')
plt.xscale('log')
plt.ylim(0.5, 2)
```

```python
dx = 1/40.
k = (2*2*np.pi)
print(dx * k**2)

dt = 6.29
dx = 1/40
print(1/k**2 * dt/dx)
```

```python
theta0 = 60*np.pi/180
Re = 6300*1e3
L = 19000*1e3
sigma = 2*np.pi/(86400)
beta = 2*sigma*np.cos(theta0)/Re
n = 1
k = 2*n*np.pi/L
print(beta/k**2)
```

```python
n = 2
dt = 0.1
a = -1
b = 0.25
c = 1/(2*n*np.pi)**2
print('dx > {:.5f}'.format(dt/(b*c**a)))

k = 2*n*np.pi



dt = 0.1
print(dt/0.024)
print(4*dt/(1+k**2))
print('dt/dx < {}'.format(1/4 * np.sqrt(k**2 + 1)))
print('dt < {}'.format(1/40 * 1/4 * np.sqrt(1+k**4)))

print(dt/(np.sqrt(k**4 - 1)))
```

```python
n = 1
dt = 1
c = 1/(2*n*np.pi)**2
print(4*c*dt)

# # dx = 0.025
# print(c*dt/dx)
# # print(c*dt/alpha)
```

```python
filename = '../data/psi_wavespeed.csv'
psi = pd.read_csv(filename, header=None, index_col=0, skiprows=6)
np.max(np.max(psi))
```

```python
dx = 1/40
c = 1/(2*2*np.pi)**2
print(c/dx)
print(1/(c/dx))
```

## Hovmuller

```python
def hovmuller(filename):
    psi = pd.read_csv(filename, header=None, index_col=0, skiprows=6)
    x = psi.columns.values
    t = psi.index.values
    X, T = np.meshgrid(x, t)
    plt.contourf(X, T, psi.values, levels=np.linspace(-2.5,2.5,13))
    plt.xlabel('x$_i$')
    plt.colorbar()
```

```python
compare('../data/psi_bounded_gaussian_0.05.csv', times=[0,50,100])
```

```python
compare('../data/psi_bounded_gaussian_0.25.csv', times=[0,50, 100])
```

```python
hovmuller('../data/psi_bounded_gaussian_0.25.csv')
```

```python
hovmuller('../data/psi_bounded_gaussian_0.05.csv')
```

```python
compare('../data/psi_periodic_gaussian_0.05.csv', times=[10, 50, 100])
```

## Periodic


### Sine

```python
hovmuller('../data/psi_periodic_centered_sine.csv')
```

```python
hovmuller('../data/psi_periodic_forward_sine.csv')
```

### Gaussian

```python
# ! ls -l ../data/ | grep gauss
hovmuller('../data/psi_periodic_gauss_0.12.csv')
```

```python
hovmuller('../data/psi_periodic_centered_gauss_0.08.csv')
```

```python
hovmuller('../data/psi_periodic_centered_gauss_0.09.csv')
```

```python
hovmuller('../data/psi_periodic_centered_gauss_0.11.csv')
```

```python
hovmuller('../data/psi_periodic_centered_gauss_0.12.csv')
```

## Bounded

```python
hovmuller('../data/psi_bounded_centered_sine.csv')
plt.plot(np.sin(2*np.pi*x))
```

```python
x = np.linspace(0, 1, 40)
plt.plot(x, np.sin(2*np.pi*x))
```

```python
hovmuller('../data/psi_bounded_centered_gauss.csv')
```

## Stability
