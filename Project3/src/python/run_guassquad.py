from gaussQuad import gQuad
import argparse
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import roots_laguerre
import timeit
import pandas as pd
# Parser info
parser_description = 'Runs Gauss Quadrature integration.'
N_end = 'Runs Gauss Quadrature for n=nStart until N=Nend, default = 31.'
N_endDefault = 31
N_start = 'For which N to start with'
N_startDefault = 2
output_help = 'Filepath to output file (.csv)'
output_default = '../../data/gaussQuad.csv'


# Initialize parser
parser = argparse.ArgumentParser(description=parser_description)
parser.add_argument('--output', '--o', default=output_default, help=output_help)
parser.add_argument('--n','--N_start', type=int, default=N_startDefault, help=N_start)
parser.add_argument('--N', '--N_end', type=int, default = N_endDefault, help=N_end)


if __name__ == '__main__':
    args = parser.parse_args()
    N =  args.N
    nstart = args.n
    if nstart != 1:
        nstart = nstart -1
    output = args.output
    resultLeg = []
    errorLeg = []
    resultLag = []
    errorLag = []
    timeLeg = []
    timeLag = []
    Ns = []
    for n in range(nstart,N+1):
        print('Running for N = {}'.format(N))

        xleg, wleg = leggauss(n)
        xlag, wlag = roots_laguerre(n)

        leQuad = gQuad(xleg,xlag,wleg,wlag)
        timer = timeit.Timer(lambda: leQuad.integrate_legrende(-2,2))
        time = timer.timeit(1)
        resultLeg.append(leQuad.getResult)
        errorLeg.append(leQuad.error)
        timeLeg.append(time)
        leQuad.integrate_laguerre()
        timer = timeit.Timer(lambda: leQuad.integrate_laguerre())
        time = timer.timeit(1)
        errorLag.append(leQuad.error)
        resultLag.append(leQuad.getResult)
        timeLag.append(time)
        Ns.append(n)



    data = np.array([np.array(resultLeg[1:]),
            np.array(resultLag[1:]),np.array(errorLeg[1:]), np.array(errorLag[1:])
            , np.array(timeLeg[1:]), np.array(timeLag[1:])]).transpose()

    columns = ['result_leg', 'result_lag', 'error_leg', 'error_lag', 'time_leg', 'time_lag']
    index = Ns[1:]
    df = pd.DataFrame(data=data,index=index, columns=columns)#, columns=columns)
    df.index.name='N'
    df.to_csv(output)
