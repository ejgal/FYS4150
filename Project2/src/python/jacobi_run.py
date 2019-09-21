import jacobi
import sys
import timeit
from line_profiler import LineProfiler
import cProfile as cp

if __name__ == "__main__":
    N = int(sys.argv[1])
    h = 1./(N)
    d = 2./(h**2)
    a = -1./(h**2)
    A = jacobi.cCreate_toeplitz(d, a,N)

   # pro = LineProfiler(jacobi.jacobiRun(A))
   # pro.print_stats()
    cp.run('jacobi.jacobiRun(A)')