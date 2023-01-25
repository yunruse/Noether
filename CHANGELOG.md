# 1.0
- Unit testing added.

- Improved display mechanisms
    - You can use `measure @ unit` for quick display in that unit.
    - You can chain units with `&`. By default (`conf.human_time`), for example, time is displayed in `year & day & hour & minute & second`.
    - Support for `rich` API (automatic in `python -im noether`)

- Expanded catalogue
    - More obscure, regional and historic units added
    - `catalogue_extended` can be disabled to bypass historical units for speedup

- Core code rewritten entirely from scratch
    - `Measure` is now frozen, and is generic to its underlying value, which can be any `Real` subclass. `Measure.cast(T)` can be used to cast to a type.
    - `Measure.stddev` is `None` by default rather than zero.

- Config handler changed to `toml`.
    - Now loads from `${XDG_CONFIG_HOME:-~/.config}/noether/default.toml`.
    - Does not automatically create a config file to avoid filespam.
    - `measure_compare_uncertainty` is now disabled by default.
    - `display_repr_code` will use a more Pythonic `repr` showing how to generate an object.