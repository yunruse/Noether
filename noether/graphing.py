"""Noether: module for ease-of-use graphing"""

# Used as namespace in Noether REPL:
# pylint: disable=F0401, W0611

from collections import namedtuple

import numpy as np
import matplotlib  # noqa: F401
from matplotlib import pyplot as plt

from .matrix import Matrix, Vector  # noqa: F401

__all__ = """\
np matplotlib plt Vector Matrix \
plot_y plot_x""".split()


def has_asymptote(a):
    """Heuristic to determine if an array has a (vertical) asymptote."""
    return np.std(a[1:] - a[:-1]) > np.std(a)


_gr = namedtuple("GraphResult", "data label hasAsymptote")
def GraphResult(data, domain, hasInputSpace):
    label = getattr(data, "__name__", None)
    if label == '<lambda>':
        label = None
    if callable(data):
        data = np.vectorize(data)(domain)
    elif not hasInputSpace:
        raise ValueError("Cannot plot output array without a domain")

    asym = has_asymptote(data)
    minMax = (0, 0) if asym else (min(data), max(data))
    return _gr(data, label, asym)


def plot_xy(*funcs, axis="x", jmin=None, jmax=None, axisLines=True, title=None):
    """Plot a variable amount of functions or data in Cartesian space.

    If the first value provided is an array, it will be consumed as the
    domain.
    Provide startj and endj to manually control the limit of the output axis."""

    hasInputSpace = funcs and isinstance(funcs[0], np.ndarray)

    if hasInputSpace:
        x, *funcs = funcs
    else:
        x = np.linspace(-6, 6, 2000)

    results = [GraphResult(f, x, hasInputSpace) for f in funcs]

    fig, axes = plt.subplots()

    xlim = min(x), max(x)
    if not (jmin and jmax):
        jmin = min(0 if k.hasAsymptote else min(k.data) for k in results)
        jmax = max(0 if k.hasAsymptote else max(k.data) for k in results)
        asym = any(k.hasAsymptote for k in results)
        reach = 1.5 if asym else 1.1
        c, d = (jmax + jmin) / 2, (jmax - jmin) / 2
        jmin = c - (d * reach)
        jmax = c + (d * reach)
        if asym:
            jmin = min(jmin, -6)
            jmax = max(jmax, 6)

    ylim = jmin, jmax

    if axis == "y":
        xlim, ylim = ylim, xlim
    axes.set_xlim(*xlim)
    axes.set_ylim(*ylim)

    if axisLines:
        inf = 1e17
        axes.plot([-inf, inf], [0, 0], "gray", lw=0.5)
        axes.plot([0, 0], [-inf, inf], "gray", lw=0.5)

    for k in results:
        y = k.data
        if axis == "y":
            x, y = y, x
        axes.plot(x, y, label=k.label)

    if title:
        axes.set_title(title)

    if len(funcs) > 1:
        plt.legend()
    elif not title and hasattr(funcs[0], '__name__'):
        axes.set_title(funcs[0].__name__)

    plt.show()
    return fig, axes


# TODO: set nice limit detection for functions with asymptotes

# TODO: polar
