## Abstracts

### Project 1 - Increasing accuracy and speed in numerical solutions of differential equations

This work demonstrates the necessity of understanding the problem before
hand when doing numerical problem solving, and the consequence of right
away opting for a brute force a solution. To demonstrate we solved the one di-
mensional Poisson’s equation using tree different algorithms , LU-decomposition,
the general tridiagonal matrix algorithm (TDMA) or the Thomas algorithm [1]
and a specialized TDMA. We used the LU-decomposition algorithm to illus-
trate a brute force solution. From understanding our problem before hand, we
developed a specialized TDMA for our problem. The specialized TDMA was
about 80000 times faster compared to the general LU-decomposition. For large
matrices the general LU-decomposition also faced memory constraints. Our
specialized TDMA also showed an increase of around 2.2 in performance com-
pared to the general TDMA.

### Project 2 - Evaluating the performance of high-level approaches to speeding up slow code

We investigate high-level approaches to increasing the speed of python code us-
ing Numba and Cython, using an implementation of Jacobis method for finding
eigenvalues as a benchmark. The results are also compared to an c++ imple-
mentation using armadillo. We show that python code containing heavy use
of loops can gain a considerable speed up by using Numba and Cython, with
Numba requiring the least amount of effort.

### Project 3 - Solving multidimensional integrals using Monte Carlo Integration

This work aims to evaluate Monte Carlo Integration (MCI) for solving physical
problems with many degrees of freedom. The physical problem in question is
the ground state correlation energy between two electrons in a helium atom,
which we solved using four different approaches, "brute force" MCI, MCI with
importance sampling, Gaussian Quadrature (GQ) with Legendre polynomials
and GQ combining Legendre- and Laguerre polynomials. We also parallelized
the code. We did an extensive analysis of the error, CPU time and scalability of
the different approaches. The result of our analysis showed that we achieved
a close to optimal speed up for MCI with importance sampling. For run times
larger than 10 seconds MCI with importance sampling had an error that was
between 10 and 383 times smaller than the GQ Laguerre. Importance sampling
MCI had also on average 57 times lower error compared to brute force MCI.

### Project 4 - Investigation of phase transitions in magnetic systems using the Ising Model

The Ising model is one of the most studied models in statistical mechanics. In
this work we look at a classic application of the Ising model, namely the study
of phase transitions in magnetic systems. We implement a stochastic Monte
Carlo model of the Ising model following the Metropolis algorithm. We ran
our model for several temperatures and grid sizes and calculated the critical
temperature for each grid. Then we use a simple linear regression model to fit a
line to the previously calculated critical temperatures. From the regression line
we estimate the critical temperature for an infinite grid. Our result of T C ( L =
∞ ) = 2.2687 are close to the analytical result of Lars Onsager (Onsager 1944)
with a relative error of 2.00 × 10^4 .

### Project 5  - Study of Barotropic Rossby waves, using finite difference methods

This work investigates solutions of the barotropic Rossby wave equation (BRWE)
in a closed and periodic domain, using finite difference methods. First we de-
rived the BRWE by linearising the barotropic vorticity equation and then we
scaled this linearised equation to obtain dimensionless analytical values for the
phase speed in one dimension c periodic = − 0.0063, c closed = − 0.012665, both
with sinusoidal initial states. Next we developed an algorithm for solving the
BRWE, which we implemented using both forward time centered space (FTCS)
and centered time centered space (CTCS) schemes. For both versions we did an
extensive stability analysis and found FTCS to be unconditionally unstable for
all combination of ∆x, ∆t. CTCS was found to be stable for ∆x/∆t < k 2 . Using
the CTCS version we obtained c periodic = − 0.00625 and c closed = − 0.0125 which
is in good agreement with the analytical results.
