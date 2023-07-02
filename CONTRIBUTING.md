Thank you for reading this! Pull requests are absolutely welcome and appreciated, especially to add new units.

# Development environment

You'll need `pip install pyright unittest` to run tooling.

> **Warning**
> Note that running Noether from source will raise errors on missing files.
> This is intentional - you must `make units` first.

## Catalogue shorthand

`make units` utilises `noe_transformer.py` to transpile `.units.py` files into Python.

Note that this is not Python – it is a strict subset of its syntax (namely imports and equalities only) that is transpiled.

This is in alpha; it is only used in a few corners of the catalogue and has not yet been fully and formally defined.

It is the intent to have the catalogue entirely use this system. Until then, for `.gitignore` purposes, the transpiled result is `_.py` rather than `.py`.

## Under the hood

`noether.core` provides the SI base units, from which almost all other units in `catalogue` are derived.

The essential classes are:

- `Multiplication`, a dict of exponents (eg `{'length': 1', 'time': -1}`) that handles `*`, `**`, `/`.
  - `Dimension`, (which mostly handles display)
- `Prefix`, such as `milli` or `tera`
- `Measure`, a subclass of `Generic[Real]`, which holds a `.value`, `.stddev` and `.dim`.
  - `Unit`, a named `Measure` used for display purposes.

Other classes handle configuration, collation and display. 

## Internal style guide

- Consistency is useful but not the goal.
  - Use whichever of `'` and `"` is convenient.
- Comments explain why, not what. Code should be written in a way that is clear and not confusing. Python is hardly the fastest language – slight inefficiency is not a problem.
- Imports are done in "paragraphs", usually from generic to specific imports.
- Files with a single class are named after them.