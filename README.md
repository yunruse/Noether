# Noether (in development: Alpha 0.1.3)

## The problem: computers don't understand physical measurements

A calculator does the little things. They weren't essential, at first, but it's rather nice to not have to do the conversion in your head when you can instead start worrying about the topic at hand. Why not extend this to units? This is far from a nicety: NASA famously lost *328 million dollars* because [feet and metres were mistaken](https://medium.com/predict/a-328-million-dollar-conversion-error-f6d525c85fd2). 

Whether you're a layman, a student, or a NASA programmer, Noether should make working with numbers a lot more pleasant:

- Work with measurements, not numbers: Noether automagically handles unit conversions and operations.
- Work in whatever unit system you and your colleagues like – units naturally interoperate.
- It propagates uncertainty – meaning you don't have to be so uncertain you propagated it right yourself.
- Save your effort typing and trawling Wikipedia: physical constants, units and definitions are defined and kept up to date with ISO, SI, CODATA, and other authoritative sources, so you don't have to be.
- Noether has a variety of useful addons that might also help out with general use as a calculator.

You can use Noether like a calculator or import it for projects. Noether is intended to compliment `numpy` and `matplotlib`; while it is yet in early stages, it will inevitably be integrated smoothly with these.

## Usage 

Dig right in straight away:

```bash
pip install noether
python3.7 -im noether
```

Noether requires `pip install toml`, and some extras for addons, namely `numpy`, `matplotlib` and `scipy`, which are presently included as requirements.

From here on out we'll assume you did `python -im noether`. This does `import noether as noe; from noether import *; display = `, which is very useful if you want to use Noether as a calculator.

And, well, it has almost every unit known: BMI, bushel and byte; eotvos, erg and electronvolt; parsec, plethron and potrzebie. Units are displayed very consciously: the dimension is displayed, scientific notation is summoned if deemed necessary; even electronagmetic data is displayed.

```
>>> 0.5 * gibibyte / second
4.295×10⁹bps <data rate>
>>> metre
1m <wavelength: radio, VHF, P>
>>> (joule / kilogram / kelvin)(12, 2)
12 ± 2K⁻¹·m²·s⁻² <specific heat capacity>
>>> e / electron.mass
(2.187×10¹¹ ± 1649)A·kg⁻¹·s
>>> 12 * pixel / mm
1.2×10⁴pix·m⁻¹ <image quality>
```

When using Noether, you may use `display(unit)` to override what units are used for display:

```
>>> display(ppi)
>>> 12 * pixel / mm
304.8ppi <image quality>
>>> display()
>>> 12 * pixel / mm
1.2×10⁴pix·m⁻¹ <image quality>
```

You may, of course, define your own units and even dimensions on the fly:

```
>>> FF = Unit(furlong / fortnight, 'ff')
>>> display(FF)
>>> c
1.803×10¹²ff <velocity, speed>

>>> health = Dimension.new('health', dimsym='H', unitsym='a')
>>> apple = Unit(health)
>>> print(health * time)
H·T
>>> apple / day
1.157×10⁻⁵a·s⁻¹
```

## Addons

Addons are stored in the `addons` folder. They're not imported by default, and as such make use of `matplotlib`, `numpy`, `scipy` to various degrees to get their job done. Matrices, fractions, unit-aware functions; these are some niceties, but they're not necessarily fully-featured.

Presently, `numpy.addons.graphing` (requires [`astley`](https://github.com/yunruse/astley)) provides a nice interface to graphing functions.

## Updates and development

Updates are released to the `release` branch (and PyPI) every so often. They are not guaranteed to have a sturdy, documented and tested API just yet, but each release should be pretty stable.

Anything that uses more than `toml` should be put in `addons`.

Currently (as of August 2021) Noether is in **semi-hiatus**: when I find myself in need of a specific new feature in Noether I will definitively add it, and then likely some more bits and bobs. Any units I run into in the wild will of course be added in also. Hoerver, systematic changes are unlikely and will required more time. Please feel free to raise issues or feature requests on GitHub, though, and I'll be more than happy to get working on them.

## Legal

Copyright (c) Mia yun Ruse ([yunru.se]) 2018–2021.

With the exception of scientific data, which is cited where relevant,
Noether is licensed under a [Creative Commons Attribution 4.0](cc) International
license. In non-legal terms: do whatever you like, including science! But if you
redistribute or fork Noether, you must credit me.

[yunru.se]: https://yunru.se/
[cc]: https://creativecommons.org/licenses/by/4.0/
