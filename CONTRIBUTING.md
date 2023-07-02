Thank you for reading this! Pull requests are absolutely welcome and appreciated, especially to add new units.

# Development environment

You'll need `pip install pyright unittest` to run tooling.

> **Warning**
> Note that running Noether from source will raise errors on missing files.
> This is intentional - you must `make units` first.

## Catalogue shorthand

`make units` utilises `noe_transformer.py` to transpile `.noe.py` files into `._py` files.

The custom `.noe.py` format is not formally specified (or complete) but its shorthand allows for niceties like e.g.
 `a = b = 'c' = foo` instead of `a = b = Unit(foo, ['a', 'b'], ['c']]`,
which, when you have a lot of units, is really rather useful.

Note that this is not Python – it is a strict subset of its syntax (namely imports and equalities only) that is transpiled.

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