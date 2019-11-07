import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from plot import *

# Check for equilibrium

def plot_equilibrium(filename):
    filename = '../data/equilibrium.csv'
    df = pd.read_csv(filename)
    df['E'] = np.abs(df['E'])
    df['M'] = np.abs(df['M'])
    for col,var in zip(['E','M'],['cv','suscept']):
        fig,ax = plt.subplots(2)
        ax1 = ax[0]
        ax2 = ax[1]
        df.loc[df['T']==1.0].plot('cycles',col, ax=ax1,logx=True,label='{}, T=1.0'.format(col))
        df.loc[df['T']==2.4].plot('cycles',col, ax=ax2, logx=True,label='{}, T=1.0'.format(col))
        # df.loc[df['T']==1.0].plot('cycles',var, ax=ax1,logx=True,label='T=1.0')
        # df.loc[df['T']==2.4].plot('cycles',var, ax=ax2, logx=True,label='T=2.4')

    plt.show()


if __name__ == '__main__':
    filename = '../data/test_parallel.csv'
    df = pd.read_csv(filename)
    print(df)
    df.plot('T','Mabs')
    plt.show()
    df.plot('T','suscept')
    plt.show()
