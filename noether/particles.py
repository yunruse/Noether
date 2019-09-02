from dataclasses import dataclass, field
import fractions

from .unit import Measure
from .unitCatalogue import coulomb
from .constants import e, m_e, MeVc2

I = fractions.Fraction(1)

__all__ = 'Particle u d s c t b e p n'.split()

@dataclass
class Particle:
    symbols: list = field(default_factory=list)
    mass: Measure = 0 * MeVc2
    charge: Measure = 0 * coulomb

    angular_momentum: float = 0
    baryon: float = 0
    isospin: float = 0

    charm: float = 0
    strangeness: float = 0
    beauty: float = 0
    truth: float = 0

    conserved = "mass charge baryon charm strangeness truth beauty".split()

    # Particle compositions ASSUME strong interaction.
    # Naturally quark flavour can change via the weak.

    def __add__(self, other):
        return Particle(
            **{i: getattr(self, i) + getattr(other, i) for i in self.conserved}
        )

    def __sub__(self, other):
        return Particle(
            **{i: getattr(self, i) - getattr(other, i) for i in self.conserved}
        )

    @classmethod
    def using(cls, particle, **kwargs):
        d = {i: getattr(particle, i) for i in cls.conserved}
        d.update(kwargs)
        return Particle(**d)

# Quarks

_b = dict(angular_momentum=I / 2, baryon=I / 3)

up      = u = Particle(**_b, mass=2.3     * MeVc2, charge=+e*2/3, isospin=+I/2)
down    = d = Particle(**_b, mass=4.8     * MeVc2, charge=-e*1/3, isospin=-I/2)

charm   = c = Particle(**_b, mass=1275    * MeVc2, charge=+e*2/3, charm=1)
strange = s = Particle(**_b, mass=95      * MeVc2, charge=-e*1/3, strangeness=-1)

top     = t = Particle(**_b, mass=173_210 * MeVc2, charge=+e*2/3, truth=1)
bottom  = b = Particle(**_b, mass=4180    * MeVc2, charge=-e*1/3, beauty=-1)

# Baryons currently discovered

p = proton  = Particle.using(u + u + d, mass=938.272_046 * MeVc2)

n = neutron = Particle.using(u + d + d, mass=939.565_379 * MeVc2)

lambda_0 = Particle.using(u + d + s, mass=1115.683 * MeVc2)

# Leptons

e = electron = Particle(symbols=["e"], mass=m_e, charge=-e)
