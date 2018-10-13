'''Noether: International System of Units dimensionality object'''

import math

prefixes = dict(
    y=-24, z=-21, a=-18, f=-15, p=-12, n=-9, μ=-6, m=-3,
    k=3, M=6, G=9, T=12, P=15, E=18, Z=21, Y=24
)

def exp_mantissa(num, base=10):
    exp = math.floor(math.log(num, base))
    mantissa = num / (10 ** exp)
    return exp, mantissa

def prefixify(num):
    '''Returns a number and SI-prefix if it fits.'''
    if not isinstance(num, (float, int)):
        return num, ''
    exp, mantissa = exp_mantissa(num, 10)        
    for prefix, pexp in prefixes.items():
        dexp = exp - pexp
        if -2 < dexp < 3:
            return mantissa * 10**dexp, prefix

    return num, ''


dimensions = {
    'length': 'm',
    'time': 's',
    'current': 'A',
    'temperature': 'K',
    'mass': 'Kg',
    'luminosity': 'Cd',
    'substance': 'mol'
}

powerify = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')

_default_dim = {i: 0 for i in dimensions}

precision = 3

class Unit:    
    __slots__ = 'factor dim symbols'.split()
    def __repr__(self):
        dims = [
            dimensions[i] + str(v).translate(powerify)*(v!=1)
            for i, v in self.dim.items()
            if v != 0]
        exp, man = exp_mantissa(self.factor)
        num = str(round(man, precision))
        if exp:
            num += '×10' + str(exp).translate(powerify)
        return '{} {}'.format(num, '·'.join(dims))

    def __float__(self):
        return float(self.factor)

    def __int__(self):
        return int(self.factor)

    @property
    def imag(self):
        return 0

    @property
    def real(self):
        return float(self)
    
    def isBaseUnit(self):
        return self.factor == 1
    
    def __init__(self, dim, *symbols, _factor=1):
        if isinstance(dim, Unit):
            self.dim = dim.dim
            self.factor = dim.factor
        else:
            if isinstance(dim, str):
                dim = {**_default_dim, dim: 1}
            self.dim = dim
            self.factor = _factor

        self.symbols = symbols

    # Dimension-changing operators

    def __mul__(self, other):
        if isinstance(other, Unit):
            return Unit(
                {i: self.dim[i] + other.dim[i] for i in self.dim},
                _factor=self.factor*other.factor)
        else:
            return Unit(
                self.dim,
                _factor=self.factor*other)

    def __rmul__(self, other):
        return self * other

    def __pow__(self, exp):
        return Unit(
            {i: v*exp for i, v in self.dim.items()},
            _factor=self.factor**exp)

    def __truediv__(self, other):
        if isinstance(other, Unit):
            return Unit(
                {i: self.dim[i] - other.dim[i] for i in self.dim},
                _factor=self.factor/other.factor)
        else:
            return Unit(
                self.dim, _factor=self.factor/other)

    def __rtruediv__(self, other):
        return Unit(
            {i: -v for i, v in self.dim.items()},
            _factor=other/self.factor)

    def __neg__(self):
        return Unit(self.dim, _factor=-self.factor)

    def __add__(self, other):
        if isinstance(other, Unit):
            if other.dim != self.dim:
                raise ValueError('Inequal units!')
            return Unit(self.dim, _factor=self.factor+other.factor)
        else:
            return Unit(self.dim, _factor=self.factor+other)

    __radd__ = __add__

    def __sub__(self, other):
        return self + -other

    __rsub__ = __sub__
        
class Units:
    Ampere = Unit('current', 'A')
    Kelvin = Unit('length', 'k')
    Second = Unit('time', 's')
    Meter = Metre = Unit('length', 'm')
    Kilogram = Unit('mass', 'kg')
    Candela = Unit('luminosity', 'cd')
    Mole = Unit('substance', 'mol')

    Hertz = Unit(1 / Second, 'Hz')

    Radian = Unit(Metre / Metre, 'rad')
    Steradian = Unit(Metre*Metre / Metre*Metre, 'rad')

    Newton = Unit(Kilogram * Metre / Second ** 2, 'N')
    Pascal = Unit(Newton / Metre ** 2, 'Pa')

    Joule = Unit(Newton * Metre, 'J')
    Watt = Unit(Joule / Second, 'W')

    Coulomb = Unit(Ampere * Second, 'C')
    Volt = Unit(Watt / Ampere, 'V')
    Farad = Unit(Coulomb / Volt, 'F')
    Ohm = Unit(Volt / Ampere, 'Ω')
    Siemens = Unit(1 / Ohm, 'S')
    Weber = Unit(Joule / Ampere, 'Wb')
    Tesla = Unit(Weber / (Metre ** 2), 'T')
    Henry = Unit(Ohm * Second, 'H')

    Lumen = Unit(Candela * Steradian, 'lm')
    Lux = Unit(Lumen / Metre ** 2, 'lx')
    Becquerel = Unit(Hertz, 'Bq')
    Gray = Unit(Joule / Kilogram, 'Gy')
    Sievert = Unit(Gray, 'Sv')
    Katal = Unit(Mole / Second, 'kat')

    Centimetre = Unit(Metre * 0.01, 'cm')
    Inch = Unit(Centimetre * 127/50, 'in')
    Foot = Unit(Metre * 371/1250, 'ft')

    Minute = Unit(Second * 60, 'min')
    Hour = Unit(Minute * 60, 'h')
    Day = Unit(Hour * 24, 'day')



__all__ = ['Unit', 'exp_mantissa']

for name in dir(Units):
    if '__' in name:
        continue
    globals()[name] = getattr(Units, name)
    __all__.append(name)

for name, exp in prefixes.items():
    __all__.append(name)
    globals()[name] = 10 ** exp
