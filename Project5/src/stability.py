import one_dimension as od
import numpy as np
from test_one_dim import relative_error


# Comparison of FTCS and CTCS
t = 1000
psi, zeta = od.periodic(1/40, t, init=od.sine, advance=od.forward, dt=0.08, filename='long_forward_008')
psi, zeta = od.periodic(1/40, t, init=od.sine, advance=od.forward, dt=0.05, filename='long_forward_005')
t = 3000
psi, zea = od.periodic(1/40, t, init=od.sine, advance=od.centered, dt=1, filename='long_centered')


# Longer runs investigating stability of CTCS

t = 5000
psi, zeta = od.periodic(1/40, t, init=od.sine, advance=od.centered, dt=6.30, filename='long_centered_630')


t = 100000
psi, zeta = od.periodic(1/40, t, init=od.sine, advance=od.centered, dt=6.29, filename='long_centered_629')
psi, zeta = od.periodic(1/40, t, init=od.sine, advance=od.centered, dt=4.0, filename='long_centered_400')
