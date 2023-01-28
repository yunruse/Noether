# Noether (in development: Alpha 0.2.0)

> **Note**
>
> Version 1.0 is coming soon (February 2023), rewritten from scratch and way more capable!
>
> Check out the [`rewrite`](https://github.com/yunruse/Noether/tree/rewrite) branch for more.

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

## Updates and development

Updates are released to the `release` branch (and PyPI) every so often. They are not guaranteed to have a sturdy, documented and tested API just yet, but each release should be pretty stable.

## Also check out...

Other Python unit packages include:

- [units](https://pypi.org/project/units/), a simple package for defining your own units
- [unyt](https://pypi.org/project/unyt/), which has numpy support

## Legal

Copyright (c) 2018–2022 Mia yun Ruse ([yunru.se]).

With the exception of scientific data, which are cited, Noether is licensed under a [Creative Commons Attribution 4.0](cc) International license. In non-legal terms: do whatever you like, including science!
But if you redistribute or fork Noether, you must credit me.

[yunru.se]: https://yunru.se/
[cc]: https://creativecommons.org/licenses/by/4.0/
