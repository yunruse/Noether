from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import Dimension

class NoetherWarning(UserWarning):
    'Common warning used in Noether.'

class ConfigWarning(NoetherWarning):
    'Warning when changing configuration.'


class NoetherError(Exception):
    'Common error used in Noether.'


if True:
    from noether.config import Config, conf
OPENLINEAR = Config.register(
    "measure_open_linear", False,
    "Allow linear or display operation even between incompatible units (eg metre and kilogram). Cf .si_equality"
)

class DimensionError(NoetherError):
    'Dimensions do not match.'

    args: 'tuple[Dimension, Dimension]'

    def __init__(self, dim1: 'Dimension', dim2: 'Dimension'):
        super().__init__(dim1, dim2)

    @classmethod
    def check(cls, dim1: 'Dimension', dim2: 'Dimension'):
        if conf.get(OPENLINEAR):
            return
        if dim1 != dim2:
            raise cls(dim1, dim2)

    def __str__(self):
        d1, d2 = self.args
        return (
            f'Dimensions {d1} and {d2} do not match.'
            f" To do this in spite of ambiguity, enable {OPENLINEAR}."
        )


class UnitError(NoetherError):
    'Problem with creating a unit.'


class IncompatibleUnitError(UnitError):
    'Units of different specialist types cannot be merged into a separate unit.'
