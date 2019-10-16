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
    args = parser.parse_args()
    exp = args.exp
    output = args.output

    analytical = 5*np.pi**2/16**2

    Ns = [10**i for i in range(1,exp+1)]
    runs = len(Ns)

    std_brute = np.zeros(runs)
    error_brute = np.zeros(runs)
    std_importance = np.zeros(runs)
    error_importance = np.zeros(runs)
    time_brute = np.zeros(runs)
    time_importance = np.zeros(runs)
    time_importance_parallel = np.zeros(runs)

    for N,i in zip(Ns,range(0,runs)):
        N = int(N)
        print('Running for N = {:.1e}'.format(N))

        # Run brute force montecarlo
        start = time.time()
        s1,s2 = mc.montecarlo_brute(N,-2,2)
        end = time.time()
        std_brute[i] = np.sqrt(mc.variance(s1,s2,N))
        error_brute[i] = analytical - s1
        time_brute[i] = end-start

        # Run monte-carlo with importance sampling (unparallellized)
        start = time.time()
        s1,s2 = mc.montecarlo_importance(N)
        end = time.time()
        std_importance[i] = np.sqrt(mc.variance(s1,s2,N))
        error_importance[i] = analytical - s1
        time_importance[i] = end-start

        # Run monte-carlo with importance sampling (unparallelized)
        start = time.time()
        s1,s2 = mc.montecarlo_importance_parallel(N)
        end = time.time()
        time_importance_parallel[i] = end-start

    # print(std_brute)
    # print(std_importance)
    # print((error_brute - error_importance))
    # print((std_brute - std_importance))

    #
    data = np.array([std_brute, std_importance, error_brute, error_importance, time_brute, time_importance, time_importance_parallel]).transpose()
    columns = ['std_brute','std_importance','error_brute','error_importance','time_brute','time_importance', 'time_importance_parallel']
    index = Ns
    df = pd.DataFrame(data=data,index=index, columns=columns)#, columns=columns)
    df.index.name='N'
    df.to_csv(output)

        # mc.print_results(s1,s2,N)

        # s1,s2 = montecarlo_importance(N)
        # print_results(s1,s2)
    # print(std)
    # plt.plot(Ns, std)
    # plt.xscale("log")
    # plt.show()
    #
    # print(error)
    #
    # plt.plot(Ns, np.abs(error))
    # plt.xscale("log")
    # plt.show()



# import argparse
#
# parser = argparse.ArgumentParser(description='Calculates height of ball.')
#
# v_low = 0
# v_high = 500
# v_meta = '[{}-{}]'.format(v_low, v_high)
#
# parser.add_argument('--v', '--initial_velocity',
#                     choices=[i for i in range(v_low,v_high)],
#                     metavar='[{}-{}]'.format(v_low, v_high),
#                     type=float, default=30,
#                     help=' | m/s')
#
# parser.add_argument('--t', '--time',
#                     type=float,
#                     default=10,
#                     help=' | s')
#
# parser.add_argument('--g', '--gravity',
#                     type=float,
#                     default=9.81,
#                     help=' | m/s**2')
# g = args.g
# v0 = args.v
# t = args.t
#
# print v0*t - 0.5*g*t**2
