Thank you for reading this!

> **Warning**
> Note that running Noether from source will raise errors on missing files.
> This is intentional - you must `make units` first.

# Catalogue

If you want to help out, the [units](analysis/units.md) article lists every Wikipedia article about units. Pull requests are welcomed for all units which have a credible source and are in roughly the right section.

## `.units.py` shorthand

`make units` utilises `noe_transformer.py` to transpile `.units.py` files into Python.

Note that this is not actual Python – it is a strict subset of its syntax (namely imports and equalities only) that is transpiled.

This is in alpha; it is only used in a few corners of the catalogue and has not yet been fully and formally defined.

It is the intent to have the catalogue entirely use this system. Until then, for `.gitignore` purposes, the transpiled result is `_.py` rather than `.py`.

# Noether engine development

You'll need `pip install pyright unittest` to run tooling.

## Internal style guide

- Files are named directly after the class they contain.
- Use `autopep8` and `pyright`

## Under the hood

`noether.core` provides the SI base units, from which almost all other units in `catalogue` are derived.

The essential classes are:

- `Multiplication`, a dict of exponents (eg `{'length': 1', 'time': -1}`) that handles `*`, `**`, `/`.
  - `Dimension`, (which mostly handles display)
- `Prefix`, such as `milli` or `tera`
- `Measure`, a subclass of `Generic[Real]`, which holds a `.value`, `.stddev` and `.dim`.
  - `Unit`, a named `Measure` used for display purposes.

Other classes handle configuration, collation and display. 