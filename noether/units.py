'''Noether: International System of Units dimensionality object'''

import math
import operator

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

# properties modifiable in repl

precision = 3
showUnits = True
showDimension = True

# used for display
# dimension_dict: (name, unit)
fundamental = {}

class Unit(float):
    __slots__ = 'dim symbols'.split()

    def _measureUnit(self):
        if all(i == 0 for i in self.dim):
            return 'unitless', None
        
        measure, unit = fundamental.get(self.dim, (None, None))
        return measure, unit

    @property
    def measure(self):
        return self._measureUnit()[0]

    @property
    def baseUnit(self):
        return self._measureUnit()[1]

    def isBaseUnit(self):
        return self.baseUnit() == self

    def asFundamentalUnits(self):
        dims = []
        for i, sym in enumerate(dimensions.values()):
            v = self.dim[i]
            if v == 0:
                continue
            elif v != 1:
                sym += str(v).translate(powerify)
            dims.append(sym)
        
        return '·'.join(dims)
    
    def __repr__(self):
        # get scientific notation
        
        exp, man = exp_mantissa(self)
        if 0 < exp < 3:
            # easily naturalised
            num = str(round(self, precision-exp))
            exp = None
        else:
            num = str(round(man, precision))
        
        if exp:
            # unicode exponents
            num += '×10' + str(exp).translate(powerify)
        
        if not showUnits:
            return num

        # get units
        measure, base_unit = self._measureUnit()

        if showDimension and measure:
            measure = ' ({})'.format(measure)
        else:
            measure = ''
        
        if base_unit:
            unit_symbol = base_unit.symbols[0]
        else:
            unit_symbol = self.asFundamentalUnits()
        
        return '{} {}{}'.format(num, unit_symbol, measure)
    
    def __new__(cls, dim, *symbols, _factor=1, measure=None):
        num = dim if isinstance(dim, Unit) else _factor
        
        if isinstance(dim, Unit):
            dim = dim.dim
        elif isinstance(dim, str):
            dim = tuple(int(d == dim) for d in dimensions)

        self = float.__new__(cls, num)
        self.dim = dim
        self.symbols = symbols
        if measure is not None:
            fundamental[self.dim] = (measure, self)

        return self

    # Dimension-changing operators

    def __mul__(self, other, f=float.__mul__, k=1):
        dim = self.dim
        if isinstance(other, Unit):
            dim = tuple(
                self.dim[i] + k * other.dim[i]
                for i in range(len(dimensions)))
        
        return Unit(dim, _factor=f(float(self), float(other)))

    def __truediv__(self, other):
        return self.__mul__(other, float.__truediv__, k=-1)

    def __floordiv__(self, other):
        return self.__mul__(other, float.__floordiv__, k=-1)

    __rmul__ = __mul__

    def __pow__(self, exp):
        factor = float.__pow__(self, exp)
        return Unit(
            tuple(v*exp for v in self.dim),
            _factor=factor)

    def __rtruediv__(self, other):
        factor = float.__truediv__(float(other), float(self))
        return Unit(
            tuple(-v for v in self.dim),
            _factor=factor)

    # Linear operations
    
    __neg__ = lambda s: Unit(s.dim, _factor=-float(self))

    def __cmp(self, other, f):
        if isinstance(other, Unit) and self.dim != other.dim:
            raise ValueError('Inequal units {} and {}.'.format(
                self.asFundamentalUnits(), other.asFundamentalUnits()))

        return f(float(self), float(other))
    
    __eq__ = lambda s, o: s.__cmp(o, operator.eq)
    __ne__ = lambda s, o: s.__cmp(o, operator.ne)
    __lt__ = lambda s, o: s.__cmp(o, operator.lt)
    __le__ = lambda s, o: s.__cmp(o, operator.le)
    __ge__ = lambda s, o: s.__cmp(o, operator.ge)
    __gt__ = lambda s, o: s.__cmp(o, operator.gt)
    
    __add__ = __radd__ = lambda s, o: Unit(s.dim, _factor=s.__cmp(o, operator.add))
    __sub__ = __rsub__ = lambda s, o: Unit(s.dim, _factor=s.__cmp(o, operator.sub))


    
    def __add__(self, other):
        return Unit(self.dim, self.__cmp(other, operator.add))
        
class Units:
    # Fundemental SI units
    Ampere = Unit('current', 'A', measure='current')
    Kelvin = Unit('temperature', 'k', measure='temperature')
    Second = Unit('time', 's', measure='time')
    Meter = Metre = Unit('length', 'm', measure='length')
    Kilogram = Unit('mass', 'kg', measure='mass')
    Candela = Unit('luminosity', 'cd', measure='luminosity')
    Mole = Unit('substance', 'mol', measure='substance')
    
    # Unnamed time derivatives
    for i, m in enumerate((
        'speed', 'acceleration', 'snap', 'crackle', 'pop'
        ), start=1):
        Unit(Metre / Second**i, measure=m)

    Unit(Metre**2, measure='area')
    Unit(Metre**3, measure='volume')
    
    # SI derived units
    
    Hertz = Unit(1 / Second, 'Hz', measure='frequency')
    Radian = Unit(Metre / Metre, 'rad')
    Steradian = Unit(Radian**2, 'rad')

    Newton = Unit(
        Kilogram * Metre / Second ** 2,
        'N', measure='force')
    Pascal = Unit(
        Newton / Metre ** 2,
        'Pa', measure='pressure')

    Joule = Unit(
        Newton * Metre,
        'J', measure='energy')
    Watt = Unit(
        Joule / Second,
        'W', measure='power')

    Coulomb = Unit(
        Ampere * Second,
        'C', measure='charge')
    Volt = Unit(
        Watt / Ampere,
        'V', measure='voltage')
    Farad = Unit(
        Coulomb / Volt,
        'F', measure='capacitance')
    Ohm = Unit(
        Volt / Ampere,
        'Ω', measure='resistance')
    Siemens = Unit(
        1 / Ohm,
'S', measure='conductance')
    Weber = Unit(
        Joule / Ampere,
        'Wb', measure='magnetic flux')
    Tesla = Unit(
        Weber / (Metre ** 2),
        'T', measure='magnetic flux density')
    Henry = Unit(
        Ohm * Second,
        'H', measure='inductance')

    Lumen = Unit(
        Candela * Steradian,
        'lm', measure='luminous flux')
    Lux = Unit(Lumen / Metre ** 2, 'lx', measure='illuminance')
    Becquerel = Unit(Hertz, 'Bq')
    Gray = Unit(Joule / Kilogram, 'Gy', measure='dose')
    Sievert = Unit(Gray, 'Sv')
    Katal = Unit(
        Mole / Second,
        'kat', measure='catalytic activity')

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
