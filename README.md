# Noether (in development: Alpha 1.1)

## The problem: million-dollar errors are easy to make

[We're](example1) [all](example2) [human](example3). Whether you're a layman, a student or a NASA senior, it's immensely easy to make simple mistakes, especially when working with physical measurements. A good programming language will shout at you if you try to add a list to a number, so why shouldn't it stop you adding a metre to a minute? Enter Noether.

[example1]: https://medium.com/predict/a-328-million-dollar-conversion-error-f6d525c85fd2
[example2]: https://www.pri.org/stories/2012-02-23/new-clues-emerge-centuries-old-swedish-shipwreck
[example3]: https://www.bbc.co.uk/news/magazine-27509559

```bash
git clone https://github.com/yunruse/noether && cd noether && python3.7 -im noether
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

This project is large, and I want it to appeal to anybody who has ever measured anything. I'd love one day to adapt it into a mobile app so it could make everyone's life that little bit easier. So, that said, please send feedback!

## Legal (and academical)

Copyright (c) Mia yun Ruse ([yunru.se]) 2018–2020.
All scientific data shown remains in the public domain, and is cited where relevant.

This work is licensed under a [Creative Commons Attribution 4.0](cc) International
license. In non-legal terms: do whatever you like, including science! But if you
want to redistribute this project (derived or not), please credit me, or shoot me a
message and I'll see what I can do.

[yunru.se]: https://yunru.se/
[cc]: https://creativecommons.org/licenses/by/4.0/
