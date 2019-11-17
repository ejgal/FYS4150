import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

from settings import *
from parser import post_parser
import analytic as a

def plot_relative_error(datafile,T = 1.0,L=2,window=1,ordered=0):

    df = pd.read_csv(datafile)

    fig, ax = plt.subplots(2,2,sharex=True,sharey=True,figsize=get_size(ratio=1))
    axes = [ax[0,0],ax[0,1],ax[1,0],ax[1,1]]
    i = 0
    for T in [1.0,2.4]:
        for ordered in [0,1]:
            axis = axes[i]

            # Get analytical values
            cv = a.cv(T)/L**2
            E = a.expected_energy(T)/L**2
            Mabs = a.expected_magnetization(T)/L**2
            suscept = a.susceptibility(T)/L**2


            sel = df.loc[(df['T'] == T) & (df['ordered']==ordered)].copy()
            # Calculate relative errors
            sel['relcv'] = np.abs(sel['cv'] - cv)/np.abs(cv)
            sel['relE'] = np.abs(sel['E'] - E)/np.abs(E)
            sel['relMabs'] = np.abs(sel['Mabs'] - Mabs)/np.abs(Mabs)
            sel['relsuscept'] = np.abs(sel['suscept'] - suscept)/np.abs(suscept)

            axis.yaxis.set_major_locator(MultipleLocator(0.1))

            axis.tick_params(left=True,right=True,which='both')
            # ax.tick_params(labelleft =True, labelright=True)
            cols = ['relE','relMabs','relcv','relsuscept']
            labels = ['Energy','Magnetization','Heat capacity','Susceptibility']
            # colors = []

            for col,label in zip(cols,labels):
                mean = sel.rolling(window).mean()
                mean.plot('cycles',col,linestyle='--',logx=True,logy=True, ax=axis,label=label)

            axis.set_title('Ordered={} T={}'.format(ordered,T))
            axis.set_ylabel('Relative error')
            axis.set_xlabel('Monte Carlo cycles')
            axis.autoscale_view('tight')
            axis.grid()

            if i > 0:
                axis.get_legend().remove()
            i += 1

    plt.savefig(FIGDIR + 'relative_error.png')
    plt.savefig(FIGDIR + 'relative_error.pdf')


def plot_equilibrium(datafile):
    df = pd.read_csv(datafile)

    # Plot equilibrium tests
    df = pd.read_csv(equi)
    df['E'] = np.abs(df['E'])
    df['Mabs'] = np.abs(df['Mabs'])
    ticks = np.arange(-5,5,0.1)
    for col,ylabel in zip(['E','Mabs'],['$|$Energy$|$', '$|$Magnetization$|$']):
        fig, ax=plt.subplots(2, sharex=True, sharey=True)
        for T in [1.0,2.4]:
            lb = 'T={}'.format(T)
            # Plot for spins up and random
            for axis, ordered in zip(ax, [1,0]):
                sel = df.loc[(df['T']==T) & (df['ordered']==ordered)]
                sel = sel.loc[df['cycles'].between(0,50000)]
                sel.plot('cycles',col, ax=axis,linestyle='-', label=lb)

                # axis.set_ylabel(r'$|<${}$>|$'.format(col))
                axis.set_ylabel(ylabel)
                axis.yaxis.set_major_locator(MultipleLocator(0.1))
                axis.grid(linestyle='--',axis='y')
                axis.set_title('Ordered={}'.format(ordered))
        plt.savefig(FIGDIR + 'equilibrium_{}.png'.format(col))
        plt.savefig(FIGDIR + 'equilibrium_{}.pdf'.format(col))
        plt.clf()

def plot_distribution(distfile, datafile):
    dist = pd.read_csv(distfile,index_col=0)
    data = pd.read_csv(datafile)
    data['T'] = data['T'].round(2)
    data.index = data['T']
    columns = dist.columns
    num_bins = int(1+3.3*np.log(len(dist)))
    L = 20
    i = 0

    for T in columns:
        dist[T] = dist[T]/L**2
        fig,ax = plt.subplots(1,figsize=get_size(columns=2,ratio=0.3))
        label = 'T={} $\sigma_E^2$={:.2f}'.format(T,data.loc[float(T),'cv']*float(T)**2)
        dist[T].hist(density=True,bins=64,label=label, alpha=0.8,ax=ax)
        plt.legend()
        plt.grid(False)
        # plt.yscale('log')
        plt.ylabel('Probability density')
        plt.xlabel('Energy')
        plt.savefig(FIGDIR + 'distribution_{}.png'.format(i))
        plt.savefig(FIGDIR + 'distribution_{}.pdf'.format(i))
        i +=1
    plt.clf()

def plot_phase(datafile):
    df = pd.read_csv(datafile)

    fig, ax = plt.subplots(2,2,sharex=True,sharey=False,figsize=get_size(ratio=0.8))
    axes = [ax[0,0],ax[0,1],ax[1,0],ax[1,1]]
    i = 0
    for col,ylabel in zip(['E','Mabs','cv','suscept'],['Energy','Magnetization','Heat capacity','Susceptibility']):
        axis = axes[i]
        for L in [40,60,80,100]:
            spins = L**2
            label = 'L={}'.format(L)
            sel = df.loc[df['spins']==spins]
            sel.plot('T',col,linestyle=' ',markersize=1.5,marker='o',label=label,ax=axis)
        axis.legend()
        axis.set_ylabel(ylabel)
        axis.grid()
        if i > 0:
            axis.get_legend().remove()

        i += 1
    plt.savefig(FIGDIR + 'phase.png'.format(col))
    plt.savefig(FIGDIR + 'phase.pdf'.format(col))
    plt.clf()

def plot_accepted(datafile):
    df = pd.read_csv(datafile)
    df['ratio'] = df['accepted']/(df['spins']*df['cycles'])
    fig, ax = plt.subplots(1,figsize=get_size(ratio=0.4))
    # df = df.loc[df['cycles'].between(0,100000)]
    df.loc[(df['T']==1.0) & (df['ordered']==0)].plot('cycles','ratio',ax=ax,label='T=1.0')
    df.loc[(df['T']==2.4) & (df['ordered']==0)].plot('cycles','ratio',ax=ax,label='T=2.4')
    plt.xscale('log')
    # plt.yscale('log')
    plt.grid()
    plt.legend()
    plt.yscale('log')
    plt.ylabel('Accepted / (spins $\cdot$ cycles)')
    plt.savefig(FIGDIR + 'accepted.png')
    plt.savefig(FIGDIR + 'accepted.pdf')
    plt.clf()

def plot_fit(datafile):

    df = pd.read_csv(datafile)
    fig,ax = plt.subplots(figsize=get_size(columns=1))
    colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728']

    for L,color in zip([40,60,80,100],colors):
        spins = L**2
        sel = df.loc[df['spins']==spins]
        fit = np.polyfit(sel['T'],sel['cv'],6)
        poly = np.poly1d(fit)
        T = np.linspace(2.2,2.35,100)
        ax.plot(T, poly(T),color=color,linestyle='-',linewidth=0.5)
        ax.plot(sel['T'],sel['cv'],marker='o',markersize=0.3,color=color,linestyle=' ')

    plt.xlabel('T')
    plt.ylabel('Heat capacity')
    plt.savefig(FIGDIR + 'fit.png')
    plt.savefig(FIGDIR + 'fit.pdf')

if __name__ == '__main__':
    args = post_parser().parse_args()
    equi = args.equi
    phase = args.phase
    distfile = args.distfile
    datafile = args.distdata
    errorfile = args.error

    plot_equilibrium(equi)

    plot_distribution(distfile, datafile)
    plot_fit('../data/longrun6.csv')
    plot_accepted(equi)
    plot_phase(phase)
    win = 5
    plot_relative_error(errorfile,T=1.0,window=win)
    plot_relative_error(errorfile,T=1.0,window=win,ordered=1)
    plot_relative_error(errorfile,T=2.4,window=win)
    plot_relative_error(errorfile,T=2.4,window=win,ordered=1)
