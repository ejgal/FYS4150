#include <armadillo>
#include <tuple>
using namespace arma;

mat toeplitz(double, double, int);
void max_nondiagonal(mat, int, int &, int &);
void jacobi(int, double, double, double);
void rotate(mat &, int, int, int);
vec analytic_eigenvalues(int, double, double);
