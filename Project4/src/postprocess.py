import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from settings import *
from parser import post_parser

def plot_equilibrium(datafile):
    df = pd.read_csv(datafile)
    df['E'] = np.abs(df['E'])
    df['M'] = np.abs(df['M'])
    for col in ['E','M']:
        fig,ax = plt.subplots(2)
        ax1 = ax[0]
        ax2 = ax[1]
        df.loc[df['T']==1.0].plot('cycles',col, ax=ax1,logx=True,label='|{}|, T=1.0'.format(col))
        df.loc[df['T']==2.4].plot('cycles',col, ax=ax2, logx=True,label='|{}|, T=2.4'.format(col))
        plt.savefig(FIGDIR + 'equilibrium_{}'.format(col))
        plt.clf()

def plot_phase(datafile):
    df = pd.read_csv(datafile)
    for col in ['E','Mabs','cv','suscept']:
        fig, ax = plt.subplots(1)
        for L in [40,60,80,100]:
            spins = L**2
            label = 'L={}'.format(L)
            df.loc[df['spins']==spins].plot('T',col, ax=ax,linestyle=' ',markersize=1,marker='o',label=label)
        ax.legend()
        plt.savefig(FIGDIR + 'phase_{}.png'.format(col))
        plt.clf()

if __name__ == '__main__':
    args = post_parser().parse_args()
    equi = args.equi
    phase = args.phase

    plot_phase(DATADIR + phase)
    plot_equilibrium(DATADIR + equi)
