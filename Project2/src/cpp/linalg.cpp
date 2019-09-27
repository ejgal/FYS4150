#include "linalg.h"
#include <tuple>
#include <chrono>
#include "time.h"
#include <iomanip>

using namespace arma;
using namespace std;


vec analytic_eigenvalues(int n, double a, double d) {
  vec eigval = vec(n);
  for (int i=1; i<=n; i++) {
    eigval(i-1) = d + 2*a*cos(i*datum::pi/(n+1));
  }
  return eigval;
}

mat toeplitz(double a, double d, int N) {
  // Build a NxN toeplitz matrix with diagonal elements d and offdiagonal
  // elements d
  // mat A = mat(N, N, fill::zeros);
  mat A = zeros<mat>(N,N);
  for (int i=0; i<N; i++) {
    A(i,i) = d; // Fill diagonal elements
  }
  for (int i=0; i<N-1; i++){
    A(i+1, i) = a; // fill lower diagonal
    A(i, i+1) = a; // fill upper diagonal
  }
  return A;
}

void max_nondiagonal(mat& A, int& n, unsigned& row, unsigned int& col) {
  // Find indexes of the offdiagonal element with the largest absolute value
  // for a symmetric matrix
  double current_max = 0.0;
  double a_ij;
  for (unsigned int i=0; i<n; i++) {
    for (unsigned int j=i+1; j<n; j++) { // Symmetric matrix -> only loop over upper half
      a_ij = fabs(A(i,j));
      if (a_ij >= current_max) {
        row = i;
        col = j
        current_max = a_ij; // update maximum value
      }
    }
  }
}




void rotate(mat &A, int N, int k, int l) {
  double temp_a_ik; double temp_a_il; double temp_a_kk; double temp_a_ll;
  double c; double s; double tau; double t;
  tau = (A(l,l) - A(k,k))/(2*A(k,l));
  if (tau > 0) {
    t = 1./(tau + sqrt(1. + tau*tau));
  } else {
    t = -1./(-tau + sqrt(1. + tau*tau));
  }
  c = 1./(sqrt(1+t*t));
  s = t*c;
  for (int i=0; i<N; i++) {
    if ( i != k && i != l) {
      temp_a_ik = A(i,k);  // Store elements that will be overwritten
      temp_a_il = A(i,l); // Store elements that will be overwritten
      A(i,k) = temp_a_ik*c - temp_a_il*s; // Column k
      A(i,l) = temp_a_il*c + temp_a_ik*s; // Column l
      // Similarity transformation -> symmetric matrix
      A(k,i) = A(i,k); // Row k
      A(l,i) = A(i,l); // Row l
    }
  }
  temp_a_kk = A(k,k); // Store elements that will be overwritten
  temp_a_ll = A(l,l); // Store elements that will be overwritten
  A(k,k) = temp_a_kk*c*c - 2*A(k,l)*c*s + temp_a_ll*s*s;
  A(l,l) = temp_a_ll*c*c + 2*A(k,l)*c*s + temp_a_kk*s*s;
  A(k,l) = 0.0;
  A(l,k) = 0.0;
}


int jacobi(int n, double a, double d, vec &eigval, mat &A, double epsilon) {
  unsigned int k=0; unsigned int l=0; double max_offdiag;
  int iterations=0;
  clock_t start, finish;
  cout << setiosflags(ios::showpoint);
  cout << setprecision(10);
  max_nondiagonal(A, n, k,l);
  max_offdiag = A(k,l);
  double elapsed_rotate = 0;
  double elapsed_max = 0;
  while (max_offdiag*max_offdiag  > epsilon) {
    start = clock();
    rotate(A, n, k, l);
    finish = clock();
    elapsed_rotate += (double) (finish - start)/(CLOCKS_PER_SEC);

    start = clock();
    max_nondiagonal(A,n,k,l);
    finish = clock();
    elapsed_max += (double) (finish - start)/(CLOCKS_PER_SEC);
    max_offdiag = A(k,l);
    iterations ++;
  }
  cout << "Time rotate: " << elapsed_rotate << endl;
  cout << "Find max: " << elapsed_max << endl;

  for (int i=0; i<n; i++) {
    eigval(i) = A(i,i);
  }
  return iterations;
}
