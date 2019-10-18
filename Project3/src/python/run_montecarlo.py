import argparse
import numpy as np
import montecarlo as mc
import pandas as pd
import time


# Parser info
parser_description = 'Runs Monte-Carlo simulation.'
exp_help = 'Highest power of 10 to run experiment for.'
exp_default = 8

output_help = 'Filepath to output file (.csv)'
output_default = '../../data/montecarlo.csv'

points_help = 'Number of different sample sizes to run for. '
points_help += 'Logarithmically spaced between 10 and 10^exp'
points_default = 20

# Initialize parser
parser = argparse.ArgumentParser(description=parser_description)
parser.add_argument('--output', '--o', default=output_default, help=output_help)
parser.add_argument('--exp', '--e', type=int, default=exp_default, help=exp_help)
parser.add_argument('--points', '--p', type=int, default=points_default, help=points_help)

if __name__ == '__main__':
    # Run parser and store input to variables
    args = parser.parse_args()
    exp = args.exp
    output = args.output
    points = args.points

    analytical = 5*np.pi**2/16**2

    # Set up which sample sizes to run with
    Ns = np.logspace(1,exp,points)
    runs = len(Ns)

    # Arrays for storing experiment data
    std_brute_pl = np.zeros(runs)
    std_importance = np.zeros(runs)
    time_brute_pl = np.zeros(runs)
    time_importance = np.zeros(runs)
    time_importance_pl = np.zeros(runs)
    result_brute_pl = np.zeros(runs)
    result_importance = np.zeros(runs)

    for N,i in zip(Ns,range(0,runs)):
        N = int(N)
        print('Running for N = {:.1e}'.format(N))

        # Run brute force montecarlo
        start = time.time()
        s1,s2 = mc.montecarlo_brute(N,-2,2)
        end = time.time()
        std_brute_pl[i] = np.sqrt(mc.variance(s1,s2,N))
        time_brute_pl[i] = end-start
        result_brute_pl[i] = s1

        # Run monte-carlo with importance sampling (unparallellized)
        start = time.time()
        s1,s2 = mc.montecarlo_importance(N)
        end = time.time()
        std_importance[i] = np.sqrt(mc.variance(s1,s2,N))
        time_importance[i] = end-start
        result_importance[i] = s1

        # Run monte-carlo with importance sampling (parallelized)
        start = time.time()
        s1,s2 = mc.montecarlo_importance_parallel(N)
        end = time.time()
        time_importance_pl[i] = end-start

    # Store data to csv file
    data = np.array([result_brute_pl, result_importance, std_brute_pl, std_importance, time_brute_pl, time_importance, time_importance_pl]).transpose()
    columns = ['result_brute_pl','result_importance','std_brute_pl','std_importance','time_brute_pl','time_importance', 'time_importance_pl']
    index = Ns
    df = pd.DataFrame(data=data,index=index, columns=columns)
    df.index.name='N'
    df['error_brute_pl'] = df['result_brute_pl'] - analytical
    df['error_importance'] = df['result_importance'] - analytical

    # Discard the first run
    df = df.iloc[1:,:]
    df.to_csv(output)
