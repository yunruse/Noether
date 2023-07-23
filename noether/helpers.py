'''
Helpful standalone functions.
'''

from fractions import Fraction
import os
import pathlib
from typing import Generic, TypeVar


# Typing does not currently support
# numbers.Rational etc
Rational = int | Fraction
Real = Rational | float
MeasureValue = Real


# % String methods


def removeprefix(string: str, prefix: str):
    if string.startswith(prefix):
        return string[len(prefix):]
    return string


def removesuffix(string: str, suffix: str):
    if string.endswith(suffix):
        return string[:-len(suffix)]
    return string


def scanline(string: str, lengths: list[int]) -> list[str]:
    "Divide column-indented strings"
    chunks = []
    for N in lengths:
        chunks.append(string[:N].strip())
        string = string[N:]
    return chunks + [string.strip()]


# % Dictionary methods


KT = TypeVar('KT')
VT = TypeVar('VT')


class ImmutableDict(Generic[KT, VT], dict[KT, VT]):
    def __setitem__(self, _k: KT, _v: VT):
        raise AttributeError(
            '{!r} object does not support item assignment'.format(type(self).__name__))

    def __delitem__(self, _):
        raise AttributeError(
            '{!r} object does not support item deletion'.format(type(self).__name__))


def reorder_dict_by_values(dictionary: dict):
    kv = list(dictionary.items())
    kv.sort(key=lambda kv: kv[1])

    dictionary.clear()
    for k, v in kv:
        dictionary[k] = v


# % Pathing


def get_dot_config():
    return pathlib.Path(
        os.path.expanduser(
            os.environ.get(
                'XDG_CONFIG_HOME', '~/.config')))
