#include "linalg.h"
#include <tuple>
#include <chrono>

using namespace arma;
using namespace std;

mat toeplitz(double a, double d, int N) {
  // Build a NxN toeplitz matrix with diagonal elements d and offdiagonal
  // elements d
  mat A = mat(N, N, fill::zeros);
  for (int i=0; i<N; i++) {
    A(i,i) = d; // Fill diagonal elements
  }
  for (int i=0; i<N-1; i++){
    A(i+1, i) = a; // fill lower diagonal
    A(i, i+1) = a; // fill upper diagonal
  }
  return A;
}

void max_nondiagonal(mat A, int N, int &row, int &col) {
  // Find indexes of the offdiagonal element with the largest absolute value
  double current_max = 0;
  row = 0;
  col = 0;
  for (int i=0; i<N; i++) {
    for (int j=0; j<N; j++) {
      if ((i != j) && (fabs(A(i,j))) >= current_max) {
        row = i;
        col = j;
        current_max = fabs(A(i,j)); // update maximum value
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
  for (int i=0; i<N+1; i++) {
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


void jacobi(int N, double a, double d, double epsilon) {
  double h = 1./N;
  double hh = h*h;
  a = -1./hh;
  d = 2./hh;
  mat A = toeplitz(a, d, N+1);
  double pi = datum::pi;
}
