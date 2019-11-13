import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import summary_table





def critical_temperature(datafile, window):

    df = pd.read_csv('../data/longrun4.csv')
    n = window
    Tlargest = []
    Trolling = []
    Tmean = []
    Ls = []
    for L in [40,60,80,100]:
        sel = df.loc[df['spins']==L**2]
        Tcnlarg = sel.nlargest(n,'cv')['T'].mean()
        Tcrolling = sel.rolling(n).mean().nlargest(1,'cv')['T'].values[0]
        Trolling.append(Tcrolling)
        mean = (Tcnlarg+Tcrolling)/2
        Tmean.append(mean)
        Tlargest.append(Tcnlarg)
        plt.scatter(1/L,Tcnlarg,marker='s',color='red')
        plt.scatter(1/L,Tcrolling,color='blue')
        plt.scatter(1/L, mean,color='green')
        Ls.append(L)
    TL = sel.rolling(n).mean().nlargest(1,'cv')['T'].values[0]
    L = np.linspace(101,39,1000)
    print(TL - a/100)
    # print(Tc)


    alpha = 0.05
    values = np.array([Tlargest,Trolling,Tmean,Ls])
    df = pd.DataFrame(values.transpose(),columns=['Tlargest','Trolling','Tmean','L'])
    df['L'] = -1/df['L']
    for col,mark in zip(['Tlargest','Trolling','Tmean'],['r--','b--','g--']):
        formula = '{} ~ L'.format(col)
        fit = smf.ols(formula=formula, data=df).fit()
        a = fit.params[-1]
        T = fit.params[0]

    #     plt.plot(1/L,T - a/L)
        print('Method: {}'.format(col))
        print(T)
        print(2/(np.log(1 + np.sqrt(2))))

    #     print(fit.summary())
    #     print('a: {}'.format(a))
        print('Tc: {}'.format(T-2/(np.log(1 + np.sqrt(2)))))
        st, data, ss2 = summary_table(fit, alpha=alpha)

        fittedvalues = data[:, 2]
        predict_mean_se  = data[:, 3]
        predict_mean_ci_low, predict_mean_ci_upp = data[:, 4:6].T
        predict_ci_low, predict_ci_upp = data[:, 6:8].T
        Linv = [ 1/L for L in Ls ]
        plt.plot(Linv, fittedvalues, '-', lw=2)
        plt.plot(Linv, predict_ci_low, mark, lw=2)
        plt.plot(Linv, predict_ci_upp, mark, lw=2)

if __name__ == '__main__':
