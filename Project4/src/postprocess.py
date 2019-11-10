import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from settings import *
from parser import post_parser

def plot_equilibrium(datafile):
    df = pd.read_csv(datafile)

    # Calculate ratio of accepted configurations
    df['ratio'] = df['accepted']/(df['spins']*df['cycles'])

    # Plot equilibrium tests
    df = pd.read_csv(equi)
    df['E'] = np.abs(df['E'])
    df['M'] = np.abs(df['M'])
    for col in ['E','M']:
        fig, ax=plt.subplots(3, sharex=True)
        for T in [1.0,2.4]:
            lb = 'T={}'.format(T)
            for axis, ordered in zip(ax, [1,-1,0]):
                df.loc[(df['T']==T) & (df['ordered']==ordered)].plot('cycles',col, ax=axis,linestyle='--', label=lb,logx=True)
                axis.set_ylabel('{} - ordered={}'.format(col,ordered))
        plt.savefig(FIGDIR + 'equilibrium_{}.png'.format(col))
        plt.clf()

def plot_distribution(distfile, datafile):
    dist = pd.read_csv(distfile,index_col=0)
    data = pd.read_csv(datafile)
    data['T'] = data['T'].round(2)
    data.index = data['T']
    columns = dist.columns[0::3]
    num_bins = int(1+3.3*np.log(len(dist)))

    for T in columns:
        label = 'T={} ,cv={:.2f}'.format(T,data.loc[float(T),'cv'])
        dist[T].hist(density=True, bins=num_bins,label=label, alpha=0.8)
    plt.legend()
    plt.ylabel('Probability density')
    plt.xlabel('Energy')
    plt.savefig(FIGDIR + 'distribution.png')
    plt.clf()

def plot_phase(datafile):
    df = pd.read_csv(datafile)
    for col,ylabel in zip(['E','Mabs','cv','suscept'],['Energy','Magnetization','Heat capacity','Susceptibility']):
        fig, ax = plt.subplots(1)
        for L in [40,60,80,100]:
            spins = L**2
            label = 'L={}'.format(L)
            df.loc[df['spins']==spins].plot('T',col, ax=ax,linestyle=' ',markersize=1,marker='o',label=label)
        ax.legend()
        ax.set_ylabel(ylabel)
        plt.savefig(FIGDIR + 'phase_{}.png'.format(col))
        plt.clf()

if __name__ == '__main__':
    args = post_parser().parse_args()
    equi = args.equi
    phase = args.phase
    distfile = args.distfile
    datafile = args.distdata

    plot_distribution(distfile, datafile)
    plot_equilibrium(equi)
    plot_phase(DATADIR + phase)
