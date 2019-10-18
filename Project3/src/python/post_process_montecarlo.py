import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np
import scipy.stats as st
import mpl_settings

parser_description = 'Analyze results of monte-carlo experiment.'
filepath_help = 'Filepath of file to analyze (.csv)'

DATADIR = '../../data/'
FIGDIR = '../../figures/'

# Initialize parser
parser = argparse.ArgumentParser(description=parser_description)
parser.add_argument('--input', default=DATADIR+'montecarlo.csv',help=filepath_help)


def print_CI(alpha, mean, std):
    z = st.norm.ppf(1-alpha/2.)
    L = mean - z*std
    U = mean + z*std
    for l,u in zip(L,U):
        print('C.I, {}: [{:.5f},{:.5f}]'.format(alpha,l,u))


def CI(alpha, mean, std):
    z = st.norm.ppf(1-alpha/2.)
    L = mean - z*std
    U = mean + z*std
    return L,U



if __name__ == '__main__':
    args = parser.parse_args()
    filename = args.input
    print(filename)

    # Load data
    df = pd.read_csv(filename)
    print(df)


    # Calculate and plot standard deviation versus N
    std_time_importance = (df['std_importance']/df['time_importance_pl'])
    std_time_brute = df['std_brute_pl']/df['time_brute_pl']
    std_time_ratio = std_time_brute/std_time_importance
    print(std_time_ratio)
    plt.xscale('log')
    plt.yscale('log')

    plt.plot(df['N'], std_time_brute, label='std/time brute', marker='o')
    plt.plot(df['N'], std_time_importance, label='std/time importance',marker='s')
    plt.plot(df['N'], std_time_ratio, label='std/time ratio',marker='x')
    plt.grid()
    plt.xlabel('N')
    plt.ylabel('standard deviation/time')
    plt.legend()
    plt.savefig(FIGDIR+'mc_std_time_ratio.png')
    plt.clf()


    # Plot standard deviation versus N
    plt.xscale('log')
    plt.yscale('log')

    plt.plot(df['N'], df['std_importance'], label='Brute', marker='o')
    plt.plot(df['N'], df['std_brute_pl'], label='Importance',marker='s')
    plt.plot(df['N'], df['std_brute_pl']/df['std_importance'], label='Brute/Importance',marker='x')
    plt.grid()
    plt.xlabel('N')
    plt.ylabel('standard deviation/time')
    plt.legend()
    plt.savefig(FIGDIR+'mc_std_time.png')
    plt.clf()




    # loglog plot of error
    plt.xscale('log')
    plt.yscale('log')
    df['error_brute_pl'] = np.abs(df['error_brute_pl'])
    df['error_importance'] = np.abs(df['error_importance'])
    plt.plot(df['N'],df['error_brute_pl'], label='error_brute', marker='s')
    plt.plot(df['N'],df['error_importance'], label='error_importance', marker='o')
    plt.plot(df['N'], df['error_brute_pl']/df['error_importance'], label='error brute/error importance', marker='x')

    plt.xlabel('N')
    plt.ylabel('Error')
    plt.legend()
    plt.grid()

    plt.savefig(FIGDIR+'mc_error.png')
    plt.clf()



    # Plot time ratio parallel unparallel
    time_ratio = df['time_importance']/df['time_importance_pl']
    plt.xscale('log')
    plt.plot(df['N'],time_ratio, label='Unparallelized/Parallelized', marker='s')
    plt.xlabel('N')
    plt.ylabel('Time ratio')
    plt.legend()
    plt.grid()
    plt.savefig(FIGDIR+'mc_time_ratio.png')
    # plt.show()
    plt.clf()



    # "3D" plot of std, error and time
    # plt.xscale('log')
    # plt.yscale('log')
    # ax1 = plt.scatter(df['std_importance'], df['error_importance'],c=np.log10(df['time_importance_pl']),marker='o', cmap='Oranges')
    # ax2 = plt.scatter(df['std_brute_pl'], df['error_brute_pl'],c=np.log10(df['time_brute_pl']),marker='s', cmap='Greens')
    #
    # plt.xlabel('Standard deviation')
    # plt.ylabel('Error')
    # plt.colorbar(ax1)
    # plt.colorbar(ax2)
    # plt.savefig(FIGDIR+'std_error_time.png')
    # plt.show()


    # Plot confidence intervals
    # confidence_brute = CI(0.01, df['result_brute_pl'], df['std_brute_pl'])
    # confidence_importance = CI(0.01, df['result_importance'], df['std_importance'])
    # plt.clf()
    # plt.xscale('log')
    # plt.yscale('log')
    # for i in range(0,len(df['N'].values)):
    #     # result = df['result_brute_pl'].values[i]
    #     L = confidence_brute[0].values[i]
    #     U = confidence_brute[1].values[i]
    #     plt.vlines(df['N'].values[i], L,U, color='r')
    #     L = confidence_importance[0].values[i]
    #     U = confidence_importance[1].values[i]
    #     plt.vlines(df['N'].values[i], L,U)
    # plt.show()


    # Error bar plotting
    # plt.clf()
    # analytical = (5*np.pi**2/16**2)
    # alpha = 0.05
    # err = df['std_importance']*st.norm.ppf(1-alpha/2.)
    # print(err)
    # ax = df.plot.bar('N','result_importance',yerr=err.values)
    # plt.axhline(analytical,color='r',linestyle='--',label='Analytical')
    # plt.legend()
    # plt.show()
