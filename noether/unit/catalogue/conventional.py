"""Conventional SI-compatible units."""

from math import pi
from .fundamental import (
    U, kilogram, metre, second, ampere
)
from .si import hertz, radian, steradian, watt

# # Conventional units

minute = U(second * 60, "min")
hour = U(minute * 60, "h")
day = U(hour * 24, "d")
week = day * 7
fortnight = week * 2
year = U(day * 365.25, "yr")

cm = metre / 100
kmph = metre * 1000 / hour

acre = U(100 * metre**2, "a")
hectare = U(100 * acre, "ha")
litre = U((metre / 10)**3, "l", SI=True)

gram = U(kilogram / 1000, "g", SI=True)
tonne = ton = U(kilogram * 1000, "t", SI=True)

bpm = U(hertz / 60, "bpm")

# # Angles

degree = U(radian * pi / 180, "°")
angular_minute = U(degree / 60, "′")
angular_second = U(degree / 3600, "″")
gradian = U(radian * pi / 200, "gon")

circle = turn = U(radian * 2*pi, "turn")
sphere = spat = U(steradian * 4*pi, "sp")

deg = degree
rad = radian
grad = gradian
sterad = steradian

# # Electricity

watt_hour = U(watt * hour, 'Wh', SI=True)
amp_hour = ampere_hour = U(ampere * hour, 'Ah', SI=True)
