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
    T = np.linspace(Tmin,Tmax,1000)
    for L in [40,60,80,100]:
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
    Tc = crit_temp_poly('../data/longrun6.csv',n=6)
    L = [40,60,80,100]
    values = np.array([Tc,L]).transpose()
    df = pd.DataFrame(values,columns=['Tc','L'])

    # Inverse L -> Critical temperature at intercept
    df['Linv'] = 1/df['L']

    # Fit line
    fit = smf.ols(formula='Tc ~ Linv', data=df).fit()
    a = fit.params[-1]
    T = fit.params[0]
    CI = fit.conf_int(alpha=0.01)
    upper = CI.loc['Intercept',1]
    width = upper-T
    fig, ax = plt.subplots(1,figsize=get_size(columns=1))
    Linv = np.linspace(0,10,100)

    # Plot fit
    plt.plot(Linv,T + Linv * a,label='Fit')
    df.plot('Linv','Tc',marker='o', ax=ax, linestyle=' ',label='T$_C$(L)')
    plt.xlim(0,0.03)
    plt.ylim(2.25,2.30)
    plt.xlabel('1/L')
    plt.ylabel('T')
    plt.legend()
    plt.savefig(FIGDIR + 'Tc_fit.png')
    plt.savefig(FIGDIR + 'Tc_fit.pdf')

    # Calculate errors
    rel_err = np.abs(T - analytic)/analytic
    abs_err = np.abs(T - analytic)
    T_low = T - width
    T_high = T + width
    upper_abs = np.abs(T_low - analytic)
    lower_abs = np.abs(T_high - analytic)

    # Write results to file
    with open(DATADIR + 'critical.csv','w') as file:
        file.write(',Value,CI low, CI high\n')
        file.write('T$_C$,{:.4f},{:.4f}, {:.4f}\n'.format(T, T_low,T_high))
        file.write('Absolute error,{:.2e},,'.format(abs_err))
        file.write('Relative error,{:.2e},,\n'.format(rel_err))
