'''
Natural unit systems of all kinds.
Includes Planck systems, both Gaussian and Lorentz-Heaviside.
'''

from math import pi
from .si import radian
from .scientific import c
from .constants import hbar, G, k_B, e_0

__all__ = ("planck", "planck_g", "planck_lh")

l_P = (hbar * G   / c**3         )**0.5
m_P = (hbar / G   * c            )**0.5
t_P = (hbar * G   / c**5         )**0.5
q_P = (hbar       * c    * e_0   )**0.5
T_P = (hbar / G   * c**5 / k_B**2)**0.5

class _planck:
    # TODO: change this to a UnitSystem
    # eg display(natural(c=1, G=1, e_0=1))
    def __new__(self):
        raise ValueError("Planck unit is a namespace, not a class.")

def _new_planck(factor, name, desc):
    class planck(_planck):
        description = desc
        # TODO: other natural units..?
        length      = l_P * factor
        mass        = m_P / factor
        time        = t_P * factor
        charge      = q_P * factor
        temperature = T_P / factor

        area = length ** 2
        volume = length **3
        speed = length / time
        acceleration = speed / time
        momentum = mass * speed
        energy = mass * speed**2
        force = momentum / time
        power = energy / time
        density = mass / volume
        energy_density = energy / volume
        intensity = power / area
        angular_frequency = radian / time
        pressure = force / area
        current = charge / time
        voltage = energy / charge
        resistance = voltage / current
        induction = force / length / current
        inductance = energy / current
        flow = volume / time
        viscosity = pressure * time

    planck.__name__ = planck.__qualname__ = name
    return planck

RP = (4*pi) ** 0.5
planck = planck_g = _new_planck(1, 'planck_g', 'Gaussian')
planck_lh = _new_planck(RP, 'planck_lh', 'Lorentz-Heaviside')
