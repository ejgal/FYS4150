import numpy as np
from pytest import approx
import analytic as a




def test_z():
    for T in np.linspace(1.,10.,5):
        analytic = a.z(T)
        calculated = 0
        states = a.produce_states()
        for state in states:
            energy = a.energy(state)
            calculated += np.exp(-1/T*energy)
        assert analytic == approx(calculated)


def test_expected_energy():
    "<E>"
    for T in np.linspace(1.,10.,5):
        zt = a.z(T)
        B=1/T
        analytic = a.expected_energy(T)
        states = a.produce_states()
        calculated = 0
        for state in states:
            energy = a.energy(state)
            prob = a.probability(T,state)
            calculated += prob*energy
        assert analytic == approx(calculated)

def test_E2():
    "<E^2>"
    for T in np.linspace(1.,10.,5):
        B = 1/T
        analytic = 256/a.z(T)* np.cosh(8*B)
        states = a.produce_states()
        calculated = 0
        for state in states:
            energy = a.energy(state)
            prob = a.probability(T,state)
            calculated += prob*energy**2
        assert analytic == approx(calculated)


def test_Esquared():
    "<E>^2"
    for T in np.linspace(1.,10.,3):
        B = 1/T
        zt = a.z(T)
        # analytic = (16/a.z(T))**2 *(np.exp(-16*B) + np.exp(16*B) - 2)
        analytic = 32**2/(zt)**2 * np.sinh(8*B)**2
        states = a.produce_states()
        calculated = 0
        for state in states:
            energy = a.energy(state)
            prob = a.probability(T,state)
            calculated += prob*energy
        assert analytic == approx(calculated**2)




def test_M():
    """
    <M>
    """
    for T in np.linspace(1.,10.,5):
        # analytic = a.expected_magnetization(T)
        zt = a.z(T)
        B = 1/T
        analytic = 8/zt * (np.exp(8*B) + 2)
        states = a.produce_states()
        calculated = 0
        for state in states:
            magnetization = a.magnetization(state)
            prob = a.probability(T,state)
            calculated += np.abs(magnetization)*prob
        assert analytic == approx(calculated)


def test_M2():
    """
    <M^2>
    """
    for T in np.linspace(1.,10.,5):
        B = 1/T
        analytic = 32/a.z(T)*(np.exp(8*B) + 1)
        states = a.produce_states()
        calculated = 0
        for state in states:
            magnet = np.abs(a.magnetization(state))
            prob = a.probability(T,state)
            calculated += prob*magnet**2
        assert analytic == approx(calculated)


def test_Msquared():
    """
    <M>^2
    """
    for T in np.linspace(1.,10.,5):
        B = 1/T
        analytic = 64/a.z(T)**2 *(4*np.exp(8*B) + np.exp(16*B) + 4)
        states = a.produce_states()
        calculated = 0
        for state in states:
            magnet = np.abs(a.magnetization(state))
            prob = a.probability(T,state)
            calculated += prob*magnet
        assert analytic == approx(calculated**2)



def test_variance_energy():
    for T in np.linspace(1.,10.,5):
        T = 1.
        B = 1/T
        analytic = a.variance_energy(T)
        states = a.produce_states()
        E2 = 0
        E = 0
        for state in states:
            energy = a.energy(state)
            prob = a.probability(T,state)
            E2 += energy**2*prob
            E +=  energy*prob
        assert analytic == approx(E2 - E**2)

def test_variance_magnetization():
    for T in np.linspace(1.,10.,5):
        analytic = a.variance_magnetization(T)
        states = a.produce_states()
        M2 = 0
        M = 0
        for state in states:
            magnetization = np.abs(a.magnetization(state))
            prob = a.probability(T,state)
            M2 += magnetization**2*prob
            M += magnetization*prob
        assert analytic == approx(M2 - M**2)
