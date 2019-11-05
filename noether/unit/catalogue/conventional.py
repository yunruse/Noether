"""Conventional SI-compatible units."""

from math import pi
from .fundamental import (
    U, kilogram, metre, second, ampere
)
from .si import hertz, radian, watt

gram = U(kilogram / 1000, "g", SI=True)
cm = metre / 100

minute = U(second * 60, "min")
hour = U(minute * 60, "h")
day = U(hour * 24, "d")
week = day * 7
fortnight = week * 2
year = U(day * 365.25, "yr")

kmph = metre * 1000 / hour

bpm = U(hertz / 60, "bpm")

degree = U(radian * pi / 180, "°")
angular_minute = U(degree / 60, "′")
angular_second = U(degree / 3600, "″")

acre = U(100 * metre**2, "a")
hectare = U(100 * acre, "ha")
litre = U((metre / 10)**3, "l", SI=True)
tonne = ton = U(kilogram * 1000, "t", SI=True)

watt_hour = U(watt * hour, 'Wh', SI=True)
amp_hour = ampere_hour = U(ampere * hour, 'Ah', SI=True)