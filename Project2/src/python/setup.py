from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name="cythonJacobi",
    ext_modules=cythonize("cythonJacobi.pyx"),
    include_dirs=[numpy.get_include()]
)