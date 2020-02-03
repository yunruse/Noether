'''
A quick pocket-calculator-like interpreter for Noether.

Launches quickly by making heavy imports (numpy, matplotlib) in the background.
'''

import noether
from noether import *

display = Unit.display

glob = dict(globals())
loc = dict(locals())

while True:
    # todo: multi-line
    # todo: lazy-load in shells
    inp = input('>>> ')
    try:
        print(eval(inp, glob, loc))
    except SyntaxError:
        exec(inp, glob, loc)
