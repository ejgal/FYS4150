import numpy as np
from numba import jit, njit, prange
from numpy.polynomial.legendre import leggauss
from scipy.special import roots_laguerre


class gQuad(object):
    def __init__(self, leg,lag,legw, lagw):
        self.totalSum = 0
        self.leg, self.legw = leg, legw
        self.lag, self.lagw = lag, lagw
        self.N = leg.shape[0]
    def integrate_legrende(self,a,b):
        totSum = _run_legrende(self.leg,self.legw, a, b, self.N)
        self.totalSum = totSum


    def integrate_laguerre(self):
        totSum = _run_laguerre(self.leg,self.lag, self.legw, self.lagw, self.N)
        self.totalSum = totSum
    
    @property 
    def getResult(self):
        return self.totalSum


    @property
    def error(self):
        analytical = 5*np.pi**2/16**2
        return analytical - self.totalSum 


@njit(parallel=True)
def _run_laguerre(leg,lag,legw,lagw, N):
    x, wga = lag, lagw
    leg, wge = leg, legw
    totalSum = 0
    thetaScalem = np.pi/2
    pScalem = 2*np.pi/2
    for i in prange(N):
        for j in prange(N):
            for k in prange(N):
                for l in prange(N):
                    for m in prange(N):
                        for n in prange(N):
                            r1, t1, phi1 = x[i], thetaScalem*leg[j] + thetaScalem, pScalem*leg[k] +pScalem
                            r2, t2, phi2 = x[l], thetaScalem*leg[m] + thetaScalem, pScalem*leg[n] +pScalem

                            cosbeta = np.cos(t1)*np.cos(t2) + (np.sin(t1)*np.sin(t2)*np.cos(phi1-phi2))
                            func = np.exp(-3*(r1+r2))*r1*r1*r2*r2*np.sin(t1)*np.sin(t2)
                            denom = r1*r1+r2*r2-(2*r1*r2*cosbeta)
                            if denom > 1e-10:
                                weight =  wga[i]*wga[l]*wge[j]*wge[m]*wge[k]*wge[n]
                                func = func/np.sqrt(denom)
                                totalSum += func*weight

    return pScalem**2*thetaScalem**2*totalSum

@njit(parallel=True)
def _run_legrende(leg,legw,a,b, N, alpha=2):
    x = leg
    w = legw
    xl = (b+a)*0.5
    xm = (b-a)*0.5
    totalSum = 0
    for i in prange(N):
        for j in prange(N):
            for k in prange(N):
                for l in prange(N):
                    for m in prange(N):
                        for n in prange(N):
                            x1, y1, z1, x2, y2, z2 = xm*x[i]+xl, xm*x[j]+xl, xm*x[k]+xl, xm*x[l]+xl, xm*x[m]+xl, xm*x[n]+xl
                            exp1 = -2*alpha*np.sqrt(x1*x1+ y1*y1 + z1*z1)
                            exp2 = -2*alpha*np.sqrt(x2*x2+y2*y2+z2*z2)
                            deno = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
                            weight = w[i]*w[j]*w[k]*w[l]*w[m]*w[n]

                            if deno > 10**-10:
                                totalSum += weight*np.exp(exp1+ exp2)/deno

    return totalSum*((b-a)*0.5)**6

if __name__ == "__main__":
    leg, legw = leggauss(31)
    lag, lagw = roots_laguerre(31)
    quad = gQuad(leg,lag, legw,lagw)
    result_leg = quad.integrate_legrende(-2,2)
    result_lag = quad.integrate_laguerre()

    analytical = 5*np.pi**2/16**2
    error_lag = analytical - result_lag
    error_leg = analytical - result_leg

    print('Analytical: {:.5f}'.format(analytical))
    print('Result laguerre: {:.5f}'.format(result_lag))
    print('Result legendre: {:.5f}'.format(result_leg))
    print('Error leguerre: {:.5f}'.format(error_lag))
    print('Error legendre: {:.5f}'.format(error_leg))
