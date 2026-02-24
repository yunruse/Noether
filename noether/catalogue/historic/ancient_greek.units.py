'''
Ancient Greek units
https://en.wikipedia.org/wiki/Ancient_Greek_units_of_measurement
All units of length are based on an Attic
measurement (pous = 296 mm)
'''

from noether.core import Unit, UnitSet

from ..fundamental import meter

#% ancient_greek "Ancient Greek"

pous = πούς = meter * 0.296
# foot as defined in Athens (though varying regionally)


daktylos = δάκτυλος = pous / 16
# finger
kondylos = κόνδυλος = daktylos * 2
# knuckle
palaiste = palaistē = παλαιστή = doron = dōron = δῶρον = daktylos * 4
# palm
dichas = διχάς = hemipodion = hēmipodion = ἡμιπόδιον = daktylos * 8
# half-foot
lichas = λιχάς = daktylos * 10
# distance from tip of thumb to tip of outstretched index finger
orthodoron = orthodōron = ὀρθόδωρον = daktylos * 11
# width of a straight hand
spithame = spithamē = σπιθαμή = daktylos * 12
# span of all fingers
pygme = pygmē = πυγμή = daktylos * 18
# forearm
pygon = pygōn = πυγών = daktylos * 20
# elbow to fist
pechys = pēchys = πῆχυς = daktylos * 24
# cubit (elbow to tip of hand)

haploun_bema = haploun_bēma = ἁπλοῦν_βῆμα = pous * 2.5
# step
diploun_bema = diploun_bēma = διπλοῦν_βῆμα = bema = bēma = βῆμα = pous * 5
# pace
orgyia = ὄργυια = pous * 6
# fathom
kalamos = κάλαμος = akaina = ἄκαινα = dekapous = δεκάπους = pous * 10
hamma = ἅμμα = pous * 60
# knot
plethron = πλέθρον = pous * 100
# typical length of an athletic running-track
stadion = στάδιον = pous * 600
# one eighth of a Roman mile

diaulos = δίαυλος = stadion * 2
# ancient Olympic racing distance
hippikon = ἱππικόν = stadion * 4
# length of a hippodrome (horse racing stadium)
milion = μίλιον = stadion * 8
# Ancient Greek equiv. of a mile
dolichos = δόλιχος = stadion * 12
# ancient Olympic "long race"
parasanges = παρασάγγης = stadion * 30
# league; used to measure walking distance
schoinos = σχοινός = stadion * 40
# adopted from an Egyptian unit of surveying with knotted cords
stage = stadion * 160
