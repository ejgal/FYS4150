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


# Initialize parser
parser = argparse.ArgumentParser(description=parser_description)
parser.add_argument('--output', '--o', default=output_default, help=output_help)
parser.add_argument('--exp', type=int, default=exp_default, help=exp_help)


if __name__ == '__main__':

    # Run parser and store input to variables
    args = parser.parse_args()
    exp = args.exp
    output = args.output

    analytical = 5*np.pi**2/16**2

    Ns = [10**i for i in range(1,exp+1)]
    runs = len(Ns)

    # Arrays for storing experiment data
    std_brute = np.zeros(runs)
    std_importance = np.zeros(runs)
    time_brute = np.zeros(runs)
    time_importance = np.zeros(runs)
    time_importance_pl = np.zeros(runs)
    result_brute = np.zeros(runs)
    result_importance = np.zeros(runs)

    for N,i in zip(Ns,range(0,runs)):
        N = int(N)
        print('Running for N = {:.1e}'.format(N))

        # Run brute force montecarlo
        start = time.time()
        s1,s2 = mc.montecarlo_brute(N,-2,2)
        end = time.time()
        std_brute[i] = np.sqrt(mc.variance(s1,s2,N))
        time_brute[i] = end-start
        result_brute[i] = s1

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
    data = np.array([result_brute, result_importance, std_brute, std_importance, time_brute, time_importance, time_importance_pl]).transpose()
    columns = ['result_brute','result_importance','std_brute','std_importance','time_brute','time_importance', 'time_importance_pl']
    index = Ns
    df = pd.DataFrame(data=data,index=index, columns=columns)#, columns=columns)
    df.index.name='N'
    df['error_brute'] = df['result_brute'] - analytical
    df['error_importance'] = df['result_importance'] - analytical
    df.to_csv(output)
