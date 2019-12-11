import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from error import error_jacobi_bounded, error_jacobi_periodic

DATADIR = '../data/'
FIGDIR = '../figures/'
# Plot settings
colwidth = 418.25368
width = colwidth / 72.27
height = width / 1.618
figsize = [width, height]
fontsize = 12
ticksize = 8
legendsize = 10
DPI = 300


def get_size(columns=2, ratio=False):
    colwidth = 418.25368
    if columns == 1:
        colwidth *= 0.5
    width = colwidth / 72.27
    if not ratio:
        height = width / 1.618
    else:
        height = ratio*width
    return [width, height]


# Set plot settings
plt.rc('text', usetex=True)

plt.rc('figure', autolayout=True)
plt.rc('figure', figsize=[width, height])
plt.rc('figure', dpi=DPI)

plt.rc('xtick', labelsize=ticksize)
plt.rc('ytick', labelsize=ticksize)

plt.rc('axes', labelsize=fontsize)
plt.rc('axes', titlesize=fontsize)

plt.rc('legend', fontsize=legendsize)
plt.rc('legend', numpoints=1)
plt.rc('legend', handletextpad=0.3)


def compare(filename1, filename2, outfile, times=[0, 50, 150]):
    infile1 = DATADIR + filename1 + '.csv'
    infile2 = DATADIR + filename2 + '.csv'
    outfile = FIGDIR + outfile

    psi1 = pd.read_csv(infile1, header=None, index_col=0, skiprows=6)
    psi2 = pd.read_csv(infile2, header=None, index_col=0, skiprows=6)
    fig, ax = plt.subplots(2, figsize=get_size(columns=2))
    for axis, psi in zip(ax, [psi1, psi2]):
        for t in times:
            psi.iloc[t, :].plot(label='t={}'.format(t), ax=axis)
        axis.legend(loc='right')
        axis.grid()

    plt.savefig(outfile + '.png')
    plt.savefig(outfile + '.pdf')
    plt.clf()


def hovmuller(filename):
    infile = DATADIR + filename + '.csv'
    outfile = FIGDIR + filename
    psi = pd.read_csv(infile, header=None, index_col=0, skiprows=6)
    x = psi.columns.values
    t = psi.index.values
    X, T = np.meshgrid(x, t)
    plt.contourf(X, T, psi.values)
    plt.xlabel('x')
    plt.ylabel('t')
    plt.colorbar()
    plt.savefig(outfile + '.png')
    plt.savefig(outfile + '.pdf')
    plt.clf()


def hovmuller_four(filenames, outfile):
    outfile = FIGDIR + outfile
    plt.rc('figure', autolayout=False)
    figsize = get_size(columns=2, ratio=1)
    fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=figsize)
    levels = np.linspace(-1.25, 1.25, 10)
    for file, ax in zip(filenames, axes.flat):
        infile = DATADIR + file + '.csv'
        psi = pd.read_csv(infile, header=None, index_col=0, skiprows=6)
        x = psi.columns.values
        t = psi.index.values
        X, T = np.meshgrid(x, t)
        c = ax.contourf(X, T, psi.values, levels)
        ax.set_xlabel('x$_i$')
        ax.set_ylabel('t')
    fig.colorbar(c, ax=axes.ravel().tolist())
    plt.savefig(outfile + '.png')
    plt.savefig(outfile + '.pdf')
    plt.clf()
    plt.rc('figure', autolayout=True)


if __name__ == '__main__':

    # Error analysis jacobis method
    fig, ax = plt.subplots()
    abs, rel, nx = error_jacobi_bounded()
    ax.plot(nx, abs, label='Bounded')
    abs, rel, nx = error_jacobi_periodic()
    ax.plot(nx, abs, label='Periodic')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid()
    plt.legend()
    plt.xlabel('Grid points')
    plt.ylabel('Absolute error')
    plt.savefig(FIGDIR + 'error_jacobi.png')
    plt.savefig(FIGDIR + 'error_jacobi.pdf')
    plt.clf()
    
    # # Bounded
    hovmuller('psi_bounded_centered_sine')
    hovmuller('psi_bounded_centered_gauss')

    # # Periodic
    hovmuller('psi_periodic_centered_short')

    times = [0, 50, 150, 300, 500]
    file1 = 'psi_periodic_centered_long'
    file2 = 'psi_periodic_forward_long'
    compare(file1, file2, 'compare_dt_1', times)

    sigmas = [0.08, 0.10, 0.11, 0.12]
    filenames = []
    for sigma in sigmas:
        filenames.append('psi_periodic_gauss_{:.2f}'.format(sigma))
    hovmuller_four(filenames, 'hovmuller_sigma')
