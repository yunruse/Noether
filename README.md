# Noether (in development: Alpha 0.1.2)

## The problem: computers don't understand physical measurements

A calculator does the little things. They weren't essential, at first, but it's rather nice to not have to do the conversion in your head when you can instead start worrying about the topic at hand. Why not extend this to units? This is far from a nicety: NASA famously lost *328 million dollars* because [feet and metres were mistaken](https://medium.com/predict/a-328-million-dollar-conversion-error-f6d525c85fd2). 

Whether you're a layman, a student, or a NASA programmer, Noether should make working with numbers a lot more pleasant:

- Work with measurements, not numbers: Noether automagically handles unit conversions and operations.
- Work in whatever unit system you and your colleagues like – units naturally interoperate.
- It propagates uncertainty – meaning you don't have to be so uncertain you propagated it right yourself.
- Save your effort typing and trawling Wikipedia: physical constants, units and definitions are defined and kept up to date with ISO, SI, CODATA, and other authoritative sources, so you don't have to be.

You can use Noether like a calculator or import it for projects. Noether is intended to compliment `numpy` and `matplotlib`; while it is yet in early stages, it will inevitably be integrated smoothly with these.

Dig right in straight away:

```bash
pip install noether
python3.7 -im noether
```

## Units

(From here on out we'll assume you did `python -im noether`, which does `import noether as noe` and provides a bundle of constants in the namespace.)

Noether has almost every unit known: BMI, bushel and byte; eotvos, erg and electronvolt; parsec, plethron and potrzebie. It makes the bold assumption you know how to use it, so the REPL is a lot more informative:

```
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

## Updates and development

Updates are released to the `master` branch (and PyPI, and the release log!) every so often. They are not guaranteed to have a sturdy, documented and tested API just yet, but each release should be pretty stable. 

If running from source, Noether requires `pip install toml`.

Every single change I plan to make can be found on my [kanban board]. Thanks to internet magic, this appears live, exactly as I see and edit. If you have a feature suggestion, drop me an issue on GitHub. Issues will stay in GitHub: they're much more important than features.

[kanban board]: https://www.notion.so/714348466a284bd1b0d1942c81688579

## Legal

Copyright (c) Mia yun Ruse ([yunru.se]) 2018–2020.

With the exception of scientific data, which is cited where relevant,
Noether is licensed under a [Creative Commons Attribution 4.0](cc) International
license. In non-legal terms: do whatever you like, including science! But if you
want to redistribute this project (derived or not), please credit me, or shoot me a
message and I'll see what I can do.

[yunru.se]: https://yunru.se/
[cc]: https://creativecommons.org/licenses/by/4.0/
