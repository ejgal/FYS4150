import numpy as np
from numba import jit,njit, prange

from settings import *
from ising import ising,write_header,write_run,expectation_values
from parser import phase_parser
from timing import estimate_time

@njit(parallel=True)
def phase_transitions(L,lenL,T,lenT,cycles,ordered,delay=0):
    """
    Run ising model for all combinations of temperature and grid width.

    Args:

        L: Grid widths
        T: Temperatures
        lenL: Number of widths
        lenT: Number of temperatures

        ordered, delay as in ising

    Returns:
        2D arrays of size lenLxlenT.
        E -
    """

    # Arrays for storing results
    E = np.zeros(shape=(lenL,lenT))
    M = np.zeros(shape=(lenL,lenT))
    Mabs = np.zeros(shape=(lenL,lenT))
    cv = np.zeros(shape=(lenL,lenT))
    suscept = np.zeros(shape=(lenL,lenT))
    accepted = np.zeros(shape=(lenL,lenT))


    # Start of parallelized loop
    for i in prange(lenT):
        for j in range(lenL):
            values, acc,d = ising(L[j],cycles,T[i], ordered=ordered,delay=delay)
            expect = expectation_values(values, cycles,L[j],T[i], delay)
            E[j,i] = expect[0]
            M[j,i] = expect[1]
            Mabs[j,i] = expect[2]
            cv[j,i] = expect[3]
            suscept[j,i] = expect[4]
            accepted[j,i] = acc

    # Return results, remember to store them.
    return E,M,Mabs,cv,suscept,accepted


if __name__ == '__main__':

    """
    Run ising model for L = [40,60,80,100] and different temperatures.
    """

    args = phase_parser().parse_args()
    output = args.output
    estimate = args.estimate
    Tstart = float(args.Tstart)
    Tstop = float(args.Tstop)
    dT = float(args.dT)
    delay = int(args.delay)
    ordered = int(args.ordered)
    cycles = int(args.cycles)

    # Estimate run time
    if estimate:
        estimate_time(Tstart,Tstop,dT,cycles)

        run = input("Continue with full run? (y/n):\n")
        if run != 'y':
            print('Exiting.')
            exit()

    # Grid sizes
    L = np.array([40,60,80,100])
    lenL = len(L)
    L = np.array(L)
    lenT = int((Tstop-Tstart)/(dT))
    T = np.linspace(Tstart, Tstop, lenT)

    # Write to output file before running experiment
    write_header(output)
    E,M,Mabs,cv,suscept,accepted = phase_transitions(L,lenL, T,lenT, cycles,ordered,delay=delay)

    # Write results to file
    for i in range(lenT):
        for j in range(lenL):
            expect = np.array([E[j,i],M[j,i],Mabs[j,i],cv[j,i],suscept[j,i]])
            write_run(output, expect, T[i],L[j],ordered,cycles,delay,accepted[j,i])
