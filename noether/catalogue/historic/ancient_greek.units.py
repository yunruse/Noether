'''
Ancient Greek units.
https://en.wikipedia.org/wiki/Ancient_Greek_units_of_measurement
All units of length are based on an Attic
measurement (pous = 296 mm).
'''

from noether.core import Unit, UnitSet

from ..fundamental import meter

pous = πούς = meter * 0.296
# Ancient greek foot, as defined in Athens (though varying regionally).


daktylos = δάκτυλος = pous / 16
# Ancient Greek; finger.
kondylos = κόνδυλος = daktylos * 2
# Ancient Greek; knuckle.
palaiste = palaistē = παλαιστή = doron = dōron = δῶρον = daktylos * 4
# Ancient Greek; palm.
dichas = διχάς = hemipodion = hēmipodion = ἡμιπόδιον = daktylos * 8
# Ancient Greek; half-foot.
lichas = λιχάς = daktylos * 10
# Ancient Greek; distance from tip of thumb to tip of outstretched index finger.
orthodoron = orthodōron = ὀρθόδωρον = daktylos * 11
# Ancient Greek; width of a straight hand.
spithame = spithamē = σπιθαμή = daktylos * 12
# Ancient Greek; span of all fingers.
pygme = pygmē = πυγμή = daktylos * 18
# Ancient Greek; forearm
pygon = pygōn = πυγών = daktylos * 20
# Ancient Greek; elbow to fist
pechys = pēchys = πῆχυς = daktylos * 24
# Ancient Greek; cubit (elbow to tip of hand)

haploun_bema = haploun_bēma = ἁπλοῦν_βῆμα = pous * 2.5
# Ancient Greek; step
diploun_bema = diploun_bēma = διπλοῦν_βῆμα = bema = bēma = βῆμα = pous * 5
# Ancient Greek; pace
orgyia = ὄργυια = pous * 6
# Ancient Greek; fathom
kalamos = κάλαμος = akaina = ἄκαινα = dekapous = δεκάπους = pous * 10
# Ancient Greek
hamma = ἅμμα = pous * 60
# Ancient Greek; knot
plethron = πλέθρον = pous * 100
# Ancient Greek; typical length of an athletic running-track
stadion = στάδιον = pous * 600
# Ancient Greek; one eighth of a Roman mile

diaulos = δίαυλος = stadion * 2
# Ancient Greek; ancient Olympic racing distance
hippikon = ἱππικόν = stadion * 4
# Ancient Greek; length of a hippodrome (horse racing stadium)
milion = μίλιον = stadion * 8
# Ancient Greek equiv. of a mile
dolichos = δόλιχος = stadion * 12
# Ancient Greek; ancient Olympic "long race"
parasanges = παρασάγγης = stadion * 30
# Ancient Greek equiv. of a league; used to measure walking distance
schoinos = σχοινός = stadion * 40
# Ancient Greek, adopted from an Egyptian unit of surveying with knotted cords
stage = stadion * 160
# Ancient Greek
