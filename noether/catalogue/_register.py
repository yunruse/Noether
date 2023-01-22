from ..core import Dimension, Measure, Unit


def U(
    value: Measure,
    *symbols: list[str],
    display=False,
    **prefixes: dict[str, bool],
) -> Unit:
    unit = Unit(value)
    return unit
