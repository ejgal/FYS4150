import numpy as np
from pytest import approx
from ising import ising, expectation_values

def test_expect():
    L = 2
    spins = L**2
    cycles = 5000000
    tol = 0.001
    delay = 500000
    T=1
    for i in range(0,2):
        values,acc,d = ising(L,cycles,T, delay)
        expect_delay = expectation_values(values, cycles,L,T, delay)

        values, acc,d = ising(L,cycles,T,0)
        expect = expectation_values(values, cycles,L,T, 0)
        cv_delay = expect_delay[3]
        cv = expect[3]
        assert cv == approx(cv_delay, rel=tol)
