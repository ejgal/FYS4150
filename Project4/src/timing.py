from ising import ising
import time

if __name__ == '__main__':
    """
    Estimate run time for phase_transitions.py
    """

    # Info about machine we want to run at
    cores = 4.
    freq = 3200.

    # Run settings
    T = 1.
    N = 6000
    Tstart = 2.
    Tend = 2.8
    dT = 0.004
    numT = (Tend-Tstart)/(dT) # Number of T values to run for
    Nscale = 100. # Ratio of cycles


    timing = 0
    # One run for each grid size
    for L in [40,60,80,100]:
        ising(10,N,T) # Warmup run, no timing
        start = time.time()
        ising(L, N, T)
        end = time.time()
        timing += end-start

    # Get system frequency
    with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq') as file:
        frequency = float(file.readline())/1000.
    CPUscale = freq/frequency # Mhz ratio

    scaled_time = timing*numT*Nscale/(CPUscale*cores*60*60)
    print('Run with these values will take {:.2f} hours'.format(scaled_time))
