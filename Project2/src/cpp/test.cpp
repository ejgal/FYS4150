#define CATCH_CONFIG_MAIN
#include "catch.hpp"
#include "linalg.h"
#include <armadillo>

using namespace arma;

TEST_CASE("max_nondiagonal returns largest element") {
  int N = 3;
  mat A = mat(N,N); //Fill A with random numbers [0,1]
  A = {{1,2,-7},
      {2,1,3},
      {-7,1,4}};
  // A(0,1) = 5;
  // A(3,2) = -10;
  cout << A;
  unsigned int k=0; unsigned int l=0;
  max_nondiagonal(A, N, k, l);
  REQUIRE( (k == 0 && l == 2) );
}

TEST_CASE("Jacobis method gives analytical eigenvalues") {
  int n = 3;
  double a = -1.;
  double d = 2.;
  double tol = pow(10,-8);
  vec eigval = vec(n);
  vec analytic = sort(analytic_eigenvalues(n, a, d));
  mat A = toeplitz(a,d,n);
  jacobi(n, a, d, A, tol);
  for (int i=0; i<n; i++){
    eigval(i) = A(i,i);
  }
  eigval = sort(eigval);
  REQUIRE( analytic(0) == Approx(eigval(0)));
  REQUIRE( analytic(1) == Approx(eigval(1)));
  REQUIRE( analytic(2) == Approx(eigval(2)));
}


TEST_CASE("Jacobis method == analytic eigenvalues realistic") {
  int n = 150;
  double h = 1./(n+1);
  double hh = h*h;
  double a = -1./hh;
  double d = 2./hh;
  double tol = pow(10,-8);
  vec eigval = vec(n);
  vec analytic = sort(analytic_eigenvalues(n, a, d));
  mat A = toeplitz(a,d,n);
  jacobi(n, a, d, A, tol);
  for( int i=0; i<n; i++){
    eigval(i) = A(i,i);
  }
  eigval = sort(eigval);
  for (int i=0; i<n; i++) {
    REQUIRE( analytic(i) == Approx(eigval(i)).epsilon(tol));
  }


}
