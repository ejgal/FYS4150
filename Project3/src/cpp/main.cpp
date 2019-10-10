// #include "time.h"
// #include <iomanip>
#include <armadillo>
#include "gausslaguerre.cpp"
using namespace arma;
using namespace std;



int main(int argc, char *argv[]) {


  int n = 5;
  //   reserve space in memory for vectors containing the mesh points
  //   weights and function values for the use of the gauss-legendre
  //   method
  double *x = new double [n];
  double *w = new double [n];
  // Gauss-Laguerre is old-fashioned translation of F77 --> C++
  // arrays start at 1 and end at n
  double *xgl = new double [n+1];
  double *wgl = new double [n+1];
  // These arrays are used for improved Gauss-Legendre, mapping of
  // x \in [-1,1] to x \in [0, infinity)
  double *r = new double [n];
  double *s = new double [n];
  //   set up the mesh points and weights
  //   set up the mesh points and weights and the power of x^alf
  double alf = 0;
  gauss_laguerre(xgl,wgl, n, alf);

  for (int i=0; i<n; i++){
    cout << xgl[i] << " - " << wgl[i] << endl;
  }

  //
  //
  //
  // int n = 100;
  // vec r = linspace(0, n, n*10);
  // mat y = mat(n, n, fill::zeros);
  // for (int i = 0; i<n; i++){
  //   for (int j = 0; j<n; j++) {
  //     y(i,j) = exp(-4*(r(i)+r(j)));
  //   }
  // }
  // cout << r;
  // // cout << y;
  // r.save("../data/r.csv", csv_ascii);
  // y.save("../data/y.csv", csv_ascii);
}
