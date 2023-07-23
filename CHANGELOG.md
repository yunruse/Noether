# Noether changelog

## 1.0
***23 Jul 2023, [281 commits](https://github.com/yunruse/Noether/pull/53/commits), closing [23 issues](https://github.com/yunruse/Noether/milestone/3?closed=1)***

A *complete* rewrite from scratch. The original was made some 5 years ago, so this is definitely a 1.0 now :)

I wouldn't consider this yet to be amazing, feature-complete stable quality... but can that be said of any open source project?

Listing all the changes would be an effort itself! Here's the cliff notes:

- Core code rewritten *entirely* from scratch
  - `Measure` is now frozen and can take any `Real` value
  - `Measure.stddev` is `None` by default rather than zero
  - Almost entirely strong-typed with `pyright` and partially unit-tested
  - API designed for both ease of use and expressiveness

- Improved display mechanisms
  - You can use `measure @ unit` for quick display in that unit.
  - You can compose units with `&` for display purposes.
    - By default, for example, time is displayed in `year & day & hour & minute & second`
  - Support for `rich` API (automatic in `python -im noether`)

- Improved catalogue mechanism
  - New optional catalogue shorthand (in development) for quicker development
  - `Catalogue` holds everything for analysis
  - Collation and display easier with `UnitSet` – display e.g. `mile @ CGS`
  - `info` tag provides context, definition and disambiguation on units

- Extended catalogue
  - SI `ronto`, `quecto`, `ronna`, `quetta` prefixes
  - Some fictional and historical units
  - Some new scientific (astronomic) units
  - All CODATA constants direct from source

- Config handler changed to `toml`
  - Now loads from `${XDG_CONFIG_HOME:-~/.config}/noether.toml`.
  - Not created by default to avoid filespam
  - Presented in categories for user convenience

Some units were lost in the conversion, and I've kind of slowed down on my microfixation on obscure units.

Of course, I will add units as I get them, and any pull request to add more units is very appreciated.
