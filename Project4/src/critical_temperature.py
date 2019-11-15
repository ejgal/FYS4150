import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from settings import *

def crit_temp_poly(datafile,n=4):
    """
    Extract critical temperature by fitting
    a polynomial of degree n.
    """
    df = pd.read_csv(datafile)
    Tc = []
    Tmin = df['T'].min()
    Tmax = df['T'].max()
    print(Tmin)
    print(Tmax)
    T = np.linspace(Tmin,Tmax,1000)
    for L in [40,60,80,100]:
        print('L: {}'.format(L))
        # Select runs with given spin
        sel = df.loc[df['spins']==L**2]
        # Fit polynomial and find temperature of highest cv
        fit = np.polyfit(sel['T'],sel['cv'],n)
        poly = np.poly1d(fit)
        T_index = np.argmax(poly(T))
        Tc.append(T[T_index])
    return Tc

if __name__ == '__main__':

    # Estimates of critical temperature
    Tc = crit_temp_poly('../data/longrun4.csv')
    L = [40,60,80,100]
    values = np.array([Tc,L]).transpose()
    df = pd.DataFrame(values,columns=['Tc','L'])
    # Inverse L -> Critical temperature at intercept
    df['L'] = -1/df['L']

    # Fit line
    fit = smf.ols(formula='Tc ~ L', data=df).fit()
    a = fit.params[-1]
    T = fit.params[0]
    CI = fit.conf_int(alpha=0.01)
    upper = CI.loc['Intercept',1]
    width = upper-T
    df['predict'] = fit.predict()
    fig, ax = plt.subplots(1)

    # df.plot('L','Tc',marker='s', ax=ax)
    # df.plot('L','predict',ax=ax)
    print(r'$Tc={:.5f} \pm {:.5f}$'.format(T, width))
    print('Tc in [{:.5f},{:.5f}]'.format(T-width, T+width))
    print('Analytical: {:.5f}'.format(analytic))
    rel_err = np.abs(analytic-T)/analytic
    upper_rel = np.abs(T-width -analytic)/analytic
    lower_rel = np.abs(T + width - analytic)/analytic
    print('relative error: {:.5f}'.format(rel_err))
    print('relative error in [{:.5f},{:.5f}]'.format(lower_rel,upper_rel))
