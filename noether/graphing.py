"""Noether: module for ease-of-use graphing"""

# Used as namespace in Noether REPL:
# pylint: disable=F0401, W0611

import argparse
from collections import namedtuple
import sys

import numpy as np
import matplotlib  # noqa: F401
from matplotlib import pyplot as plt
import astley

from .matrix import Matrix, Vector  # noqa: F401
from . import namespace

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

# TODO: polar

def main(ns):
    if ns.axis is not None:
        axis = ns.axis
    else:
        axis = "y" if any("y" in e for e in ns.function) else "x"
    signature = astley.arguments([astley.arg(axis)])

    funcs = []
    for expression in ns.function:
        node = astley.parse(expression, mode='eval').body
        func = astley.Lambda(signature, node).eval(namespace.__dict__)
        func.__name__ = expression.replace('**', '^').replace('*', '·')
        funcs.append(func)

    title = 'noether.graphing ' + ' '.join(
        repr(i) if ' ' in i else i for i in sys.argv[1:]
    )

    plot_xy(
        np.linspace(ns.start, ns.end, ns.count), *funcs,
        axis=axis, jmin=ns.min, jmax=ns.max, axisLines=ns.axisLines,
        title=title
    )

parser = argparse.ArgumentParser(
    "noether.graphing", description="Noether quick f(x)/f(y) grapher"
)

parser.add_argument(
    "function", nargs="+", help="expression of x or y"
)

parser.add_argument(
    "--axis", type=str, default=None, help="input axis of functions"
)

parser.add_argument("--min", '-m', type=float, default=None)
parser.add_argument("--max", '-M', type=float, default=None)
parser.add_argument("--start", '-s', type=float, default=-6)
parser.add_argument("--end", '-e', type=float, default=6)
parser.add_argument("--count", '-n', type=float, default=2000)
parser.add_argument(
    "--noAxisLines", dest="axisLines", action="store_false")

if __name__ == '__main__':
    main(parser.parse_args())
