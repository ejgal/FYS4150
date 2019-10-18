import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np
import scipy.stats as st
import mpl_settings

parser_description = 'Analyze results of gaussian quadrature experiment.'
filepath_help = 'Filepath of file to analyze (.csv)'

DATADIR = '../../data/'
FIGDIR = '../../figures/'

# Initialize parser
parser = argparse.ArgumentParser(description=parser_description)
parser.add_argument('--input', default=DATADIR+'gaussQuad.csv',help=filepath_help)


if __name__ == '__main__':
    args = parser.parse_args()
    filename = args.input
    print(filename)

    # Load data
    df = pd.read_csv(filename)
    print(df)

    # Plot of error
    # plt.xscale('log')
    plt.yscale('log')
    df['error_leg'] = np.abs(df['error_leg'])
    df['error_lag'] = np.abs(df['error_lag'])
    plt.plot(df['N'],df['error_leg'], label='error legendre', marker='s')
    plt.plot(df['N'],df['error_lag'], label='error laguerre', marker='o')
    plt.plot(df['N'], df['error_leg']/df['error_lag'], label='error legendre / error laguerre', marker='x')
    plt.xlabel('N')
    plt.ylabel('Error')
    plt.legend()
    plt.grid()
    plt.savefig(FIGDIR+'gauss_error.png')
    plt.clf()

    # Timings of gauss quadrature

    plt.yscale('log')
    plt.plot(df['N'],df['time_leg'], label='time legendre', marker='s')
    plt.plot(df['N'],df['time_lag'], label='time laguerre', marker='o')
    plt.plot(df['N'], df['time_leg']/df['time_lag'], label='time legendre / time laguerre', marker='x')
    plt.xlabel('N')
    plt.ylabel('Time [s]')
    plt.legend()
    plt.grid()
    plt.savefig(FIGDIR+'gauss_time.png')
    plt.clf()


    # Compare error/time ratios of gauss and monte-carlo
    mc = pd.read_csv(DATADIR+'montecarlo.csv')

    plt.yscale('log')
    plt.xscale('log')
    mc['error_importance'] = np.abs(mc['error_importance'])
    mc['error_brute_pl'] = np.abs(mc['error_brute_pl'])
    # plt.plot(mc['time_importance_pl'],mc['error_importance']/mc['time_importance_pl'], label='Importance',marker='x')
    # plt.plot(mc['time_brute_pl'],mc['error_brute_pl']/mc['time_brute_pl'], label='Brute', marker='x')
    # plt.plot(df['time_leg'], df['error_leg']/df['time_leg'], label='Legendre', marker='s', alpha=0.5)
    # plt.plot(df['time_lag'], df['error_lag']/df['time_lag'], label='Laguerre', marker='s', alpha=0.5)

    plt.plot(mc['time_importance_pl'],mc['error_importance'], label='Importance',marker='x')
    plt.plot(mc['time_brute_pl'],mc['error_brute_pl'], label='Brute', marker='x')
    plt.plot(df['time_leg'], df['error_leg'], label='Legendre', marker='s', alpha=0.5)
    plt.plot(df['time_lag'], df['error_lag'], label='Laguerre', marker='s', alpha=0.5)

    plt.legend()
    plt.xlabel('Time [s]')
    plt.ylabel('Error')
    plt.grid()
    plt.savefig(FIGDIR+'time_compare.png')
    # plt.show()
