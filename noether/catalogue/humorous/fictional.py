'''
A variety of fictional units.
Only distinctly defined units are provided.

Sourced from various fan wikis and TV Tropes.
'''

from noether.core import Unit, UnitSet
from ..fundamental import second
from ..conventional import day, year, minute
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

TOLKIEN = UnitSet({yén & enquië & ré, lár & ranga})


# % Homestuck
solar_sweep = alternian_year = Unit(
    year * 13/6, ["solar_sweep", "alternian_year"], info="i h8 that i felt obliged to add this unit ::(")


# % Dragonball
takk = Unit(minute * 0.48, "takk")

# % Superman
thrib = Unit(second, "thrib")
dendar = Unit(thrib * 100, "dendar")
wolu = Unit(thrib * 10_000, "wolu")
zetyar = Unit(wolu * 10, "zetyar")
lorax = Unit(zetyar * 73, "lorax")
kryptonian_year = Unit(lorax * 6, "kryptonian_year")

chronon = knorrian_hour = Unit(minute * 40, ["chronon", "knorrian_hour"])

# % Transformers
breem = Unit(minute * 8.3, "breem")
vorn = Unit(year * 83, "vorn")
astrosecond = Unit(breem / 1000, "astrosecond")
# TODO: https://tfwiki.net/wiki/Category:Measurements


# TODO: Like, every other fictional unit
# https://tvtropes.org/pmwiki/pmwiki.php/Main/Microts
# https://tvtropes.org/pmwiki/pmwiki.php/Main/FantasticMeasurementSystem
