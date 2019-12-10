import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


DATADIR = '../data/'
FIGDIR = '../figures/'


def compare(filename, times=[0, 50, 150]):
    infile = DATADIR + filename + '.csv'
    outfile = FIGDIR + filename + '.png'

    psi = pd.read_csv(infile, header=None, index_col=0)
    for t in times:
        psi.iloc[t, :].plot(label='t={}'.format(t))
    plt.legend()
    plt.grid()
    plt.savefig(outfile)
    plt.clf()


def hovmuller(filename):
    infile = DATADIR + filename + '.csv'
    outfile = FIGDIR + filename + '.png'
    psi = pd.read_csv(infile, header=None, index_col=0)
    x = psi.columns.values
    t = psi.index.values
    X, T = np.meshgrid(x, t)
    plt.contourf(X, T, psi.values)
    plt.xlabel('x')
    plt.ylabel('t')
    plt.colorbar()
    plt.savefig(outfile)
    plt.clf()


if __name__ == '__main__':

    times = [0, 50, 150, 300]
    compare('psi_periodic_centered_1_sine', times)
    compare('psi_periodic_forward_1_sine', times)

    # Bounded
    hovmuller('psi_bounded_centered_0.1_sine')
    hovmuller('psi_bounded_centered_0.1_gauss_0.10')

    # Periodic
    hovmuller('psi_periodic_centered_0.1_sine')
    hovmuller('psi_periodic_centered_0.1_gauss_0.08')
    hovmuller('psi_periodic_centered_0.1_gauss_0.09')
    hovmuller('psi_periodic_centered_0.1_gauss_0.10')
    hovmuller('psi_periodic_centered_0.1_gauss_0.11')
    hovmuller('psi_periodic_centered_0.1_gauss_0.12')
