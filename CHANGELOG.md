# 0.2
A complete rewrite from scratch.

- Improved display mechanisms
    - You can use `measure @ unit` for quick display in that unit.
    - You can chain units with `&`. By default (`conf.units_human_time`), for example, time is displayed in `year & day & hour & minute & second`.
    - Support for `rich` API (automatic in `python -im noether`)

- Improved catalogue
    - Includes new SI `ronto`, `quecto`, `ronna`, `quetta` prefixes
    - `catalogue_extended` can be disabled to bypass historical units for speedup
    - `catalogue.json` and `catalogue.toml` included for convenience

- Core code rewritten entirely from scratch
    - `Measure` is now frozen, and is generic to its underlying value, which can be any `Real` subclass. `Measure.cast(T)` can be used to cast to a type.
    - `Measure.stddev` is `None` by default rather than zero.
    - Improved unit testing

- Config handler changed to `toml`.
    - Now loads from `${XDG_CONFIG_HOME:-~/.config}/noether.toml`.
    - Not created by defualt to avoid filespam.
    - Presented in categories for user convenience.
    - `measure_compare_uncertainty` is now disabled by default.
    - `display_repr_code` will use a more Pythonic `repr` showing how to generate an object.