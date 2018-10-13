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
    # Fundemental SI units
    Ampere = Unit('current', 'A')
    Kelvin = Unit('length', 'k')
    Second = Unit('time', 's')
    Meter = Metre = Unit('length', 'm')
    Kilogram = Unit('mass', 'kg')
    Candela = Unit('luminosity', 'cd')
    Mole = Unit('substance', 'mol')
    
    # Derives SI Units
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

    # Conventional SI-accepted units
    
    Gram = Unit(Kilogram / 1000, 'g')
    Centimetre = Unit(Metre * 0.01, 'cm')
    Kilometre = Unit(Metre * 1000, 'km')
    
    Minute = Unit(Second * 60, 'min')
    Hour = Unit(Minute * 60, 'h')
    Day = Unit(Hour * 24, 'd')
    
    Degree = Unit(Radian * math.pi / 180, '°')
    RadialMinute = Unit(Degree / 60, '′')
    RadialSecond = Unit(Degree / 3600, '″')
    
    Acre = Unit(100 * Metre ** 2, 'a')
    Hectare = Unit(100 * Acre, 'ha')
    Litre = Unit((Metre/10)**3, 'L')
    Tonne = Unit(Kilogram * 1000, 't')
    
    # Scientific units
    
    Parsec = Unit(3.0857e16 * Metre, 'pc')
    AU = Unit(1.495_878_707e11 * Metre, 'AU')
    
    u = Dalton = Unit(
        1.660_538_86e-27 * Kilogram, 'u')
    
    # Commonly-used metric variants
    
    Angstrom = Unit(Metre * 1e-10, 'Å')
    Are = Unit((10*Metre)**2, 'a')
    Barn = Unit(1e-28 * Metre **2, 'b')
    
    Bar = Unit(1e5 * Pascal, 'bar')
    Millibar = Unit(100 * Pascal, 'mbar')
    Atmosphere = Unit(101_325 * Pascal, 'atm')
    Torr = Unit(Atmosphere / 760, 'Torr')
    
    MillimetreMercury = mmHg = Unit(
        133.322_387_415 * Pascal, 'mmHg')
        
    Calorie = Unit(4.814 * Joule, 'cal')
    Kilocalorie = Unit(Calorie * 1000, 'kCal')
    
    # Older CGS units
    
    Gal = Centimetre / Second**2
    Dyne = Gram * Gal
    Erg = Dyne * Centimetre
    Barye = Gram / (Centimetre * Second**2)
    Poise = Gram / (Centimetre * Second)
    Stokes = Centimetre**2 / Second
    Kayser = 1 / Centimetre
    
    # Speed
    
    kmph = Kilometre / Hour
    
    NauticalMile = Unit(
        1852 * Meter, 'M', 'NM', 'nmi')
    Knot = Unit(NauticalMile / Hour, 'kt', 'kn')
    
    # Imperial length and area
    
    Inch = Unit(Centimetre * 127/50, 'in')
    Foot = Unit(Inch * 12, 'ft')
    Yard = Unit(3 * Foot, 'yd')
    Chain = Unit(22 * Yard, 'ch')
    Furlong = Unit(10 * Chain, 'fur')
    Mile = Unit(8 * Furlong, 'mi')
    League = Unit(3 * Mile, 'lea')
    
    Link = 7.92 * Inch
    Rod = 25 * Link   
    
    Perch = Rod ** 2
    Rood = Furlong * Rod
    Acre = Furlong * Chain
    
    mph = Mile / Hour
    
    # Imperial volume
    
    FluidOunce = Unit(
        28.4130625 * Litre / 1000, 'fl oz')
    
    Gill = Unit(FluidOunce * 5, 'gi')
    Pint = Unit(Gill * 4, 'pt')
    Quart = Unit(2 * Pint, 'qt')
    Gallon = Unit(4 * Quart, 'gal')
    Peck = 2 * Gallon
    Bushel = 4 * Peck
    
    # Imperial weight
    
    Pound = Unit(453.59237 * Gram, 'lb')
    
    Ounce = Unit(Pound / 16, 'oz')
    Drachm = Unit(Pound / 256, 'dr')
    Grain = Unit(Pound / 7000, 'gr')
    
    Stone = Unit(14 * Pound, 'st')
    Quarter = Unit(2 * Stone, 'qr', 'qtr')
    Hundredweight = Unit(4 * Quarter, 'cwt')
    Ton = Unit(2240 * Pound, 't')
    
    Slug = 14.59390294 * Kilogram

    # Conventional time units
    Week = Day * 7
    Fortnight = Week * 2
    Year = Unit(Day * 365.25, 'yr')
    
    # Unusual units
    
    Hand = 4 * Inch
    Horse = 8 * Foot
    FootballPitch = 105 * 68 * Metre ** 2
    
    Wales = 20799 * Kilometre ** 2
    
    DogYear = Year / 7
    Sol = 88775 * Second
    GalacticYear = 225 * 1e9 * Year
    
    Firkin = 90 * Pound



__all__ = ['Unit', 'exp_mantissa']

for name in dir(Units):
    if '__' in name:
        continue
    globals()[name] = getattr(Units, name)
    __all__.append(name)

for name, exp in prefixes.items():
    __all__.append(name)
    globals()[name] = 10 ** exp
