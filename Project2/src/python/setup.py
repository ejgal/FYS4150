from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name="jacobi",
    ext_modules=cythonize("jacobi.pyx"),
    include_dirs=[numpy.get_include()]
)