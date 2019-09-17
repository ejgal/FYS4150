#include <armadillo>
#include <tuple>
using namespace arma;
mat toeplitz(double a, double d, int N);
void max_nondiagonal(mat A, int N, int &row, int &col);
