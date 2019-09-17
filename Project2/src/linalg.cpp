#include "linalg.h"
#include <tuple>
using namespace arma;
using namespace std;

mat toeplitz(double a, double d, int N) {
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
  double current_max = 0;
  row = 0;
  col = 0;
  for (int i=0; i<N; i++) {
    for (int j=0; j<N; j++) {
      if ((i != j) && (abs(A(i,j))) > current_max) {
        row = i;
        col = j;
        current_max = abs(A(i,j)); // update maximum value
      }
    }
  }
}

int main(int argc, char *argv[]) {
  cout << scientific;

  int N = atoi(argv[1]);
  double h = 1./N;
  double hh = h*h;
  double a = -1./hh;
  double d = 2./hh;
  mat A = toeplitz(a, d, N+1);
  double pi = datum::pi;
  // vec eigval;
  // eig_gen(eigval, A);
  cx_vec eigval = eig_gen( A );
  for (int i=1; i<=N+1; i++) {
    cout << d + 2*a*cos(i*pi/(N+2)) << endl;
  }
  cout << eigval << endl;


  int k = 0;
  int l = 0;
  max_nondiagonal(A, N+1, k, l);
  double epsilon = pow(10, -8);
  int count = 0;
  double max_A = A(k,l);
  while (max_A*max_A  > epsilon) {
    double c; double s; double tau; double t;

    max_nondiagonal(A, N+1, k, l); // find indexes of largest non-diag element
    // Calculate c and s (elements of transformation matrix)
    tau = (A(l,l) - A(k,k))/(2*A(k,l));
    if (tau > 0) {
      t = 1./(tau + sqrt(1. + tau*tau));
    } else {
      t = -1./(-tau + sqrt(1. + tau*tau));
    }
    c = 1./(sqrt(1+t*t));
    s = t*c;

    // Alternative way of calculating transformed matrix with fewer calculations
    for (int i=0; i<N+1; i++) {
      if ( i != k && i != l) {
        double temp_a_ik = A(i,k);  // Store elements that will be overwritten
        double temp_a_il = A(i,l); // Store elements that will be overwritten
        A(i,k) = temp_a_ik*c - temp_a_il*s; // Column k
        A(i,l) = temp_a_il*c + temp_a_ik*s; // Column l
        // Similarity transformation -> symmetric matrix
        A(k,i) = A(i,k); // Row k
        A(l,i) = A(i,l); // Row l
      }
    }
    double temp_a_kk = A(k,k); // Store elements that will be overwritten
    double temp_a_ll = A(l,l); // Store elements that will be overwritten
    A(k,k) = temp_a_kk*c*c - 2*A(k,l)*c*s + temp_a_ll*s*s;
    A(l,l) = temp_a_ll*c*c + 2*A(k,l)*c*s + temp_a_kk*s*s;
    A(k,l) = 0.0;
    A(l,k) = 0.0;
    // End transformation function - move this into a function


    max_nondiagonal(A,N+1,k,l);
    max_A = A(k,l);
    count ++;

    // Print diagnostics every 1000 steps
    if (count % 1000 == 0) {
      cout << "Count: " << count << endl;
      cout << "Max nondiagonal squared: " << max_A*max_A << endl;
      cout << "Indexes: " << k << " " << l << endl;
      cout << "tau: " << tau << endl;
      cout << "tan(theta): " << t << endl;
      cout << "cos(theta): " << c << endl;
      cout << "sin(theta): " << s << endl << endl;
    }
  }

  // Print eigenvalues
  cout << scientific;
  for (int i=0; i<N+1; i++) {
    cout << "eigenvalue " << i << ": " << A(i,i) << endl;
  }

  cout << "Transformations performed: " << count << endl;
}
