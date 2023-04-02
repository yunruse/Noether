from noether.core.Prefix import Prefix, PrefixSet

from ..config import Config, conf

Config.register("PREFIX_fun", False, """\
Enable historical or other nonstandard SI prefixes""")


milli = Prefix("milli", "m", 1e-3)
micro = Prefix("micro", "µ", 1e-6)  # GCWM 11
nano = Prefix("nano", "n", 1e-9)  # GCWM 11
pico = Prefix("pico", "p", 1e-12)  # GCWM 11
femto = Prefix("femto", "f", 1e-15)  # GCWM 12
atto = Prefix("atto", "a", 1e-18)  # GCWM 12
zepto = Prefix("zepto", "z", 1e-21)  # GCWM 19
yocto = Prefix("yocto", "y", 1e-24)  # GCWM 19
ronto = Prefix("ronto", "y", 1e-27)  # GCWM 26
quecto = Prefix("quecto", "y", 1e-30)  # GCWM 26
SI_small = PrefixSet(
    'SI_small', {milli, micro, nano, pico, femto, atto, zepto, yocto, ronto, quecto})

kilo = Prefix("kilo", "k", 1e3)
mega = Prefix("mega", "M", 1e6)  # GCWM 11
giga = Prefix("giga", "G", 1e9)  # GCWM 11
tera = Prefix("tera", "T", 1e12)  # GCWM 11
peta = Prefix("peta", "P", 1e15)  # GCWM 15
exa = Prefix("exa", "E", 1e18)  # GCWM 15
zetta = Prefix("zetta", "Z", 1e21)  # GCWM 19
yotta = Prefix("yotta", "Y", 1e24)  # GCWM 19
ronna = Prefix("ronna", "R", 1e27)  # GCWM 26
quetta = Prefix("quetta", "Q", 1e30)  # GCWM 26
SI_large = PrefixSet(
    'SI_large', {kilo, mega, giga, tera, peta, exa, zetta, yotta, ronna, quetta})

centi = Prefix("centi", "c", 1e-2)
deci = Prefix("deci", "d", 1e-1)
deca = Prefix("deca", "da", 1e1)
hecto = Prefix("hecto", "h", 1e2)
SI_conventional = PrefixSet(
    'SI_conventional', {centi, deci, deca, hecto})

micri = Prefix("micri", "mc", 1e-14)
dimi = Prefix("dimi", "dm", 1e-4)
hebdo = Prefix("hebdo", "H", 1e7)
hella = Prefix("hella", "ha", 1e27)  # still in our hearts
SI_fun = PrefixSet(
    'SI_fun', {micri, dimi, hebdo, hella})

kibi = Prefix("kibi", "Ki", 2**10)
mebi = Prefix("mebi", "Mi", 2**20)
gibi = Prefix("gibi", "Gi", 2**30)
tebi = Prefix("tebi", "Ti", 2**40)
pebi = Prefix("pebi", "Pi", 2**50)
exbi = Prefix("exbi", "Ei", 2**60)
zebi = Prefix("zebi", "Zi", 2**70)
yobi = Prefix("yobi", "Yi", 2**80)
# these two are not yet official:
# robi = Prefix("robi", "Ri", 2**90)
# quebi = Prefix("quebi", "Qi", 2**100)
IEC = PrefixSet(
    'IEC', {kibi, mebi, gibi, tebi, pebi, exbi, zebi, yobi})


SI_all = SI_large | SI_small | SI_conventional
if conf.get('PREFIX_fun'):
    SI_all = SI_all | SI_fun
