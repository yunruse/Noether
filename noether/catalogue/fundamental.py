'''
Fundamental SI dimensions and their units.
'''

from noether.core import Dimension, Unit
from .prefixes import SI_all

luminosity = Dimension.new('luminosity', 'J', -7)
current = Dimension.new('current', 'I', -6)
temperature = Dimension.new('temperature', 'Θ', -5)
mass = Dimension.new('mass', 'M', -4)
substance = Dimension.new('substance', 'N', -3)
length = Dimension.new('length', 'L', -2)
time = Dimension.new('time', 'T', -1)

candela = cd = Unit(luminosity, 'candela', 'cd', SI_all)
ampere = A = Unit(current, 'ampere', 'A', SI_all)
kelvin = K = Unit(temperature, 'kelvin', 'K', SI_all)
kilogram = kg = Unit(mass, 'kilogram', 'kg')
mole = mol = Unit(substance, 'mole', 'mol', SI_all)
meter = metre = m = Unit(length, ['meter', 'metre'], 'm', SI_all)
second = s = Unit(time, 'second', 's', SI_all)

__all__ = [
    'luminosity', 'candela', 'cd',
    'current', 'ampere', 'A',
    'temperature', 'kelvin', 'K',
    'mass', 'kilogram', 'kg',
    'substance', 'mole', 'mol',
    'length', 'meter', 'm', 'metre',
    'time', 'second', 's',
]
