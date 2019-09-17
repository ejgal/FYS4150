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
    t = 1./(tau + sqrt(1 + tau*tau));
    c = 1./(sqrt(1+t*t));
    s = t*c;

    // Perform transformation
    // Easy way of calculating transformed matrix - replace with something more efficient.
    mat S = mat(N+1,N+1, fill::zeros);
    mat Sinv = mat(N+1,N+1, fill::zeros);
    for (int i = 0; i<N+1; i++){
      S(i,i) = 1;
      Sinv(i,i) = 1;
    }
    S(k,k) = c;
    S(l,l) = c;
    S(k,l) = s;
    S(l,k) = -s;
    Sinv(k,k) = c;
    Sinv(l,l) = c;
    Sinv(k,l) = -s;
    Sinv(l,k) = s;
    A = Sinv * A * S;
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
