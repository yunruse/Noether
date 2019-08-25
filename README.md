# Noether

Noether is a library supporting units of measure, amongst other things, and can be used as an advanced scientific calculator.

It features:

- Dynamic units with an extensive catalogue for ease of use
- Ability to arbitrarily create units or dimensions of measure
- Automatic dimensional analysis
- Basic graphing (requires [Astley])

[Astley]: https://github.com/yunruse/astley

## Installation and use

Noether is currently in development, so there is no package to install - instead, navigate to where you want to install Noether, and run:

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
8.59×10⁹bps (data rate)
>>> 12 * pixel / mm
304.8ppi (image quality)
```

You may define and display units as such:
```
>>> FF = BaseUnit(furlong / fortnight, 'ff')
>>> 3 * FF
4.989×10⁻⁴ m·s⁻¹ (speed)
>>> Unit.display(FF)
>>> 3 * FF
3ff (speed)
```

If you need to measure something obscure, you can define a dimension:
```
>>> health = Dimension.new(3.2, 'health', 'a')
>>> apple = BaseUnit(health, names=['apple'], symbols=['a'])
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
