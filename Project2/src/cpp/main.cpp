#include <armadillo>
#include <iostream>
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

  // Time one run of jacobis method
  auto start = std::chrono::high_resolution_clock::now();
  jacobi(n, a, d, eigval, pow(10, -8));
  auto finish = std::chrono::high_resolution_clock::now();
  ofile << n << ",";
  ofile << std::chrono::duration_cast<std::chrono::milliseconds>(finish - start).count();

  // Time one run of finding the eigenvalues with armadillo
  start = std::chrono::high_resolution_clock::now();
  cx_vec eigval_arma = eig_gen( toeplitz(a, d, n) );
  finish = std::chrono::high_resolution_clock::now();
  ofile << ",";
  ofile << std::chrono::duration_cast<std::chrono::milliseconds>(finish - start).count();
  ofile << endl;
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
  ofile << "n,jacobi,armadillo";
  ofile.close();
  for (int i=start; i<=stop; i++) {
    for (int j=1; j<=runs; j++) {
      compare_jacobi_armadillo(i, filename);
    }
    cout << "n: " << i << endl;
  }

}
