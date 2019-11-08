import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from settings import *
from parser import post_parser

# def plot_equilibrium(datafile):
#     df = pd.read_csv(datafile)
#     df['E'] = np.abs(df['E'])
#     df['M'] = np.abs(df['M'])
#     for col in ['E','M']:
#         fig,ax = plt.subplots(2)
#         ax1 = ax[0]
#         ax2 = ax[1]
#         label1 = r'$<\vert$ {} $\vert >$\, T=1.0'.format(col)
#         label2 = r'$<\vert$ {} $\vert >$\, T=2.4'.format(col)
#         # df.loc[(df['T']==1.0) & (df['ordered']==1)].plot('cycles',col, ax=ax1, label=label1,logx=True)
#         df.loc[(df['T']==2.4) & (df['ordered']==1)].plot('cycles',col, ax=ax1, label=label2,logx=True)
#
#         # df.loc[(df['T']==1.0) & (df['ordered']==1)].plot('cycles',col, ax=ax1,logx=True,label=label1)
#         # df.loc[(df['T']==2.4]) & (df['ordered']==1)].plot('cycles',col, ax=ax1, logx=True,label='|{}|, T=2.4'.format(col))
#         plt.savefig(FIGDIR + 'equilibrium_{}'.format(col))
#         plt.clf()

def plot_phase(datafile):
    df = pd.read_csv(datafile)
    for col in ['E','Mabs','cv','suscept']:
        fig, ax = plt.subplots(1)
        for L in [40,60,80,100]:
            spins = L**2
            label = 'L={}'.format(L)
            df.loc[df['spins']==spins].plot('T',col, ax=ax,linestyle=' ',markersize=1,marker='o',label=label)
        ax.legend()
        # Plot critical value
        # plt.axvline(2.269)

        plt.savefig(FIGDIR + 'phase_{}.png'.format(col))
        plt.clf()

if __name__ == '__main__':
    args = post_parser().parse_args()
    equi = args.equi
    phase = args.phase


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


    # df.loc[(df['T']==1.0) & (df['ordered']==1)].plot('cycles','M', ax=ax1, label=lb1,logx=True)
    # df.loc[(df['T']==2.4) & (df['ordered']==1)].plot('cycles','M', ax=ax1, label=lb2,logx=True)
    # df.loc[(df['T']==1.0) & (df['ordered']==0)].plot('cycles','M', ax=ax2, label=lb1,logx=True)
    # df.loc[(df['T']==2.4) & (df['ordered']==0)].plot('cycles','M', ax=ax2, label=lb2,logx=True)
    # df.loc[(df['T']==1.0) & (df['ordered']==-1)].plot('cycles','M', ax=ax3, label=lb1,logx=True)
    # df.loc[(df['T']==2.4) & (df['ordered']==-1)].plot('cycles','M', ax=ax3, label=lb2,logx=True)

    # plot_equilibrium(DATADIR + equi)
    plot_phase(DATADIR + phase)
