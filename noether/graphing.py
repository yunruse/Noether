"""
Noether (+matplotlib): easy graphing
"""

import argparse
from collections import namedtuple
import sys

import numpy as np
import matplotlib  # noqa: F401
from matplotlib import animation, pyplot as plt

from .matrix import Matrix, Vector  # noqa: F401
import noether

__all__ = """\
np matplotlib plt Vector Matrix \
plot""".split()


def limit_heuristic(a):
    """Heuristic to determine if an array has a plottable limit."""
    return np.std(a[1:] - a[:-1]) < np.std(a)


_gr = namedtuple("GraphResult", "data label hasLimits isTimeFunc")


def GraphResult(data, domain, hasInputSpace):
    label = getattr(data, "__name__", None)
    if label == '<lambda>':
        label = None

    isTimeFunc = False
    if callable(data):
        try:
            data(1)
            data = data(domain)
        except TypeError:
            data(1, 2)  # Functions should be one or two arguments
            isTimeFunc = True

    elif not hasInputSpace:
        raise ValueError("Cannot plot function without input domain")

    hasLimits = not isTimeFunc and limit_heuristic(data)
    return _gr(data, label, hasLimits, isTimeFunc)


class Animation:
    line_args = [
        dict(lw=2),
    ]

    def animate(self, fig=None, axes=None, frames=10_000, blit=False, repeat=True):
        if fig is None and axes is None:
            fig, axes = plt.subplots()

        self.frames = frames

        self.fig = fig
        self.axes = axes
        self.lines = tuple(axes.plot([], [], **kw)[0] for kw in self.line_args)

        self.anim = animation.FuncAnimation(
            fig, frames=self.data,
            func=(lambda data: self.onFrame(data) or self.lines),
            init_func=(lambda: self.onStart() or self.lines),
            blit=blit, repeat=repeat, interval=1
        )

        return self

    lines = tuple()
    axes = None
    fig = None
    anim = None

    def onStart(self):
        pass

    def data(self, t=0):
        for frame in range(self.frames):
            t += 1
            yield t

    def onFrame(self, data):
        return self.lines


def plot(
    *funcs, axis="x", jmin=None, jmax=None,
    axisLines=True, title=None,
    dt=0.01, frames=10_000
):
    """Plot a variable amount of functions or data in Cartesian space.

    If the first value provided is an array, it will be consumed as the
    domain.
    Provide startj and endj to manually control the limit of the output axis."""

    hasInputSpace = funcs and isinstance(funcs[0], np.ndarray)

    if hasInputSpace:
        x, *funcs = funcs
    else:
        x = np.linspace(-6, 6, 2000)

    dynamics, bounded, unbounded = [], [], []
    for f in funcs:
        g = GraphResult(f, x, hasInputSpace)
        l = dynamics if g.isTimeFunc else bounded if g.hasLimits else unbounded
        l.append(g)

    fig, axes = plt.subplots()

    if title:
        axes.set_title(title)

    if len(funcs) > 1:
        plt.legend()
    elif not title and hasattr(funcs[0], '__name__'):
        axes.set_title(funcs[0].__name__)

    # Determine range if not provided

    xlim = min(x), max(x)
    if not bounded:
        jmin = jmin or -6
        jmax = jmax or 6

    elif not (jmin and jmax):
        mins, maxs = zip(*[
            (min(k.data), max(k.data)) for k in bounded if k.hasLimits
        ])
        jmin, jmax = min(mins), max(maxs)
        reach = 1.1 if unbounded else 1.5
        c, d = (jmax + jmin) / 2, (jmax - jmin) / 2
        jmin = c - (d * reach)
        jmax = c + (d * reach)

    ylim = jmin, jmax

    if axis == "y":
        xlim, ylim = ylim, xlim
    axes.set_xlim(*xlim)
    axes.set_ylim(*ylim)

    if axisLines:
        inf = 1e17
        axes.plot([-inf, inf], [0, 0], "gray", lw=0.5)
        axes.plot([0, 0], [-inf, inf], "gray", lw=0.5)

    for k in bounded + unbounded:
        y = k.data
        if axis == "y":
            x, y = y, x
        axes.plot(x, y, label=k.label)

    if dynamics:
        class newAnim(Animation):
            line_args = [{}] * len(dynamics)

            def data(self, t=0):
                for i in range(frames):
                    t += dt
                    yield t

            def onFrame(self, t):
                for line, k in zip(self.lines, dynamics):
                    f_t = np.vectorize(lambda x: k.data(x, t))
                    if axis == 'x':
                        line.set_data(x, f_t(x))
                    else:
                        line.set_data(f_t(x), x)

        anim = newAnim().animate(fig, axes, frames=10_000, blit=True, repeat=True)
    else:
        anim = None

    plt.show()
    return fig, axes, anim

# TODO: polar


def main(ns):
    import astley

    if ns.axis is not None:
        axis = ns.axis
    else:
        axis = "y" if any("y" in e for e in ns.function) else "x"
    signature = astley.arguments([astley.arg(axis)])

    funcs = []
    for expression in ns.function:
        node = astley.parse(expression, mode='eval').body
        func = astley.Lambda(signature, node).eval(noether.__dict__)
        func.__name__ = expression.replace('**', '^').replace('*', '·')
        funcs.append(func)

    title = 'noether.graphing ' + ' '.join(
        repr(i) if ' ' in i else i for i in sys.argv[1:]
    )

    plot(
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
