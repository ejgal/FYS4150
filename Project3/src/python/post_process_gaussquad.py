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
parser.add_argument('--input', default=DATADIR+'gauss_2_30.csv',help=filepath_help)


if __name__ == '__main__':
    args = parser.parse_args()
    filename = args.input
    print(filename)

    # Load data
    df = pd.read_csv(filename)
    print(df)

    # loglog plot of error
    plt.xscale('log')
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

    #
