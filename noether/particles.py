'''
A category of fundamental and other subatomic particles.

Tanabashi et al, 2019. https://doi.org/10.1103/physrevd.98.030001

'''

from dataclasses import dataclass, field
from fractions import Fraction

from .unit.measure import Measure
from .unit.catalogue import mass, charge, dalton, MeVc2, e as Q

MeV = MeVc2
eV = MeVc2 / 1e6
GeV = MeV * 1e3

I = Fraction(1)

__all__ = ('Particle', )

@dataclass
class _particle:
    symbols: list = field(default_factory=list)
    mass:   mass   = 0 * MeV
    charge: charge = 0 * Q
    spin:    Fraction = 0
    isospin: Fraction = 0
    baryon:  Fraction = 0
    lepton:  Fraction = 0
    charm:       int = 0
    strangeness: int = 0
    beauty:      int = 0
    truth:       int = 0
    _additive = "charge baryon lepton charm strangeness truth beauty".split()
    _conserved = _additive + "mass".split()

class Particle(_particle):
    '''
    A particle.
    Note that a - b indicates removing b from a,
    whereas a + -b indicates adding an antiparticle.
    '''
    def __init__(self, particle=None, **kwargs):
        _particle.__init__(self)
        if particle:
            for name in self.__dataclass_fields__:
                setattr(self, name, getattr(particle, name))
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __neg__(s): return Particle(
        mass=s.mass, **{i: -getattr(s, i) for i in s._additive})

    def __add__(s, o, f=+1): return Particle(
        **{i: getattr(s, i) + f*getattr(o, i) for i in s._conserved})
    def __sub__(s, o): return s.__add__(o, -1)

class Fermion(Particle): pass
class Hadron(Particle): pass
class Boson(Particle): pass

class Quark(Fermion):
    spin = I / 2
    baryon = I / 3

up      = u = Quark(mass=MeV(    2.16, 0.49), charge=+Q*2/3, isospin=+I/2)
down    = d = Quark(mass=MeV(    4.67, 4.88), charge=-Q*1/3, isospin=-I/2)
charm   = c = Quark(mass=MeV(    1270,   20), charge=+Q*2/3, charm=1)
strange = s = Quark(mass=MeV(      93,   11), charge=-Q*1/3, strangeness=-1)
top     = t = Quark(mass=MeV(172_900, 4_000), charge=+Q*2/3, truth=1)
bottom  = b = Quark(mass=MeV(  4_180,    30), charge=-Q*1/3, beauty=-1)


class Baryon(Hadron, Fermion):
    spin = I / 2

proton     = p   = Baryon(u + u + d, mass=dalton(   1.00727646688, 0.00000000009))
neutron    = n   = Baryon(u + d + d, mass=MeV( 939.565413,      0.000006))
# strange
lambda_0   = λ0  = Baryon(u + d + s, mass=MeV(1115.683, 0.006))
sigma_p    = Σp  = Baryon(u + u + s, mass=MeV(1189.37,  0.07))
sigma_0    = Σ0  = Baryon(u + d + s, mass=MeV(1192.642, 0.024))
sigma_m    = Σm  = Baryon(d + d + s, mass=MeV(1197.449, 0.03))
xi_0       = Ξ0  = Baryon(u + s + s, mass=MeV(1314.86,  0.2))
xi_m       = Ξm  = Baryon(d + s + s, mass=MeV(1321.71,  0.07))
omega_m    = Ωm  = Baryon(s + s + s, mass=MeV(1672.45,  0.29), spin=3/2)
# charm
lambda_p_c = λpc = Baryon(u + d + c, mass=MeV(2286.46,  0.14))
xi_p_c     = Ξpc = Baryon(u + s + c, mass=MeV(2467.93,  0.18))
xi_0_c     = Ξ0c = Baryon(d + s + c, mass=MeV(2470.91,  0.25))
omega_0_c  = Ω0c = Baryon(s + s + c, mass=MeV(2695.2,   1.7))
# exotic
xi_pp      = Ξpp = Baryon(u + c + c, mass=MeV(3621.2,   0.7))
lambda_0_b = λ0b = Baryon(u + d + b, mass=MeV(5619.6,   0.17))
sigma_p_b  = Σpb = Baryon(u + u + b, mass=MeV(5810.56,  0.25))
sigma_0_b  = Σ0b = Baryon(u + d + b, mass=None)
sigma_m_b  = Σmb = Baryon(d + d + b, mass=MeV(5815.64,  0.27))
sigma_p_t  = Σpt = Baryon(u + u + t, mass=None)
sigma_0_t  = Σ0t = Baryon(u + d + t, mass=None)
sigma_m_t  = Σmt = Baryon(d + d + t, mass=None)

class Meson(Boson, Hadron):
    spin = 0

pion_p = πp = Meson(u + -d, mass=MeV(139.57061, 0.00024))
pion_0 = π0 = Meson(u + -u, mass=MeV(134.9770,  0.0005))
pion_m = πm = -pion_p

class Lepton(Particle):
    spin = I/2
class ChargedLepton(Lepton):
    charge = -Q

electron = e = ChargedLepton(mass=MeV(   0.4109989461, 0.0000000031))
muon     = μ = ChargedLepton(mass=MeV( 105.6583745,    0.0000024))
tau      = τ = ChargedLepton(mass=MeV(1776.86,         0.12))

class neutrino(Lepton):
    charge = 0
    lepton = -1

electron_neutrino = ν_e = neutrino(mass=MeV(0,   0.000002))
muon_neutrino     = ν_μ = neutrino(mass=MeV(0,   0.19))
tau_neutrino      = ν_τ = neutrino(mass=MeV(0, 18.2))

class Boson(Particle):
    pass

photon      = H_0 = Boson(mass= eV(0,       1e-18 ), spin=1)
gluon       = g   = Boson(mass=MeV(0,       20    ), spin=1)
w_boson_p   = w_p = Boson(mass=GeV(80.379,  0.012 ), spin=1, charge=-Q)
w_boson_m   = w_m = -w_p
z_boson     = Z   = Boson(mass=GeV(91.1876, 0.0021), spin=1)
higgs_boson = H_0 = Boson(mass=GeV(125_100, 140   ), spin=0)

for name, particle in dict(globals()).items():
    if isinstance(particle, Particle):
        particle.symbols.append(name)
        if not name.startswith('_') and len(name) > 1:
            __all__ += (name, )
