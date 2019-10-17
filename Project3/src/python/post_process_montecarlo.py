import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np

parser_description = 'Analyze results of monte-carlo experiment.'
filepath_help = 'Filepath of file to analyze (.csv)'

DATADIR = '../../data/'
FIGDIR = '../../figures/'



# Initialize parser
parser = argparse.ArgumentParser(description=parser_description)
parser.add_argument('--input', default=DATADIR+'montecarlo.csv',help=filepath_help)

import scipy.stats as st

def print_CI(alpha, mean, std):
    z = st.norm.ppf(1-alpha/2.)
    L = mean - z*std
    U = mean + z*std
    for l,u in zip(L,U):
        print('C.I, {}: [{:.3f},{:.3f}]'.format(alpha,l,u))

if __name__ == '__main__':
    args = parser.parse_args()
    filename = args.input
    print(filename)

    df = pd.read_csv(filename)
    print(df)

    # std_time_importance = (df['std_importance']/df['time_importance'])
    # std_time_brute = df['std_brute']/df['time_brute']
    #
    #
    # plt.loglog(df['N'], std_time_brute)
    # plt.loglog(df['N'], std_time_importance)
    # plt.show()

    # Skip results for N = 10
    # df = df.loc[1:,:]
    # print_CI(0.01, df['result_brute'], df['std_brute'])
    # print('\n')
    # print_CI(0.01, df['result_importance'], df['std_importance'])

    # analytical = (5*np.pi**2/16**2)
    # alpha = 0.05
    # err = df['std_importance']*st.norm.ppf(1-alpha/2.)
    # print(err)
    # ax = df.plot.bar('N','result_importance',yerr=err.values)
    # plt.axhline(analytical,color='r',linestyle='--',label='Analytical')
    # plt.legend()
    # plt.show()

    # loglog plot of standard deviation
    # ax1 = df.plot.scatter('N','std_importance', loglog=True, color='r', label='std_importance')
    # df.plot.scatter('N','std_brute',loglog=True, ax=ax1, color='b', label='std_brute')
    # plt.show()
    #
    #
    # # Error plot
    # ax2 = df.plot.scatter('N','error_importance', logx=True, color='r', label='error_importance')
    # df.plot.scatter('N','error_brute', ax=ax2,logx=True, color='b', label='error_brute')
    # plt.show()
    #
    # # Plot error with bars - not very useful
    # # ax1 = df.plot.bar('N', 'error_importance',yerr='std_importance',alpha=0.5, align='center')
    # # df.plot.bar('N','error_brute',yerr='std_brute', align='center',alpha=0.5, ax=ax1, color='r')
    # # plt.show()
    #
    #
    # # Plot error divided by standard deviation
    # df['err_div_std_brute'] = df['error_brute'] / df['std_brute']
    # df['err_div_std_importance'] = df['error_importance'] / df['std_importance']
    # ax = df.plot.scatter('N','err_div_std_brute',logx=True,color='b')
    # df.plot.scatter('N','err_div_std_importance',logx=True, ax=ax, color='r')
    # plt.show()
