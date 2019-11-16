from pytest import approx
import numpy as np
from ising import ising, expectation_values
import analytic as a

def test_jit():
    """
    Check that ising with and without numba gives close to the same
    values. Uses rel=0.001 since we did not want to clutter the ising
    function more by having an option to set a seed in the RNG.
    """
    tol = 0.001
    nojit,a,d = ising.py_func(2,100000,1)
    jit,a,d = ising(2,100000,1)
    for value1, value2 in zip(nojit[[0,1,3,4]], jit[[0,1,3,4]]):
        assert value1 == approx(value2, rel=tol)

if __name__ == '__main__':
    test_jit()
