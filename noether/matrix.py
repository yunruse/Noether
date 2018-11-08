"""Noether: Useful numpy bindings"""

import math

import numpy as np

from .helpers import product


class Matrix(np.ndarray):
    """2-dimensional matrix or vector with useful operators.

    Create with & then | operators, eg:
    lorentz = gamma * (1 & -beta | -beta & 1)

    This works natively on Unit and other Matrix objects,
    and with floats via Noether's syntax. Normal operations
    works on ints, however."""

    __slots__ = "dim".split()

    def _shape(self):
        if len(self.shape) == 2:
            return self.shape
        elif len(self.shape) == 1:
            return (*self.shape, 1)
        else:
            raise ValueError("Only up-to-2d arrays are supported!")

    def __or__(self, other):
        rows, cols = self._shape()
        if isinstance(other, np.ndarray):
            new = np.append(self, other, axis=0)
        else:
            row = [other] + [None] * (cols - 1)
            new = np.append(self, row).reshape(rows + 1, cols)
        return new.view(Matrix)

    def __and__(self, other):
        rows, cols = self._shape()
        if isinstance(other, np.ndarray):
            new = np.append(self, other, axis=1)
        elif None in self:
            i, j = list(zip(*np.where(self is None)))[0]
            new = self.copy()
            new[i, j] = other
        else:
            col = [other] + [None] * (rows - 1)
            new = np.append(self, col).reshape(rows, cols + 1)
        return new.view(Matrix)

    def __new__(cls, *x, shape=None, dtype=None, shapeToSquare=True):
        """Return a matrix or vector."""
        if len(x) == 1 and hasattr(x[0], "__iter__"):
            x = x[0]

        v = np.array(x, dtype=dtype).view(type=cls)
        n = len(v)

        if shape:
            unknowns = shape.count(...)
            if unknowns == 1:
                rem = len(x) // product(i for i in shape if i != ...)
                shape = tuple(rem if i == ... else i for i in shape)

            elif unknowns > 1:
                raise ValueError("More than one unknown in length")

            return v.reshape(shape)

        if shapeToSquare and len(v.shape) == 1:
            # not already shaped: attempt to match square matrix
            a = math.sqrt(n)
            b = int(a)
            if a == b:
                return v.reshape((b, b))

        return v


def Vector(*x, shape=None, dtype=None):
    return Matrix(*x, shape=shape, dtype=dtype, shapeToSquare=False)
