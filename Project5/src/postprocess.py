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


def hovmuller(filename, ylabel=None):
    infile = DATADIR + filename + '.csv'
    outfile = FIGDIR + filename
    psi = pd.read_csv(infile, header=None, index_col=0, skiprows=6)
    x = psi.columns.values
    t = psi.index.values
    X, T = np.meshgrid(x, t)
    plt.contourf(X, T, psi.values)
    plt.xlabel('x$_i$')
    plt.ylabel(ylabel)
    plt.colorbar()
    plt.savefig(outfile + '.png')
    plt.savefig(outfile + '.pdf')
    plt.clf()


def hovmuller_four(filenames, outfile):
    outfile = FIGDIR + outfile
    plt.rc('figure', autolayout=False)
    figsize = get_size(columns=2, ratio=0.7)
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


def plot_error():
    # Error analysis jacobis method
    figsize = get_size(columns=2, ratio=0.7)
    fig, ax = plt.subplots(3, sharex=True, sharey=True, figsize=figsize)
    for target, axis in zip([1e-6, 1e-8, 1e-10], ax):
        abs, rel, nx = error_jacobi_bounded(target=target)
        axis.plot(nx, abs, label='Bounded', marker='x')
        abs, rel, nx = error_jacobi_periodic(target=target)
        axis.plot(nx, abs, label='Periodic', marker='o')
        axis.set_xscale('log')
        axis.set_yscale('log')
        axis.grid()
        axis.legend()
        axis.set_xlabel('Grid points')
        axis.set_ylabel('Absolute error')
    plt.savefig(FIGDIR + 'error_jacobi.png')
    plt.savefig(FIGDIR + 'error_jacobi.pdf')
    plt.clf()


def plot_2d(boundary, outfile, times=[0, 50, 100, 149]):
    plt.rc('figure', autolayout=False)
    figsize = get_size(columns=2, ratio=0.7)
    fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=figsize)
    levels = np.linspace(-1.5, 1.5, 10)
    for ax, time in zip(axes.flat, times):
        filename = DATADIR + boundary + '/' + 'psi_{:06.2f}.npy'.format(time)
        psi = np.load(filename)
        dx = 1/40
        nx = int(1/dx)
        if boundary == 'periodic':
            ny = nx + 1
            x = np.linspace(0, 1-dx, nx)
        else:
            nx = nx + 1
            x = np.linspace(0, 1, nx)
            ny = nx
        y = np.linspace(0, 1, ny)
        X, Y = np.meshgrid(x, y)
        c = ax.contourf(X, Y, psi, levels)
        ax.set_title('t={}'.format(time))
    fig.colorbar(c, ax=axes.ravel().tolist())
    fig.text(0.03, 0.5, 'y', ha='center', va='center', rotation='vertical', fontsize=14)
    fig.text(0.44, 0.03, 'X', ha='center', va='center', rotation='horizontal', fontsize=14)
    plt.savefig(FIGDIR + outfile + '.png')
    plt.savefig(FIGDIR + outfile + '.pdf')
    plt.clf()
    plt.rc('figure', autolayout=True)


if __name__ == '__main__':

    # Bounded
    hovmuller('psi_bounded_centered_sine', ylabel='t')
    hovmuller('psi_bounded_centered_gauss', ylabel='t')

    # Periodic
    hovmuller('psi_periodic_centered_short', ylabel='t')
    times = [0, 50, 150, 300, 500]
    file1 = 'psi_periodic_centered_long'
    file2 = 'psi_periodic_forward_long'
    compare(file1, file2, 'compare_dt_1', times)
    sigmas = [0.08, 0.10, 0.11, 0.12]
    filenames = []
    for sigma in sigmas:
        filenames.append('psi_periodic_gauss_{:.2f}'.format(sigma))
    hovmuller_four(filenames, 'hovmuller_sigma')

    plot_2d('periodic', 'periodic_2d')
    plot_2d('bounded', 'bounded_2d')

    # Jacobi error
    plot_error()

    # Stability plot CTCS
    fig, axes = plt.subplots(3, sharex=True, sharey=True)
    ax1, ax2, ax3 = axes.flat

    psi = pd.read_csv('../data/psi_long_centered_400.csv', header=None, index_col=0, skiprows=6)
    ax1.plot(np.max(np.abs(psi), axis=1), label='dt=4.00')

    psi = pd.read_csv('../data/psi_long_centered_629.csv', header=None, index_col=0, skiprows=6)
    ax2.plot(np.max(np.abs(psi), axis=1), label='dt=6.29')

    psi = pd.read_csv('../data/psi_long_centered_630.csv', header=None, index_col=0, skiprows=6)
    ax3.plot(np.max(np.abs(psi), axis=1), label='dt=6.30')

    for ax in axes.flat:
        ax.legend()
        ax.grid()
        ax.set_ylabel(r'max($|\psi|$)')
    plt.xscale('log')
    plt.ylim(0.5, 2)
    plt.xlabel('Time')
    plt.savefig(FIGDIR + 'stability_ctcs' + '.png')
    plt.savefig(FIGDIR + 'stability_ctcs' + '.pdf')
    plt.clf()

    # Stability plot comparison
    plt.subplots(figsize=get_size(columns=2, ratio=0.3))
    psi = pd.read_csv('../data/psi_long_forward_008.csv', header=None, index_col=0, skiprows=6)
    plt.plot(np.max(np.abs(psi), axis=1), label='FTCS, dt=0.08')
    psi = pd.read_csv('../data/psi_long_forward_005.csv', header=None, index_col=0, skiprows=6)
    plt.plot(np.max(np.abs(psi), axis=1), label='FTCS, dt=0.05')
    psi = pd.read_csv('../data/psi_long_centered.csv', header=None, index_col=0, skiprows=6)
    plt.plot(np.max(np.abs(psi), axis=1), label='CTCS, dt=1', alpha=0.7)
    plt.grid()
    plt.legend()
    plt.xscale('log')
    plt.xlabel('Time')
    plt.ylabel(r'max($|\psi|$)')
    plt.savefig(FIGDIR + 'stability_compare' + '.png')
    plt.savefig(FIGDIR + 'stability_compare' + '.pdf')
    plt.clf()
