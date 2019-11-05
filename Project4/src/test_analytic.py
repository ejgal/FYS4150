import numpy as np
from pytest import approx
import analytic as a


def test_z():
    T = 1
    analytic = a.z(T)
    calculated = 0
    states = a.produce_states()
    for state in states:
        energy = a.energy(state)
        calculated += np.exp(-1/T*energy)
    assert analytic == approx(calculated)

def test_expected_energy():
    T = 1
    analytic = a.expected_energy(T)
    states = a.produce_states()
    calculated = 0
    for state in states:
        energy = a.energy(state)
        prob = a.probability(T,state)
        calculated += prob*energy
    assert analytic == approx(calculated)

def test_expected_magnetization():
    T = 1
    analytic = a.expected_magnetization(T)
    states = a.produce_states()
    calculated = 0
    for state in states:
        magnetization = a.magnetization(state)
        prob = a.probability(T,state)
        calculated += np.abs(magnetization)*prob
    assert analytic == approx(calculated)


def test_variance_energy():
    T = 1
    analytic = a.variance_energy(T)
    states = a.produce_states()
    calculated = 0
    for state in states:
        energy = a.energy(state)
        prob = a.probability(T,state)
        calculated += energy**2*prob - (energy*prob)**2
    assert analytic == approx(calculated)

def test_variance_magnetization():
    T = 1
    analytic = a.variance_magnetization(T)
    states = a.produce_states()
    calculated = 0
    for state in states:
        magnetization = a.magnetization(state)
        prob = a.probability(T,state)
        calculated += magnetization**2*prob - (magnetization*prob)**2
    assert analytic == approx(calculated)
