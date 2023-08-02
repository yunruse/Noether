# Noether
`523 units, 60 prefixes`

[![PyPI](https://img.shields.io/pypi/v/noether?color=blue)](https://pypi.org/packages/noether)

**Noether** is a unit-enriched Python package, akin to Wolfram Alpha or gnu `units`. It has a large (and expanding) catalogue of up-to-date units and constants, allowing code to be written directly in the units they are concerned with while also ensuring e.g. you don't mistakenly add an energy to a length.

Just grab Python 3.10 or later and `pip install noether` to run!

Development is ongoing, especially in expanding the unit catalogue and improving unit display mechanisms.

## Usage 

Noether can be used as a Python package or as a CLI:

```sh
$ alias noe='python -im noether'
$ noe marathon
marathon  # length, 42195 m, Race length based on Greek legend, set by convention from 1908 Summer Olympics
$ noether 23degC @ degF
73.4 °F  # temperature
$ noether 'horsepower @ dB(kW)'
-1.33418061 dB(kW)  # power, 0.73549875 kW
```

The CLI allows a few niceties such as slightly terser syntax, but otherwise behaves identically to Python:

```sh
$ noether 5cm @ in --value
1.9685039370078738
$ python
>>> from noether import *
>>> 5*cm @ inch
1.9685039370078738 in  # length
```

In addition to `@` for display, you can more permanently set display units:

```py
>>> display(inch)
>>> 5 * cm
>>> mile
mile  # length, 63360 in
```

Units propagate uncertainty automatically under most operations:

```py
>>> m(5, 0.1)**3
125 ± 7.5 m**3  # volume
```

You can define your own units and dimensions:

```py
>>> foo = Unit(3e11 * furlong / fortnight, 'foo')
>>> c @ foo
6.008724999284181 foo  # speed

>>> health = Dimension.new('health', 'H')
>>> apple = Unit(health, 'apple', 'a')
>>> apple / day
apple / day  # health / time, 1.1574074074074073e-05 a / s
```

Various `conf` settings allow for customisation to behaviour:

```py
>>> conf.info_spectrum = True
>>> nm(400)
4e-07 m  # length, visible, purple
```

Use `conf.save()` to save to (by default) `~/.config/noether.toml`.


## For more, see...

- [CHANGELOG.md](https://github.com/yunruse/Noether/blob/release/CHANGELOG.md)
- [CONTRIBUTING.md](https://github.com/yunruse/Noether/blob/release/CONTRIBUTING.md)
- [LICENSE.txt](https://github.com/yunruse/Noether/blob/release/LICENSE.txt)

Other tools for working with units include:

- [Wolfram Alpha](https://www.wolframalpha.com), a comprehensive online intelligence engine
- [gnu `units`](https://www.gnu.org/software/units/), a command-line tool you likely already have
- [units](https://pypi.org/project/units/), a simple Python package for defining your own units
- [unyt](https://pypi.org/project/unyt/), a Python package with numpy support

### 📚 _**Did you know?**_

```
>>> lunation / (year % lunation)
2.7153489666011486
```
A [**lunation**](https://en.wikipedia.org/wiki/Lunar_month#Synodic_month) (about 29 days) separates one full moon from another. Every so often a thirteenth full moon occurs in a year - "a [blue moon](https://en.wikipedia.org/wiki/Blue_moon)". "Once in a blue moon" is actually only every 2.71 years or so - not as rare as you'd think. Don't tell Sinatra!