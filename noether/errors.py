class NoetherWarning(UserWarning):
    'Common warning used in Noether.'


class ConfigWarning(NoetherWarning):
    'Configuration will need extra action to apply.'


class NoetherError(Exception):
    'Common error used in Noether.'


class DimensionError(NoetherError):
    'Dimensions do not match.'


class IncompatibleUnitError(NoetherError):
    'Units of different types are incompatible.'
