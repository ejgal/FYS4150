import numpy as np
import matplotlib.pyplot as plt
import argparse

from ising import ising, expectation_values, write_run, write_header
from parser import equi_parser
from settings import *


DATADIR = '../data/'

if __name__ == '__main__':
    # Run parser and store input to variables
    args = equi_parser().parse_args()
    exp = int(args.exp)
    output = args.output
    points = int(args.points)

    # Ignore ordered input...
    # ordered = int(args.ordered)

    L = 20
    N = points
    cycles = np.logspace(2,exp,N)
    delay = 0

    write_header(output)
    for T in [1., 2.4]:
        for ordered in [-1,0,1]:
            for i in range(0,len(cycles)):
                print('T: {}, cycle: {}/{}'.format(T, int(cycles[i]), cycles[-1]))
                values, accepted = ising(L,cycles[i],T, delay=0, ordered=0)
                expect = expectation_values(values, cycles[i],L,T)
                write_run(output, expect, T,L,ordered,cycles[i],delay,accepted)
