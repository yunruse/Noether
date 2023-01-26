class NoetherError(Exception):
    '''
    Common error used in Noether.
    '''


class DimensionError(NoetherError):
    '''
    Dimensions do not match.
    '''


class IncompatibleUnitError(NoetherError):
    '''
    Units of different types are incompatible.
    '''
