#define CATCH_CONFIG_MAIN
#include "catch.hpp"
#include "linalg.h"
#include <armadillo>

using namespace arma;

TEST_CASE("max_nondiagonal returns largest element") {
  int N = 4;
  mat A = mat(N,N, fill::randu); //Fill A with random numbers [0,1]
  A(0,1) = 5;
  A(3,2) = -10;
  int k=0; int l=0;
  max_nondiagonal(A, N, k, l);
  REQUIRE( (k == 3 && l == 2) );
}



// TEST_CASE("Jacobis method compare with analytical eigenvalues") {
//
//   vec analytic = analytic_eigenvalues(3, -1, 2);
//   cout << analytic;
//
//   REQUIRE();
//   REQUIRE();
//   REQUIRE();
// }
