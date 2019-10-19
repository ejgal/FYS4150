import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np
import matplotlib as mpl

# Figure settings
mpl.rc('figure', figsize=[10,6])
mpl.rc('xtick', labelsize=20)
mpl.rc('ytick', labelsize=20)
mpl.rc('legend', fontsize=16)
mpl.rc('axes', labelsize=20)


DATADIR = '../../data/'
FIGDIR = '../../figures/'

# Parser settings
parser_description = 'Analyze results of monte-carlo and gaussian quadrature experiments.'
gauss_help = 'Filepath of gaussian quadrature results.'
gauss_default = DATADIR + 'gauss_current.csv'

mc_help = 'Filepath of monte-carlo results.'
mc_default = DATADIR + 'montecarlo_current.csv'

# Initialize parser
parser = argparse.ArgumentParser(description=parser_description,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--gauss',help=gauss_help, default=gauss_default)
parser.add_argument('--mc', help=mc_help, default=mc_default)


def plot(x,ys,labels,markers,xlabel,ylabel,filename,loglog=True,logy=False):
    if logy:
        loglog=False
        plt.yscale('log')
    if loglog:
        plt.xscale('log')
        plt.yscale('log')

    for i in range(len(ys)):
        plt.plot(x,ys[i],label=labels[i],marker=markers[i])
    plt.grid()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(FIGDIR+filename)
    plt.clf()

if __name__ == '__main__':
    # Run parser
    args = parser.parse_args()
    gauss_file = args.gauss
    mc_file = args.mc

    # Load data
    mc = pd.read_csv(mc_file)
    gauss = pd.read_csv(gauss_file)

    # Take absolute values of errors
    mc['error_brute_pl'] = np.abs(mc['error_brute_pl'])
    mc['error_importance'] = np.abs(mc['error_importance'])
    gauss['error_lag'] = np.abs(gauss['error_lag'])
    gauss['error_leg'] = np.abs(gauss['error_leg'])


    #### Monte-Carlo results

    # Loglog standard deviation
    std_ratio =  mc['std_brute_pl']/mc['std_importance']
    ys = [mc['std_importance'],mc['std_brute_pl'], std_ratio]
    labels = ['Importance', 'Brute', 'Brute/Importance']
    markers = ['o','s','x']
    x = mc['N']
    xlabel = 'Sample size'
    ylabel = 'Standard deviation'
    file = 'mc_std_time.png'
    plot(x,ys,labels, markers,xlabel,ylabel,file)

    # Loglog plot of error
    error_ratio = mc['error_brute_pl']/mc['error_importance']
    ys = [mc['error_importance'],mc['error_brute_pl'],error_ratio]
    ylabel = 'Error'
    file = 'mc_error.png'
    plot(x,ys,labels,markers,xlabel,ylabel,file)

    # Plot time ratio parallel unparallel
    time_ratio = mc['time_importance']/mc['time_importance_pl']
    plt.xscale('log')
    plt.plot(mc['N'],time_ratio, label='Unparallelized/Parallelized', marker='s')
    plt.xlabel(xlabel)
    plt.ylabel('Time ratio')
    plt.legend()
    plt.grid()
    plt.savefig(FIGDIR+'mc_time_ratio.png')
    plt.clf()

    # "3D" plot of std, error and time
    plt.xscale('log')
    plt.yscale('log')
    plt.grid()
    ax1 = plt.scatter(mc['std_importance'], mc['error_importance'],c=np.log10(mc['time_importance_pl']),marker='o', cmap='Oranges')
    ax2 = plt.scatter(mc['std_brute_pl'], mc['error_brute_pl'],c=np.log10(mc['time_brute_pl']),marker='s', cmap='Greens')
    plt.xlabel('Standard deviation')
    plt.ylabel('Error')
    plt.colorbar(ax1)
    plt.colorbar(ax2)
    plt.savefig(FIGDIR+'std_error_time.png')
    plt.clf()


    #### GQ results

    # Plot GQ errors
    error_ratio =  gauss['error_leg']/gauss['error_lag']
    ys = [gauss['error_leg'], gauss['error_lag'], error_ratio]
    labels = ['Legendre', 'Laguerre', 'Legendre/Laguerre']
    markers = ['o','s','x']
    x = gauss['N']
    xlabel = 'Integration points'
    ylabel = 'Error'
    file = 'gauss_error.png'
    plot(x,ys,labels,markers,xlabel,ylabel,file,logy=True)

    # Timings of gauss quadrature
    time_ratio = gauss['time_leg']/gauss['time_lag']
    ys = [gauss['time_leg'], gauss['time_lag'], time_ratio]
    ylabel = 'Time [s]'
    file = 'gauss_time.png'
    plot(x,ys,labels,markers,xlabel,ylabel,file,logy=True)


    #### Compare GQ and Monte-Carlo results

    # Compare error/time ratios of gauss and monte-carlo
    plt.yscale('log')
    plt.xscale('log')
    alpha = 0.5
    plt.plot(mc['time_importance_pl'],mc['error_importance'], label='Importance',marker='x')
    plt.plot(mc['time_brute_pl'],mc['error_brute_pl'], label='Brute', marker='x')
    plt.plot(gauss['time_leg'], gauss['error_leg'], label='Legendre', marker='s', alpha=alpha)
    plt.plot(gauss['time_lag'], gauss['error_lag'], label='Laguerre', marker='s', alpha=alpha)
    plt.legend()
    plt.xlabel('Time [s]')
    plt.ylabel('Error')
    plt.grid()
    plt.savefig(FIGDIR+'time_compare.png')
