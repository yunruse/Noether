'''
Fictional units.
Only distinctly defined units are provided.
'''

from noether.core import Unit, UnitSet
from ..conventional import day
from ..conventional import inch

# % Tolkien (taken from appendices)
# LOTR: The Calendars
ré = Unit(day, "ré", info="Quenya. Elvish day. Reckoned from sunset to sunset.")
enquie = enquië = Unit(
    ré * 6, "enquië",
    info="Quenya. Elvish week. It was said that Elvish loved sixes and twelves.")
yen = yén = Unit(
    enquië * 1461 * 6, "yén",
    info="Quenya. Elvish year.")

stewards_month = Unit(
    ré * 30, "stewards_month",
    info="After Númenórean calendars' year length problems, stewards of Gondor fixed"
    " the month to 30 days. This Westron reckoning is used by all in Tolkien.")
# Only in the Shire did they fix weekdays to the months, gaining a cool idiom
# (friday the 1st - a day which never occurs) and saving on confusion. Go hobbits!

# Gladden Fields (Unfinished Tales): Númenórean Linear Measures
ranga = Unit(
    inch * 38, "ranga",
    info="Númenórean 'full pace' (pl. rangar)"
    " said to be half the height of a man (whence 'halfling').")
lar = lár = daur = Unit(
    ranga * 5000, "lár",
    info="Númenórean 'pause' (Sindarin: daur, translated as 'league')"
    " said to be 5000 paces, after which marchers would briefly halt.")

TOLKIEN = UnitSet(yén & enquië & ré, lár & ranga)
