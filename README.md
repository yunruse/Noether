# Noether

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Noether is a physics REPL, with a dynamic units system,

## Installation and setup

I recommend Python 3.7, but I've tried to keep compatability to 3.5.

Just run from the command line:

```bash
pip install numpy matplotlib scipy noether

python3 -m noether

# do this if Linux gives you numpy errors
pip3 uninstall numpy
apt-get install python3-numpy
```

## Using

Noether has a thorough SI-based unit system allowing for advanced unit composition and dimensional analysis.

```python
>>> FF = Unit(Furlong / Fortnight, 'ff')
>>> 3 * FF
4.989×10⁻⁴ m·s⁻¹ (speed)

```

Of course, if you don't want to specify a unit each and every time, you can happily turn it off:

```python
>>> units.showUnits = False
>>> units.precision = 5
>>> 3 * FF
4.989×10⁻⁴
```

## Update log

- Still in development

## Legal

Copyright (c) Jack Dobson (yunru.se) 2018.

This work is licensed under a [Creative Commons Attribution 4.0](cc) International
license. In non-legal terms: do whatever you like, but credit me.

The full license is available here: [Creative Commons ]

[cc]: https://creativecommons.org/licenses/by/4.0/
