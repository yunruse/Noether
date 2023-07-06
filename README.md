# Noether 2.0

[![PyPI](https://img.shields.io/pypi/v/noether?color=blue)](https://pypi.org/packages/noether)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/noether)](https://pypi.org/packages/noether)
[![Support (Discord)](https://img.shields.io/discord/885908649342537810?label=support)](https://discord.gg/7DcwrA3c3y)
[![License](https://img.shields.io/github/license/yunruse/noether?color=blue)](LICENSE.txt)
[![Python version compatibility](https://github.com/yunruse/Noether/actions/workflows/test-compatibility.yml/badge.svg?branch=release)](https://github.com/yunruse/Noether/actions/workflows/test-compatibility.yml)

**Noether** is a unit-enriched Python package, akin to Wolfram Alpha or gnu `units`. It has a large (and expanding) catalogue of up-to-date units and constants, allowing code to be written directly in the units they are concerned with while also ensuring e.g. you don't mistakenly add an energy to a length.

Noether can be used on the command-line (`alias noether='python -im noether'`) or as a package.

Development is ongoing, especially in unit display and cataloguing.

## Usage 

Grab Python 3.11 or later and dig in:

```bash
pip install noether
alias noe='python -im noether'
noe
```

Work with units:

// fix below \\

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
```
$ noether 'saros @ year & day'
18 yr + 10.95 d  # time
```
Exactly one *saros* after a solar eclipse occurs, another occurs in roughly the same place.
It is one of the measurements made by the Antikythera mechanism - the world's oldest mechanical computer.