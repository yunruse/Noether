# Noether (in development: Alpha 2)

**Noether is currently in alpha. The developer makes no promise that the API will remain consistent, or even documented.**

Noether is a library designed to provide physical constants and measurements. It is intended to compliment `numpy`, `matplotlib` and `scipy`. Its features include:

- An extensive catalogue of scientific units and statistical distributions
- Automatic propagation of dimension and uncertainty for unit-rich work
- Basic graphing (currently requires [Astley])
- Basic support for propagating statistical error

Custom objects that can be made to extend Noether:

- `Unit`: for calculation, convention, or display
- `Dimension`: to check conservation or for display
- `Distribution`: to generate rich statistical distributions

[Astley]: https://github.com/yunruse/astley

## Installation and use

Noether is currently in development, so there is no package to install. It currently requires scipy for a few odd functions, but that will likely be removed much later in development.

```bash
pip install numpy matplotlib scipy
git clone https://github.com/yunruse/noether
```

If Linux gives you numpy errors:
```bash
pip3 uninstall numpy
apt-get install python3-numpy
```

If you don't want to put Noether and requisite Astley on the PATH, navigate to this folder and run

```bash
python -im noether
```

To use in a script (eg to not repeat yourself in calculations), run

```python
from noether import *
```

at the head of your script.

## Units

Noether has a thorough SI-based unit system allowing for advanced unit composition and dimensional analysis.

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

You may, of course, define your own units on the fly:
```
>>> FF = Unit(furlong / fortnight, 'ff')
>>> display(FF)
>>> c
1.803×10¹² <velocity, speed>
```

If you need to measure something rather new, you can define a dimension:

```
>>> health = Dimension.new(3.2, 'health', 'H', 'a')
>>> apple = Unit(health)
>>> apple / day
1.157×10⁻⁵a·s⁻¹
```

## Update log

 - **Alpha 2** (2020-02-16):
   - Many bugfixes and units added.
   - Added `noether.fraction` with `ContinuedFraction` (and `Fraction` with shortcut).
   - Introduced basics of `UnitSystem` for quality of life (eg `display(imperial)`).
   - Made special tweaks so `python -m noether` lazy-loads at fast pace.

 - **Alpha 1** (2020-01-26):
   - Made many improvements to display of units.
   - The global `display` was added, alongside a wide range of particles.
   - A test suite begins development.

## Thank you!

Noether is in early development. Please consider supporting me on [Patreon].

Any and all feedback, from scientist to schoolchild, is well-appreciated.
This project is large, and somehow wants to appeal to every single person who
would ever use a calculator, so it'll never be perfect :)

[Patreon]: https://patreon.com/yunruse

## Legal (and academical)

Copyright (c) Mia yun Ruse ([yunru.se]) 2018–2020.
All scientific data shown remains in the public domain, and is cited where relevant.

This work is licensed under a [Creative Commons Attribution 4.0](cc) International
license. In non-legal terms: do whatever you like, including science! But if you
want to redistribute this project (derived or not), please credit me, or shoot me a
message and I'll see what I can do.

If for some strange reason you find this useful in a scientific paper
– aah, it's not fully tested yet! – please throw me a reference and an email.

[yunru.se]: https://yunru.se/
[cc]: https://creativecommons.org/licenses/by/4.0/
