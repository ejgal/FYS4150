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
    # Tc = crit_temp_poly('../data/longrun4.csv')
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
    plt.plot(Linv,T + Linv * a,label='Fit')
    df.plot('Linv','Tc',marker='o', ax=ax, linestyle=' ',label='T$_C$(L)')
    plt.xlim(0,0.03)
    plt.ylim(2.25,2.30)
    plt.xlabel('1/L')
    plt.ylabel('T')
    plt.legend()
    plt.savefig(FIGDIR + 'Tc_fit.eps')
    plt.savefig(FIGDIR + 'Tc_fit.pdf')
    print(r'$Tc={:.5f} \pm {:.5f}$'.format(T, width))
    print('Tc in [{:.5f},{:.5f}]'.format(T-width, T+width))
    print('Analytical: {:.5f}'.format(analytic))
    rel_err = np.abs(T - analytic)/analytic
    T_low = T - width
    T_high = T + width
    upper_rel = np.abs(T_low - analytic)/analytic
    lower_rel = np.abs(T_high - analytic)/analytic
    abs_err = np.abs(T - analytic)
    print('relative error: {:.5e}'.format(rel_err))
    print('Absolute error: {:.5e}'.format(np.abs(abs_err)))
    print('CI abs err: {:.5e}'.format(np.abs(analytic - (T - width))))
    print('CI abs err: {:.5e}'.format(np.abs(analytic - (T + width))))

    with open(DATADIR + 'critical.csv','w') as file:
        file.write('T$_C$,{:.4f}\n'.format(T))
        file.write('Absolute error,{:.2e}\n'.format(abs_err))
        file.write('Relative error,{:.2e}\n'.format(rel_err))
