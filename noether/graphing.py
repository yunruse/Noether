"""Noether: module for ease-of-use graphing"""

# Used as namespace in Noether REPL
# pylint: disable=F0401, W0611

import numpy as np
import matplotlib  # noqa: F401
from matplotlib import pyplot as plt

from .matrix import Matrix, Vector  # noqa: F401

__all__ = """\
np matplotlib plt Vector Matrix \
plot_y plot_x""".split()


def plot_xy(linspace, *funcs, axis="x", startj=None, endj=None, axisLines=True):
    """Plot a variable amount of functions or data in Cartesian space.

    If provided with data, ensure it maps correctly to the domain given.
    Provide startj and endj to control the limit of the axes."""

    funcs = [np.vectorize(f) for f in funcs if callable(f)]

    j_results = [(f, f(linspace)) if callable(f) else (None, f) for f in funcs]

    startj = startj or min(min(j) for f, j in j_results)
    endj = endj or max(max(j) for f, j in j_results)

    fig, axes = plt.subplots()

    if startj and endj:
        if axis == "y":
            axes.set_xlim(startj, endj)
        else:
            axes.set_ylim(startj, endj)

    xlim = (min(range), max(range))
    ylim = (startj, endj)
    if axis == "y":
        xlim, ylim = ylim, xlim

    if axisLines:
        axes.plot(xlim, [0, 0], "gray", lw=0.5)
        axes.plot([0, 0], ylim, "gray", lw=0.5)

    for f, j in j_results:
        x, y = linspace, j
        if callable(f):
            label = f.__name__
        else:
            label = None

        if axis == "y":
            x, y = y, x
        axes.plot(x, y, label=label)

    if len(funcs) > 1:
        plt.legend()
    plt.show()
    return fig, axes


# TODO: set nice limit detection for functions with asymptotes

# TODO: polar
