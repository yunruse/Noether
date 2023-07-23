'''
The Potrzebie System of Weights and Measures, as defined by Donald Knuth.

https://webmadness.net/resources/The-Potrzebie-system-of-weights-and-measures.pdf
'''

from noether.core import Unit, UnitSet

from ..fundamental import second, meter
from ..scientific import minute, turn, gram
from ..conventional import inch
from ..scientific import angstrom

P = POTRZEBIE = UnitSet()
# POTRZEBIE_PREFIXES =

potrzebie = Unit(
    meter * 2.263347539605392, "potrzebie",
    info="The thickness of Mad issue 26, as measured by Donald Knuth.")
ngogn = Unit(potrzebie**3 * 100, "ngogn")
blintz = Unit(gram * 36.42538631, "blintz")

zygo = Unit(turn / 100, "zygo")
zorch = Unit(zygo / 100, "zorch", '’’’')
quircit = Unit(zorch / 100, "quircit", '’’’’')
P(turn & zygo & zorch & quircit)

# TODO: remaining units
