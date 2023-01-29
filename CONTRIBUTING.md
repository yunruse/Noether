Thank you for reading this! Every pull request is certainly appreciated.

Even if you're not a developer, information on how you use calculators like Noether is very interesting. Feel free to contact me `noether AT yunru.se`!

## Git shenanigans

### Branches

The following branch structure is is in use:

- [`release`](https://github.com/yunruse/Noether/tree/develop) is the release version; it is a mirror of PyPI.
  - [`develop`](https://github.com/yunruse/Noether/tree/develop)
    - Any feature development is done directly on `develop` or in branches.
    - [`testing`](https://github.com/yunruse/Noether/tree/testing) is used to ~~experiment~~ toy with code to check that automatic unit testing works.

### Automatic unit testing

The `tests` directory contains a few analysis tools (mostly for analysing the catalogue), and unit testing, which is ran automatically on commits to `testing` and pull requests to `release` or `develop`.

## Under the hood

### Module structure

- `noether.core`: Core code, with the bare essentials (`meter`, `second`, etc). Can be run as-is.
- `noether.catalogue`: All units and dimensions, sectioned into categories.
- `noether.catalogue.extension`: Less essential units, such as historical or whimsical units. Gotta catch 'em all!
- `noether.catalogue.info`: `MeasureInfo` handlers for displaying info about units.

### Class structure

- `ConfigOption`, which is registered in various places in code
- `Config`, which internally holds a `dict` of user settings
- `Dimension`, an `ImmutableDict` which holds dimension names and exponents (eg `speed = Dimension(length=1, time=-1)`)
- `Prefix`, such as `milli` or `tera`
- `MeasureInfo`, used for extra display "comments"
- `Measure`, a subclass of `Generic[Real]`, which holds a `.value`, `.stddev` and `.dim`.
  - `Unit`, a named `Measure` used for display purposes.
    - `AffineUnit`, with a zero-point (useful for °C)
    - `ChainedUnit`, which handles `unit & unit` (eg `foot & inch`)
  - `MeasureRelative`, which handles `measure @ unit` (stored as `.unit`)
- `DisplaySet` (nominally `display`), which handles which unit should be used for display
- `Catalogue` (nominally `catalogue`), which collates every unit
