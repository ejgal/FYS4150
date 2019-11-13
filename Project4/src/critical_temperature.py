import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import summary_table





def critical_temperature(datafile, window, alpha):

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
        # plt.scatter(1/L,Tcnlarg,marker='s',color='red')
        # plt.scatter(1/L,Tcrolling,color='blue')
        # plt.scatter(1/L, mean,color='green')
        Ls.append(L)
    TL = sel.rolling(n).mean().nlargest(1,'cv')['T'].values[0]
    L = np.linspace(101,39,1000)
    # print(TL - a/100)
    # print(Tc)

    a = 0
    values = np.array([Tlargest,Trolling,Tmean,Ls])
    df = pd.DataFrame(values.transpose(),columns=['Tlargest','Trolling','Tmean','L'])
    df['L'] = -1/df['L']
    # print('window: {}'.format(n))
    Errlist = []
    CIlist = []
    for col,mark in zip(['Tlargest','Trolling'],['r--','b--']):
        formula = '{} ~ L'.format(col)
        fit = smf.ols(formula=formula, data=df).fit()
        a = fit.params[-1]
        T = fit.params[0]

    #     plt.plot(1/L,T - a/L)

        # print('Method: {}'.format(col))
        # print(T)
        # print(2/(np.log(1 + np.sqrt(2))))

    #     print(fit.summary())
    #     print('a: {}'.format(a))
        # Absolute error
        # Terr = T-2/(np.log(1 + np.sqrt(2)))
        # Relative error
        Terr = T/(2/(np.log(1 + np.sqrt(2))))
        Errlist.append(T)
        CIlist.append(fit.conf_int(alpha=alpha))
        # print('Tc error: {:.2e}'.format(Terr))
        # st, data, ss2 = summary_table(fit, alpha=alpha)
        #
        # fittedvalues = data[:, 2]
        # predict_mean_se  = data[:, 3]
        # predict_mean_ci_low, predict_mean_ci_upp = data[:, 4:6].T
        # predict_ci_low, predict_ci_upp = data[:, 6:8].T
        # Linv = [ 1/L for L in Ls ]
        # plt.plot(Linv, fittedvalues, '-', lw=2)
        # plt.plot(Linv, predict_ci_low, mark, lw=2)
        # plt.plot(Linv, predict_ci_upp, mark, lw=2)
    return Errlist, CIlist

if __name__ == '__main__':

    data = '../data/longrun4.csv'
    TLarge = []
    Troll = []
    Tlarge_ci = []
    Troll_ci = []
    startwin = 1
    maxwin = 10
    analytic = 2/(np.log(1 + np.sqrt(2)))

    for i in range(startwin,maxwin):
        [Tl, Tr], CI = critical_temperature(data, i, alpha=0.01)
        TLarge.append(Tl)
        Troll.append(Tr)
        Tlarge_ci.append(CI[0].loc['Intercept',1]-Tl)
        Troll_ci.append(CI[1].loc['Intercept',1]-Tr)
    #
    # print(len(Tlarge_ci))
    # print(np.shape(Tlarge_ci))
    # print(np.shape(TLarge))
    window = np.linspace(startwin,maxwin,maxwin-startwin)
    # print(Tlarge_ci)
    fig, ax = plt.subplots(1)
    ax1= ax
    ax1.errorbar(window, np.abs(TLarge), label='nlargest', linestyle=' ',marker='x',yerr=(Tlarge_ci),capsize=10)
    ax1.errorbar(window, np.abs(Troll), label='rolling', linestyle=' ', marker='x',yerr=(Troll_ci),capsize=10)
    ax1.grid()
    # ax2.grid()
    ax1.legend()
    # ax2.legend()
    # ax1.set_xscale('log')
    ax1.axhline(analytic,linestyle='--')
    # ax2.axhline(analytic,linestyle='--')

    # ax2.set_xscale('log')
    plt.show()
    fig, ax = plt.subplots(1)
    ax1= ax
    ax1.plot(window, np.abs(TLarge - analytic))
    ax1.plot(window, np.abs(Troll - analytic))
    ax1.set_yscale('log')
    plt.show()

    fig, ax = plt.subplots(2)
    ax1, ax2 = ax
    upper = np.array(TLarge) + np.array(Tlarge_ci)
    lower = np.array(TLarge) - np.array(Tlarge_ci)
    print(np.shape(upper))
    ax1.plot(window, ((TLarge - analytic)/analytic),marker='x')
    ax2.plot(window, ((Troll - analytic)/analytic), marker='x')
    ax1.plot(window, ((upper - analytic)/analytic), linestyle='--',label='upper relative error',color='green')
    ax1.plot(window, ((lower - analytic)/analytic), linestyle='--',label='upper relative error',color='green')

    upper = np.array(Troll) + np.array(Troll_ci)
    lower = np.array(Troll) - np.array(Troll_ci)
    ax2.plot(window, ((upper - analytic)/analytic), linestyle='--',label='upper relative error',color='green')
    ax2.plot(window, ((lower - analytic)/analytic), linestyle='--',label='upper relative error',color='green')
    print(TLarge[2])
    print(np.sum(TLarge[2:5])/3.)

    # ax1.set_yscale('log')
    # ax2.set_yscale('log')
    ax1.grid()
    ax2.grid()
    plt.show()
