from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.Dimension import Dimension


class NoetherWarning(UserWarning):
    'Common warning used in Noether.'


class ConfigWarning(NoetherWarning):
    'Warning when changing configuration.'


class NoetherError(Exception):
    'Common error used in Noether.'


class DimensionError(NoetherError):
    'Dimensions do not match.'

    args: 'tuple[Dimension, Dimension, str | None]'

    def __init__(self, dim1: 'Dimension', dim2: 'Dimension', message: str | None = None):
        super().__init__(dim1, dim2, message)

    @classmethod
    def check(cls, dim1: 'Dimension', dim2: 'Dimension', message: str | None = None):
        # ensure not dimensionless - those are usually okay
        if dim1 != dim2:
            raise cls(dim1, dim2, message)

    def __str__(self):
        dim1, dim2, msg = self.args
        message = f'Dimensions {dim1} and {dim2} do not match.'
        if msg is not None:
            message += ' ' + msg
        return message


class UnitError(NoetherError):
    'Problem with creating a unit.'


class IncompatibleUnitError(UnitError):
    'Units of different specialist types cannot be merged into a separate unit.'
