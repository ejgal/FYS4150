import time
import numpy as np
import datetime

from ising import ising


def estimate_time(Tstart,Tstop,dT,cycles,cores=4,freq=3200,):
    """
    Estimate run time for phase_transitions.py
    """

    # Run settings
    N = 6000 # Cycles to test run
    numT = int(np.ceil((Tstop-Tstart)/(dT))) # Number of T values to run for
    Nscale = cycles / N # Ratio of cycles
    timing = 0
    grids = [40,60,80,100]
    print('Values for full run')
    print('Number of temperatures: {}'.format(numT))
    print('Total number of runs: {}'.format(numT*len(grids)))

    print('Doing small runs with {} cycles to estimate run time.'.format(N))
    # One run for each grid size
    for L in grids:
        ising(10,N,Tstart) # Warmup run, no timing
        start = time.time()
        ising(L, N, Tstart)
        end = time.time()
        timing += end-start
        print('Test run with L={} took: {:.2f} seconds.'.format(L, end-start))

    # Get system frequency
    with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq') as file:
        frequency = float(file.readline())/1000.
    CPUscale = freq/frequency # Mhz ratio

    scaled_time = timing*numT*Nscale/(CPUscale*cores*60*60)
    print('Run with these values will take about {:.2f} hours'.format(scaled_time))

    now = datetime.date.today()
    deadline = datetime.datetime(2019,11,18,23,59,59)
    now = datetime.datetime.now()
    duration = deadline - now
    hours = duration.days*60 + duration.seconds/(60*60)
    print('Hours until project deadline: {:.2f}'.format(hours))
    



if __name__ == '__main__':
    estimate_time(2.1,2.3,0.001,1000000,cores=8,freq=3200)
