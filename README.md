# Noether (in development: Alpha 1.1)

Noether is a library designed to provide physical constants and measurements. It is intended to compliment `numpy`, `matplotlib` and `scipy` with features such as:

- An extensive catalogue of scientific units and statistical distributions
- Automatic propagation of dimension and uncertainty for unit-rich work
- Basic graphing (currently requires [Astley])
- Basic support for propagating statistical error

[Astley]: https://github.com/yunruse/astley


## Units

BMI, bushel and byte; eotvos, erg and electronvolt; parsec, plethron and potrzebie. Noether has (almost) every unit known, with a thorough unit system allowing for automatic dimensional analysis.

```python
>>> 0.5 * gibibyte / second
4.295×10⁹bps <data rate>
>>> a = 12 * pixel / mm
>>> a
1.2×10⁴pix·m⁻¹ <image quality>
>>> display(ppi)
>>> a
304.8ppi <image quality>
>>> (joule / kilogram / kelvin)(12, 2)
12 ± 2K⁻¹·m²·s⁻² <specific heat capacity>
>>> e / electron.mass
(2.187×10¹¹ ± 1649)A·kg⁻¹·s
```

You may, of course, define your own units and dimensions on the fly:

```
>>> FF = Unit(furlong / fortnight, 'ff')
>>> display(FF)
>>> c
1.803×10¹²ff <velocity, speed>

>>> health = Dimension.new(3.2, 'health', 'H', 'a')
>>> apple = Unit(health)
>>> apple / day
1.157×10⁻⁵a·s⁻¹
```

## Installation and use

Noether currently requires Python 3.7 or above. It's not yet on PyPI, but it's easy to jump into a quick calculator-like instance quick:

```bash
git clone https://github.com/yunruse/noether
cd noether
python -im noether
```

This simply runs `import noether` and `from noether import *`. Documentation assumes the latter has been done; it makes for a neater experience.

Some yet-undocumented submodules may require `astley`,  `numpy`, `matplotlib` and `scipy` to use:

```bash
pip install numpy matplotlib
git clone https://github.com/yunruse/astley
# modify your PATH as needed
```

## Update log

Updates are released to the `master` branch every couple of weeks. They are not guaranteed to have a sturdy, documented and tested API just yet, but each release should be pretty dang stable.

 - **Alpha 1.1** (2020-02-16):
   - Many bugfixes and units added.
   - Added `noether.fraction` with `ContinuedFraction` (and `Fraction` with shortcut).
   - Introduced basic backend for `UnitSystem` for quality of life (eg `display(imperial)`).
   - Made special tweaks so `python -m noether` lazy-loads at fast pace.

 - **Alpha 1** (2020-01-26):
   - Made many improvements to display of units.
   - The global `display` was added, alongside a wide range of particles.
   - A test suite begins development.

## Thank you!

From schoolchild to scientist, all feedback is appreciated. This project is large, and somehow wants to appeal to every single person who would ever use a calculator, so it'll never be perfect :)

Oh, and while you're here – Noether is in early development. Please consider supporting me on [Patreon].

[Patreon]: https://patreon.com/yunruse

## Legal (and academical)

Copyright (c) Mia yun Ruse ([yunru.se]) 2018–2020.
All scientific data shown remains in the public domain, and is cited where relevant.

This work is licensed under a [Creative Commons Attribution 4.0](cc) International
license. In non-legal terms: do whatever you like, including science! But if you
want to redistribute this project (derived or not), please credit me, or shoot me a
message and I'll see what I can do.

[yunru.se]: https://yunru.se/
[cc]: https://creativecommons.org/licenses/by/4.0/
