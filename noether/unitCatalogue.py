'''Noether: SI, SI-derived and SI-compatible units'''

from .unit import BaseUnit as U
from math import pi

BU = lambda q, sym: U(1, sym, _dim=q, m=q)

class Catalogue:
    # Fundemental SI units
    Ampere = BU('current', 'A')
    Kelvin = BU('temperature', 'k')
    Second = BU('time', 's')
    Meter = Metre = BU('length', 'm')
    Kilogram = BU('mass', 'kg')
    Candela = BU('luminosity', 'cd')
    Mole = BU('substance', 'mol')
    
    # SI derived units
    
    Hertz = U(1 / Second, 'Hz', m='frequency')
    Radian = U(Metre / Metre, 'rad')
    Steradian = U(Radian**2, 'rad')
    
    Newton = U(
        Kilogram * Metre / Second ** 2,
        'N', m='force')
    Pascal = U(
        Newton / Metre ** 2,
        'Pa', m='pressure')
    Joule = U(
        Newton * Metre,
        'J', m='energy')
    Watt = U(
        Joule / Second,
        'W', m='power')
    Coulomb = U(
        Ampere * Second,
        'C', m='charge')
    Volt = U(
        Watt / Ampere,
        'V', m='voltage')
    Farad = U(
        Coulomb / Volt,
        'F', m='capacitance')
    Ohm = U(
        Volt / Ampere,
        'Ω', m='resistance')
    Siemens = U(
        1 / Ohm,
        'S', m='conductance')
    Weber = U(
        Joule / Ampere,
        'Wb', m='magnetic flux')
    Tesla = U(
        Weber / (Metre ** 2),
        'T', m='magnetic flux density')
    Henry = U(
        Ohm * Second,
        'H', m='inductance')
    
    Lumen = U(
        Candela * Steradian,
        'lm', m='luminous flux')
    Lux = U(Lumen / Metre ** 2, 'lx', m='illuminance')
    Becquerel = U(Hertz, 'Bq')
    Gray = U(Joule / Kilogram, 'Gy', m='dose')
    Sievert = U(Gray, 'Sv')
    Katal = U(
        Mole / Second,
        'kat', m='catalytic activity')
    
    # Unnamed derivative measures
    
    for i, m in enumerate((
        'speed', 'acceleration', 'snap', 'crackle', 'pop'
        ), start=1):
        U(Metre / Second**i, m=m)
    
    del i, m
    
    U(Kilogram * Metre / Second, m='momentum')
    U(Metre**2, m='area')
    U(Metre**3, m='volume')
    
    U(Newton / Metre, 'Nm⁻¹',
         m='surface tension, spring constant')
    
    # Conventional SI-accepted units
    
    Gram = U(Kilogram / 1000, 'g')
    Centimetre = U(Metre * 0.01, 'cm')
    Kilometre = U(Metre * 1000, 'km')
    
    Minute = U(Second * 60, 'min')
    Hour = U(Minute * 60, 'h')
    Day = U(Hour * 24, 'd')
    
    Degree = U(Radian * pi / 180, '°')
    RadialMinute = U(Degree / 60, '′')
    RadialSecond = U(Degree / 3600, '″')
    
    Acre = U(100 * Metre ** 2, 'a')
    Hectare = U(100 * Acre, 'ha')
    Litre = U((Metre/10)**3, 'L')
    Tonne = U(Kilogram * 1000, 't')
    
    # Scientific units
    
    Parsec = U(3.0857e16 * Metre, 'pc')
    AU = U(1.495_878_707e11 * Metre, 'AU')
    
    u = Dalton = U(
        1.660_538_86e-27 * Kilogram, 'u')
    
    # Commonly-used metric variants
    
    Angstrom = U(Metre * 1e-10, 'Å')
    Are = U((10*Metre)**2, 'a')
    Barn = U(1e-28 * Metre **2, 'b')
    
    Bar = U(1e5 * Pascal, 'bar')
    Millibar = U(100 * Pascal, 'mbar')
    Atmosphere = U(101_325 * Pascal, 'atm')
    Torr = U(Atmosphere / 760, 'Torr')
    
    MillimetreMercury = mmHg = U(
        133.322_387_415 * Pascal, 'mmHg')
        
    Calorie = U(4.814 * Joule, 'cal')
    Kilocalorie = U(Calorie * 1000, 'kCal')
    
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
    
    NauticalMile = U(
        1852 * Meter, 'M', 'NM', 'nmi')
    Knot = U(NauticalMile / Hour, 'kt', 'kn')
    
    # Imperial length and area
    
    Inch = U(Centimetre * 127/50, 'in')
    Foot = U(Inch * 12, 'ft')
    Yard = U(3 * Foot, 'yd')
    Chain = U(22 * Yard, 'ch')
    Furlong = U(10 * Chain, 'fur')
    Mile = U(8 * Furlong, 'mi')
    League = U(3 * Mile, 'lea')
    
    Link = 7.92 * Inch
    Rod = 25 * Link   
    
    Perch = Rod ** 2
    Rood = Furlong * Rod
    Acre = Furlong * Chain
    
    mph = Mile / Hour
    
    # Imperial volume
    
    FluidOunce = U(
        28.4130625 * Litre / 1000, 'fl oz')
    
    Gill = U(FluidOunce * 5, 'gi')
    Pint = U(Gill * 4, 'pt')
    Quart = U(2 * Pint, 'qt')
    Gallon = U(4 * Quart, 'gal')
    Peck = 2 * Gallon
    Bushel = 4 * Peck
    
    # Imperial weight
    
    Pound = U(453.59237 * Gram, 'lb')
    
    Ounce = U(Pound / 16, 'oz')
    Drachm = U(Pound / 256, 'dr')
    Grain = U(Pound / 7000, 'gr')
    
    Stone = U(14 * Pound, 'st')
    Quarter = U(2 * Stone, 'qr', 'qtr')
    Hundredweight = U(4 * Quarter, 'cwt')
    Ton = U(2240 * Pound, 't')
    
    Slug = 14.59390294 * Kilogram
    
    # Conventional time units
    Week = Day * 7
    Fortnight = Week * 2
    Year = U(Day * 365.25, 'yr')
    
    # Unusual units
    
    Hand = 4 * Inch
    Horse = 8 * Foot
    FootballPitch = 105 * 68 * Metre ** 2
    
    Wales = 20799 * Kilometre ** 2
    
    DogYear = Year / 7
    Sol = 88775 * Second
    GalacticYear = 225 * 1e9 * Year
    
    Firkin = 90 * Pound
    Smoot = 1.67005 * Metre

__all__ = []
table = []

for name in dir(Catalogue):
    if '__' in name:
        continue
    
    # Append name to symbols
    unit = getattr(Catalogue, name)
    if isinstance(unit, U):
        unit.symbols += (name, )
    else:
        unit = U(unit, name)
    
    globals()[name] = unit
    __all__.append(name)
    
    sym, m = unit._symbolMeasure()
    sNum = unit._numerical()
    m = str(m).replace('None', 'unknown').replace('unitless', '')
    table.append([name, sNum, sym, m])

table.sort(key=lambda q: q[3])
from .helpers import tablify
print('\n'.join(tablify(table)))
