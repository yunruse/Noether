# Noether

**Noether is currently in development, so its API is subject to change, and some features may be incomplete or undocumented.**

Noether is a library designed to compliment `numpy`, `matplotlib` and `scipy` by providing a rich category of real-world values from CODATA, SI and more. It provides, for your convenience:

- An extensive catalogue of scientific units and statistical distributions
- Automatic propagation of dimension and uncertainty for unit-rich work
- Basic graphing (requires [Astley])
- Basic support for propagating statistical error

Custom objects that can be made to extend Noether:

- `Unit`: for calculation, convention, or display
- `Dimension`: to check conservation or for display
- `Distribution`: to generate rich statistical distributions

On the cards for future features:

- More mature SI presentation when a named unit is not found (eg in terms of Joules or Newtons)
- More extensive maths suite for propagating errors
- Linting to verify measure annotations
- Optional linting for symbols to warn that, eg, `E` is not in Joules
- Support for vecotrs and tensors via NumPy

On the cards for features relying on [Astley], which allows code (and therefore formulae) to be treated as objects:

- Automatic translation of MathJax/LaTeX notation to Python+Noether and vice versa
- More pronounced introspection
- Algebraic manipulation (eg analytic calculus, simplifying functions)

[Astley]: https://github.com/yunruse/astley

## Installation and use

Noether is currently in development, so there is no package to install. It currently requires scipy for a few odd functions, but it may remove this requirement before release to lower install size.

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
>>> gibibyte / second
8.59×10⁹bps <data rate>
>>> 12 * pixel / mm
304.8ppi <image quality>
>>> (joule / kilogram / kelvin) * Measure(12, 2)
12 ± 2K⁻¹·m²·s⁻² <specific heat capacity>
```

You may define and display units as such:
```
>>> FF = Unit(furlong / fortnight, 'ff')
>>> 3 * FF
4.989×10⁻⁴ m·s⁻¹ (speed)
>>> Unit.display(FF)
>>> 3 * FF
3ff (speed)
```

If you need to measure something obscure, you can define a dimension:
```
>>> health = Dimension.new(3.2, 'health', 'a')
>>> apple = Unit(health, names=['apple'], symbols=['a'])
>>> apple / day
1.157×10⁻⁵a·s⁻¹
```

## Update log

Currently pre-release.

## Legal

Copyright (c) Mia Dobson (yunru.se) 2019.

This work is licensed under a [Creative Commons Attribution 4.0](cc) International
license. In non-legal terms: do whatever you like, but credit me.

The full license is available here: [Creative Commons ]

[cc]: https://creativecommons.org/licenses/by/4.0/
