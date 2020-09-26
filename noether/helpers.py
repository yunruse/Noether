"""Noether: general standalone math and repl niceties"""

import math
import os
import sys
import functools
import fractions

__all__ = "clear intify Fraction sqrt sign product tablify".split()

# display


def clear(isTerminal=True):
    if not isTerminal:
        print("\n" * 200)
    elif os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def bell():
    sys.stdout.write("\a")
    sys.stdout.flush()

# numerical


def intify(x):
    """Change to an int if it is equal to one."""
    i = int(x)
    return i if x == i else x


FLOATING_POINT_ERROR_ON_LOG_TENXPONENTS = 12


def exp_mantissa(num, base=10):
    """Returns e, m such that x = mb^e"""
    if num == 0:
        return 1, 0
    # avoid floating point error eg log(1e3, 10) = 2.99...
    exp = math.log(abs(num), base)
    exp = round(exp, FLOATING_POINT_ERROR_ON_LOG_TENXPONENTS)
    exp = math.floor(exp)  # 1 <= mantissa < 10
    mantissa = num / (base**exp)
    return exp, mantissa


Fraction = fractions.Fraction


@functools.wraps(math.sqrt)
def sqrt(x):
    # redefined to be nicer for certain expressions
    return x ** 0.5


def sign(x):
    """Return the mathematical sign of the particle."""
    if x.imag:
        return x / sqrt(x.imag ** 2 + x.real ** 2)
    return 0 if x == 0 else -1 if x < 0 else 1


def product(iterable, start=1):
    for i in iterable:
        start *= i
    return start


def tablify(table, sep=" "):
    table = [[str(i) for i in row] for row in table]
    lens = [0] * max(map(len, table))
    for row in table:
        for n, col in enumerate(row):
            lens[n] = max(lens[n], len(col))
    return (sep.join(c + " " * (l - len(c)) for c, l in zip(r, lens)) for r in table)
