# Noether 1.0

[![PyPI](https://img.shields.io/pypi/v/noether?color=blue)](https://pypi.org/packages/noether)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/noether)](https://pypi.org/packages/noether)
[![Support (Discord)](https://img.shields.io/discord/885908649342537810?label=support)](https://discord.gg/7DcwrA3c3y)
[![License](https://img.shields.io/github/license/yunruse/noether?color=blue)](LICENSE.txt)
[![Python version compatibility](https://github.com/yunruse/Noether/actions/workflows/test-compatibility.yml/badge.svg?branch=release)](https://github.com/yunruse/Noether/actions/workflows/test-compatibility.yml)

TODO: rewrite this to be less advertisey

## The problem: computers don't understand physical measurements

A calculator does the little things. They weren't essential, at first, but it's rather nice to not have to do the conversion in your head when you can instead start worrying about the topic at hand. Why not extend this to units? This is far from a nicety: NASA famously lost *328 million dollars* because [feet and metres were mistaken](https://medium.com/predict/a-328-million-dollar-conversion-error-f6d525c85fd2). 

Whether you're a layman, a student, or a NASA programmer, Noether should make working with numbers a lot more pleasant:

- Work with measurements, not numbers: Noether automagically handles unit conversions and operations.
- Work in whatever unit system you and your colleagues like – units naturally interoperate.
- It propagates uncertainty – meaning you don't have to be so uncertain you propagated it right yourself.
- Save your effort typing and trawling Wikipedia: physical constants, units and definitions are defined and kept up to date with ISO, SI, CODATA, and other authoritative sources, so you don't have to be.
- Noether has a variety of useful addons that might also help out with general use as a calculator.

You can use Noether like a calculator or import it for projects. Noether is intended to compliment `numpy` and `matplotlib`; while it is yet in early stages, it will inevitably be integrated smoothly with these.

## Usage 

Dig right in straight away:

```bash
pip install noether
python3.7 -im noether
```

From here on out we'll assume you did `python -im noether`, which does a few extra niceties to make it calculator-ready.

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

When using Noether, you may use `display(unit)` to override what units are used for display. However, you can also use `@ unit` to quickly see what's going on. You can even chain units together with `&`!

```
>>> 12 * pixel / mm
1.2×10⁴pix·m⁻¹ <image quality>
>>> 12 * pixel / mm @ ppi
304.8ppi <image quality>

>>> meter @ foot & inch
3 ft + 3.3701 in <length>
```

You may, of course, define your own units and even dimensions on the fly:

```
>>> FF = Unit(furlong / fortnight, 'ff')
>>> c @ FF
1.803×10¹² FF <velocity, speed>

>>> health = Dimension.new('health', 'H')
>>> apple = Unit(health)
>>> print(health * time)
H·T
>>> apple / day
1.157×10⁻⁵a·s⁻¹
```

## For more, see...

Check out [CONTRIBUTING.md](CONTRIBUTING.md) and [LICENSE.txt](LICENSE.txt) for info of that sort.

Other tools for working with units include:
- [Wolfram Alpha](https://www.wolframalpha.com), a comprehensive online intelligence engine
- [gnu units](https://www.gnu.org/software/units/), a command-line tool that you likely already have
- [units](https://pypi.org/project/units/), a simple Python package for defining your own units
- [unyt](https://pypi.org/project/unyt/), a Python package with numpy support

### 📚 _**Did you know?**_
Half of a `byte` is a `nibble`! The unit represents 4 bits of data.