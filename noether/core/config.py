'''
TOML configuration.
'''

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any, Optional
import tomllib

from ..helpers import get_dot_config

CONF_DIR = get_dot_config() / 'noether'
CONF_FILE = CONF_DIR / 'default.toml'


@dataclass
class ConfigOption:
    name: str
    default: Any
    type: type
    help: str = ""


def ConfigProperty(option: ConfigOption):
    def getter(self):
        if option.name in self:
            return self[option.name]
        return option.default

    def setter(self, value):
        typ = option.type
        if not isinstance(value, typ):
            raise TypeError(
                f"conf.{option.name} must be {option.type.__name__},"
                f" not {type(value).__name__}")
        self[option.name] = value

    def deleter(self):
        if option.name in self:
            del self[option.name]
    return property(getter, setter, deleter)


class Config(dict):
    info: dict[str, ConfigOption] = dict()

    @classmethod
    def register(
        cls,
        key: str,
        default,
        help="",
        typ: Optional[type] = None,
    ):
        option = ConfigOption(
            key, default,
            typ or type(default), help
        )
        cls.info[key] = option
        setattr(cls, key, ConfigProperty(option))

    def __init__(
        self,
        value: Optional[dict] = None,
        **kwargs,
    ):
        result = {
            k: v.default
            for k, v in self.info.items()}
        result.update(value or {})
        result.update(kwargs)
        super().__init__(result)

    def __repr__(self):
        return 'Config({})'.format(', '.join(
            f'{k}={v}' for k, v in self.items()
            if v != self.info[k].default
        ))

    def get_defaults(self):
        for k in self.info:
            self.setdefault(k, self.info[k].default)

    def reset(self):
        for k in self.info:
            self[k] = self.info[k].default

    # % Attributes

    def get(self, key: str):
        if key in self:
            return self[key]
        elif key in self.info:
            return self.info[key].default
        else:
            raise KeyError('Unknown config key', key)

    # % IO

    def __str__(self):
        self.get_defaults()

        string = ""
        for k, v in sorted(self.items()):
            desc = self.info[k].help.strip()
            if help:
                string += "\n\n"
                for l in desc.split('\n'):
                    string += f'# {l}\n'
            v = json.dumps(v)
            string += f'{k} = {v}'

        return string.strip()

    def save(self, path: Path = CONF_FILE, help=True):
        os.makedirs(path.parent, exist_ok=True)
        with open(path, 'w') as f:
            f.write(str(self))

    def load(self, path: Path = CONF_FILE):
        with open(path, 'rb') as f:
            new = tomllib.load(f)
            self.update(new)


conf = Config()
if CONF_FILE.is_file():
    conf.load(CONF_FILE)
