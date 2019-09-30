#include <armadillo>
#include <iostream>
#include "time.h"
#include <iomanip>

#include "linalg.h"

using namespace std;
using namespace arma;

void compare_jacobi_armadillo(int n, const char* filename) {
  /* Run the jacobi algorithm and armadillos eig_symfor a matrix of size nxn and
  /* write the number of iterations needed and the time used to file */

  // Initialize variables
  double h = 1./(n+1);
  double hh = h*h;
  double a = -1./hh;
  double d = 2./hh;

  ofstream ofile;
  ofile.open(filename, ios::app); // Open file in append mode
  ofile << setiosflags(ios::showpoint);
  ofile << setprecision(10);

  // Time one run of jacobis method
  mat A = toeplitz(a,d,n);
  clock_t start, finish;
  start = clock();
  double tolerance = pow(10.0, -9);
  int iterations = jacobi(n, a, d, A, tolerance);
  finish = clock();
  ofile << n << "," << iterations << ',';
  double timeused = (double) (finish - start)/(CLOCKS_PER_SEC);
  ofile << timeused << ",";

  // Time one run of finding the eigenvalues with armadillo
  vec arma_eigval;
  mat arma_eigvec;
  start = clock();
  eig_sym(arma_eigval, arma_eigvec, A);
  finish = clock();
  timeused = (double)(finish - start)/(CLOCKS_PER_SEC);
  ofile << timeused << endl;
  ofile.close();
}


int main(int argc, char *argv[]) {
  int runs = atoi(argv[1]);
  const char* filename = argv[2];
  vec Ns = {100, 120, 150, 180, 200, 220, 250, 275, 300, 350};

  // Write header line
  ofstream ofile;
  ofile.open(filename);
  ofile << "n,iterations,jacobi,armadillo" << endl;
  ofile.close();

  // Run experiment
  for (int i=0; i<Ns.size() ; i++) {
    for (int j=1; j<=runs; j++) {
      compare_jacobi_armadillo(Ns(i), filename);
    }
    // Print to keep track of progress
    cout << "n: " << Ns(i) << endl;
  }
}
