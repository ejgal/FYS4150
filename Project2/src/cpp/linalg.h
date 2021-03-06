#include <armadillo>
#include <tuple>
using namespace arma;

mat toeplitz(double, double, int);
void max_nondiagonal(mat&, int&, unsigned int&, unsigned int&);
int jacobi(int, double, double, mat&, double);
void rotate(mat &, int, int, int);
vec analytic_eigenvalues(int, double, double);
