Thank you for reading this! Pull requests are absolutely welcome and appreciated.

Even if you're not a developer, information on how you use calculators like Noether is very interesting. Feel free to contact me `noether AT yunru.se`!

# Development environment

You'll need `pip install pyright unittest` to run tooling.

> **Warning**
> Note that running Noether from source will raise errors on missing files.
> This is intentional - you must `make catalogue` first.
> For info on the (optional) catalogue shorthand being transpiled, see below.

## Catalogue shorthand

As you may have seen, the `noe_transformer.py` tool transforms `.noe.py` files into `._py` files.
This fixes a lot of annoying shenanigans, allowing you to do `a = b = 'c' = foo` instead of `a = b = Unit(foo, ['a', 'b'], ['c']]`.
It is currently in development.

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