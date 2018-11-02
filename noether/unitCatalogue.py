'''Noether: SI, SI-derived and SI-compatible units'''

from .unit import *

class Catalogue:
    # Fundemental SI units
    Ampere = Unit('current', 'A', measure='current')
    Kelvin = Unit('temperature', 'k', measure='temperature')
    Second = Unit('time', 's', measure='time')
    Meter = Metre = Unit('length', 'm', measure='length')
    Kilogram = Unit('mass', 'kg', measure='mass')
    Candela = Unit('luminosity', 'cd', measure='luminosity')
    Mole = Unit('substance', 'mol', measure='substance')
    
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
    
    # Unnamed derivative measures
    
    for i, m in enumerate((
        'speed', 'acceleration', 'snap', 'crackle', 'pop'
        ), start=1):
        Unit(Metre / Second**i, measure=m)
    
    Unit(Kilogram * Metre / Second, measure='momentum')
    Unit(Metre**2, measure='area')
    Unit(Metre**3, measure='volume')
    
    Unit(Newton / Metre, 'Nm⁻¹',
         measure='surface tension, spring constant')
    
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
    Smoot = 1.67005 * Metre

__all__ = []

for name in dir(Catalogue):
    if '__' in name:
        continue
    globals()[name] = getattr(Catalogue, name)
    __all__.append(name)
