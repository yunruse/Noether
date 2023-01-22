'''
ChainedUnit, allowing for the `&` operator to link units together.

Currently not in production.
'''

from .unit import Unit

DisplayUnit = Unit  # ? what was the intent here?


class ChainedUnit(DisplayUnit):
    """
    A chain of units, all of the same dimension.

    Instantiate by:
     -  `ChainedUnit(a, b, c, ...)`, where the "default unit" is a,
     -  `a & b & c &...`, where the "default unit" is the smallest.

    A ChainedUnit CAN be treated as a measure to be used numerically,
    and it will behave as the "default unit", though this is not
    recommended. It can be used to instantiate a measurement,
    or to display other units.
    """
    __slots__ = Unit.__slots__ + tuple()

    # a & b & c  =  (a & b) & c