import numpy as np
import matplotlib
from matplotlib import pyplot as plt

from .matrix import Matrix, Vector

__all__ = '''\
np matplotlib plt Vector Matrix \
plot_y plot_x'''.split()

def _plot_xy(*funcs, starti=-6, endi=6, axis='x', n=2000, startj=None, endj=None):

    i = np.linspace(starti, endi, n)
    js = [(f, np.vectorize(f)(i)) for f in funcs]
    
    startj = startj or min(min(j) for f, j in js)
    endj = endj or max(max(j) for f, j in js)
    
    fig, axes = plt.subplots()
    
    if startj and endj:
        if axis == 'y':
            axes.set_xlim(startj, endj)
        else:
            axes.set_ylim(startj, endj)
    
    xlim = (starti, endi)
    ylim = (startj, endj)
    if axis == 'y':
        xlim, ylim = ylim, xlim
    
    axes.plot(xlim, [0, 0], 'gray', lw=0.5)
    axes.plot([0, 0], ylim, 'gray', lw=0.5)
    
    for f, j in js:
        if axis == 'y':
            axes.plot(j, i, label=f.__name__)
        else:
            axes.plot(i, j, label=f.__name__)
            
    if len(funcs) > 1:
        plt.legend()
    plt.show()
    return fig, axes

def plot_y(*funcs, startx=-6, endx=+6, n=2000, starty=None, endy=None):
    return _plot_xy(
        *funcs, axis='x', n=n,
        starti=startx, endi=endx, startj=starty, endj=endy)

def plot_x(*funcs, starty=-6, endy=+6, n=2000, startx=None, endx=None):
    return _plot_xy(
        *funcs, axis='y', n=n,
        starti=starty, endi=endy, startj=startx, endj=endx)

# TODO: set nice limit detection for functions with asymptotes

# TODO: polar
