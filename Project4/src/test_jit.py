from pytest import approx

from ising import ising

def test_jit():
    nojit,acc1 = ising.py_func(2,100000,1)
    jit,acc2 = ising(2,100000,1)
    for value1, value2 in zip(nojit[[0,1,3,4]], jit[[0,1,3,4]]):
        assert value1 == approx(value2, rel=0.001)

if __name__ == '__main__':
    test_jit()
