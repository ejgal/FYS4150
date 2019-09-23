#include <armadillo>
#include <iostream>
#include "time.h"
#include <iomanip>

#include "linalg.h"

using namespace std;
using namespace arma;

void compare_jacobi_armadillo(int n, const char* filename) {
  // Initialize variables
  double h = 1./(n+1);
  double hh = h*h;
  double a = -1./hh;
  double d = 2./hh;
  vec eigval = vec(n);

  ofstream ofile;
  ofile.open(filename, ios::app); // Open file in append mode
  ofile << setiosflags(ios::showpoint);
  ofile << setprecision(10);

  // Time one run of jacobis method
  mat A = toeplitz(a,d,n);
  clock_t start, finish;
  start = clock();
  int iterations = jacobi(n, a, d, eigval, A, pow(10.0, -8));
  finish = clock();
  ofile << n << "," << iterations << ',';
  double timeused = (double) (finish - start)/(CLOCKS_PER_SEC);
  ofile << timeused << ",";

  // Time one run of finding the eigenvalues with armadillo

  vec arma_eigval;
  mat arma_eigvec;

  start = clock();
  eig_sym(arma_eigval, arma_eigvec, A);

  // cx_vec eigval_arma = eig_sym( toeplitz(a, d, n) );
  finish = clock();
  timeused = (double)(finish - start)/(CLOCKS_PER_SEC);
  ofile << timeused << endl;
  ofile.close();
}


int main(int argc, char *argv[]) {
  int start = atoi(argv[1]);
  int stop = atoi(argv[2]);
  int runs = atoi(argv[3]);
  const char* filename = argv[4];

  cout << start << endl;
  cout << stop << endl;
  cout << runs << endl;

  // Write header line
  ofstream ofile;
  ofile.open(filename);
  ofile << "n,iterations,jacobi,armadillo" << endl;
  ofile.close();

  // Run experiment
  for (int i=start; i<=stop; i++) {
    for (int j=1; j<=runs; j++) {
      compare_jacobi_armadillo(i, filename);
    }
    // Print to keep track of progress
    cout << "n: " << i << endl;
  }

  // Write arguments to file
  ofile.open("../../data/last_run.txt");
  ofile << "start: " << start << endl;
  ofile << "stop: " << stop << endl;
  ofile << "runs: " << runs << endl;
  ofile.close();
}
