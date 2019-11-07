from pytest import approx

from ising import ising

# def test_jit():
#     nojit = ising.py_func(2,1000,1)
#     jit = ising(2,1000,1)
#     for value1, value2 in zip(nojit, jit):
#         print(value1, value2)
#         assert value1 == approx(value2)
#
# if __name__ == '__main__':
#     test_jit()
