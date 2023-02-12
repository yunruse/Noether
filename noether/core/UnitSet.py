'''
List of units used for display purposes.

Also handles dimension names.
'''

from .Unit import Unit


class UnitSet(set[Unit]):
    '''
    set[Unit] with convenience functions.
    '''

    def __init__(self, *iterable: 'Unit | UnitSet'):
        super().__init__()
        for x in iterable:
            if isinstance(x, Unit):
                self.add(x)
            else:
                self |= x

    def add(self, value: Unit) -> Unit:
        super().add(value)
        return value

    __call__ = add
