import numpy as np
import matplotlib.pyplot as plt
import argparse

from ising import ising, expectation_values, write_run, write_header
from plot import *


DATADIR = '../data/'


# Parser info
parser_description = 'Run ising model to check for equilibrium.'

output_help = 'Path to store file'
output_def = DATADIR + 'equilibrium.csv'

exp_help = 'Highest power of 10 Monte Carlo cycles to run experiment for.'
exp_def = 6

points_help = 'Number of different sample sizes to run for. '
points_help += 'Logarithmically spaced between 10 and 10^exp'
points_def = 30

ordered_help = 'Initial spin direction. 1 = up, -1 = down, 0 = random.'
oredered_def = 0

# Initialize parser
parser = argparse.ArgumentParser(description=parser_description)
parser.add_argument('--output', '--o', default=output_def, help=output_help)
parser.add_argument('--exp', '--e', default=exp_def, help=exp_help)
parser.add_argument('--points', '--p', default=points_def,help=points_help)
parser.add_argument('--ordered', default=ordered_def, help=ordered_help)



if __name__ == '__main__':
    # Run parser and store input to variables
    args = parser.parse_args()
    exp = args.exp
    output = args.output
    points = args.points
    ordered = args.ordered

    L = 20
    N = points
    cycles = np.logspace(2,6,N)
    delay = 0

    write_header(filename)
    for T in [1., 2.4]:
        for i in range(0,len(cycles)):
            print('T: {}, cycle: {}/{}'.format(T, int(cycles[i]), cycles[-1]))
            values, accepted = ising(L,cycles[i],T, delay=0, ordered=0)
            expect = expectation_values(values, cycles[i],L,T)
            write_run(filename, expect, T,L,ordered,cycles[i],delay,accepted)
