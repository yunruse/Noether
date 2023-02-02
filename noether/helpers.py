'''
Helpful standalone functions.
'''

import os
import pathlib

# % String methods


def removeprefix(string: str, prefix: str):
    if string.startswith(prefix):
        return string[len(prefix):]


def removesuffix(string: str, suffix: str):
    if string.endswith(suffix):
        return string[:-len(suffix)]


def scanline(string: str, lengths: list[int]) -> list[str]:
    "Divide column-indented strings"
    chunks = []
    for N in lengths:
        chunks.append(string[:N].strip())
        string = string[N:]
    return chunks + [string.strip()]


# % Dictionary methods


class ImmutableDict(dict):
    def __setitem__(self, _k, _v):
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
