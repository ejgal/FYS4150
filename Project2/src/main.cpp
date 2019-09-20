#include <armadillo>

#include "linalg.h"

using namespace std;
using namespace arma;


int main(int argc, char *argv[]) {

  int N = atoi(argv[1]);

  double h = 1./N;
  double hh = h*h;
  double a = -1./hh;
  double d = 2./hh;
  cout << analytic_eigenvalues(N+1, a, d);

  jacobi(N+1, a, d, pow(10, -8));

  // double h = 1./N;
  // double hh = h*h;
  // double a = -1./hh;
  // double d = 2./hh;
  // mat A = toeplitz(a, d, N+1);
  // double pi = datum::pi;

  // Time to find eigenvalues with armadillo
  // auto start = std::chrono::high_resolution_clock::now();
  // cx_vec eigval = eig_gen( A );
  // auto finish = std::chrono::high_resolution_clock::now();
  // cout << "Time used armadillo eig_gen: ";
  // cout << std::chrono::duration_cast<std::chrono::milliseconds>(finish - start).count();
  // cout << endl;


  // Print analytical eigenvalues
  // for (int i=1; i<=N+1; i++) {
  //   cout << d + 2*a*cos(i*pi/(N+2)) << endl;
  // }

  // Print armadillo eigenvalues
  // cout << eigval << endl;


  // start = std::chrono::high_resolution_clock::now();
    // Print diagnostics every 1000 steps
    // if (count % 1000 == 0) {
    //   cout << "Count: " << count << endl;
    //   cout << "Max nondiagonal squared: " << max_A*max_A << endl;
    //   cout << "Indexes: " << k << " " << l << endl;
    //   cout << "tau: " << tau << endl;
    //   cout << "tan(theta): " << t << endl;
    //   cout << "cos(theta): " << c << endl;
    //   cout << "sin(theta): " << s << endl << endl;
    // }
  // }
  // finish = std::chrono::high_resolution_clock::now();
  // // chrono::duration<double> elapsed_time = finish-start;
  // cout << "Time used jacobis method: ";
  // cout << std::chrono::duration_cast<std::chrono::milliseconds>(finish - start).count();
  // cout << endl;

  // Print eigenvalues
  // cout << scientific;
  // for (int i=0; i<N+1; i++) {
  //   cout << "eigenvalue " << i << ": " << A(i,i) << endl;
  // }
  //
  // cout << "Transformations performed: " << count << endl;
}
