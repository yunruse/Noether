# Noether (in development: Alpha 0.1.2)

## The problem: million-dollar errors are easy to make

[We're](https://medium.com/predict/a-328-million-dollar-conversion-error-f6d525c85fd2) [all](https://www.pri.org/stories/2012-02-23/new-clues-emerge-centuries-old-swedish-shipwreck) [human](https://www.bbc.co.uk/news/magazine-27509559).
Whether you're a layman, a student or a NASA senior, it's immensely easy to make simple mistakes, especially when working with physical measurements. A good programming language will shout at you if you try to add a list to a number, so why shouldn't it stop you adding a metre to a minute? Enter Noether.

```bash
pip install noether&& python3.7 -im noether
```

You can use Noether as a calculator or in simulations (though at the moment it's not exactly performant). Noether is intended to compliment `numpy`, `matplotlib` and `scipy` with

- A disturbingly extensive and constantly-updated catalogue of scientific units, measurements and constants
- Automatic unit conversion, and propagation of dimension and statistical error

In the pipeline:

- Advanced support for more sophisticated statistical errors 
- Treat functions like code with [ASTley], and automagically graph them in a REPL
- Use [Astley]'s code analysis with Numba to ensure both code safety and performance 

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

>>> health = Dimension.new('health', dimsym='H', unitsym='a')
>>> apple = Unit(health)
>>> apple / day
1.157×10⁻⁵a·s⁻¹
```

## Installation and use

Noether currently requires Python 3.7 or above. It's easy to jump into a quick calculator-like instance quick:

```bash
pip install noether
python -im noether
```

This simply runs `import noether as noe` and `from noether import *`. We'll assume the latter has been done; it makes for a neater experience when working with units.

Some yet-undocumented submodules may happen to require `astley`,  `numpy`, `matplotlib` and `scipy` to use:

```bash
pip install numpy matplotlib
git clone https://github.com/yunruse/astley
# modify your PATH as needed
```

## Update log

Updates are released to the `master` branch every couple of weeks. They are not guaranteed to have a sturdy, documented and tested API just yet, but each release should be pretty dang stable.

Every single change I plan to make can be found on my [kanban board]. Thanks to internet magic, this appears live, exactly as I see and edit. If you have a feature suggestion, drop me an issue on GitHub. Bug fixes will stay in GitHub: they're much more important than features.

[kanban board]: https://www.notion.so/714348466a284bd1b0d1942c81688579

 - **Alpha 0.1.2** (2020-05-07):
   - Added basic config support.
   - This is the first PyPI release.

 - **Alpha 0.1.1** (2020-02-16):
   - Many bugfixes and units added.
   - Added `noether.fraction` with `ContinuedFraction` (and `Fraction` with shortcut).
   - Introduced basic backend for `UnitSystem` for quality of life (eg `display(imperial)`).
   - Made special tweaks so `python -m noether` lazy-loads at fast pace.

 - **Alpha 0.1** (2020-01-26):
   - Made many improvements to display of units.
   - The global `display` was added, alongside a wide range of particles.
   - A test suite begins development.

## Thank you!

This project has a decently large scope, and I want it to appeal to anybody who has ever needed to measure anything. Your feedback, no matter how small, means a lot to me!

## Legal (and academical)

Copyright (c) Mia yun Ruse ([yunru.se]) 2018–2020.
All scientific data shown remains in the public domain, and is cited where relevant.

This work is licensed under a [Creative Commons Attribution 4.0](cc) International
license. In non-legal terms: do whatever you like, including science! But if you
want to redistribute this project (derived or not), please credit me, or shoot me a
message and I'll see what I can do.

[yunru.se]: https://yunru.se/
[cc]: https://creativecommons.org/licenses/by/4.0/
