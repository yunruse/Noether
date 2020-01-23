# Noether

**Noether is currently in development, so its API is subject to change, and some features may be incomplete or undocumented.**

Noether is a library designed to compliment `numpy`, `matplotlib` and `scipy` by providing a rich category of real-world values from CODATA, SI and more. It provides, for your convenience:

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

## Development

Noether has infrequent development, so it has a rather small test suite and incomplete API. T

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

Copyright (c) Mia yun Ruse (yunru.se) 2019-2020.

This work is licensed under a [Creative Commons Attribution 4.0](cc) International
license. In non-legal terms: do whatever you like, but don't forget to credit me :)

[cc]: https://creativecommons.org/licenses/by/4.0/
