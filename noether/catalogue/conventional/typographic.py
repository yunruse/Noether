'''
Typographic (imperial) units.
'''

from noether.core import Unit

from .avourdupois import inch

pica = Unit(inch / 6, "pica")  # as defined by PostScript
cicero = Unit(inch / 6, "cicero")

pica_american = Unit(inch * 400/2409, "pica_american")  # as used in TeX
pica_french = Unit(inch * 0.1776, "pica_french")
point = Unit(inch / 72, "point", "pt")  # DTP point - this one varies a lot!

agate = ruby = Unit(point * 5.5, "agate", "ruby")

em = Unit(point, "em")
en = Unit(em / 2, "en")

#  TODO: add an repr-info-hook thing which tells you point names
# https://en.wikipedia.org/wiki/Traditional_point-size_names#Comparison_table
