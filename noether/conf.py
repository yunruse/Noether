
import os
import toml

from collections import namedtuple

ConfigEntry = namedtuple("ConfigEntry", "name kind default description".split())

CONF_DIR = os.path.expanduser('~/.config/noether')
os.makedirs(CONF_DIR, exist_ok=True)
conf_new = not os.path.isdir(CONF_DIR)

def process_path(path):
    if not os.path.isabs(path):
        path = os.path.join(CONF_DIR, path)
    return path

class Config(dict):
    __slots__ = ("info", "dirty")
    def __init__(self):
        dict.__init__(self)
        object.__setattr__(self, "info", {})
        object.__setattr__(self, "dirty", False)
    
    def register(self, name, kind=object, default=None, description=None):
        """
        Register a config variable.
        """
        self.info[name] = ConfigEntry(name, kind, default, description)
        self[name] = default

    def __repr__(self):
        s = "Noether config:\n"
        names = list(sorted(self.keys()))
        longest = max(map(len, names))
        for name in names:
            s += f" - {name.ljust(longest)}: {repr(self[name])}\n"
        return s.strip()
    
    def __contains__(self, name):
        return name in self.info
    
    def __getattr__(self, name):
        try:
            return dict.__getitem__(self, name)
        except NameError:
            return self.info[name].default
    
    def __setattr__(self, name, value):
        dict.__setitem__(self, name, value)
        object.__setattr__(self, "dirty", True)
    
    def __delattr__(self, name):
        dict.__setitem__(self, name, self.info[name].default)
        object.__setattr__(self, "dirty", True)
    
    def save(self, path="default.conf", rich=False):
        """Save the current config"""
        with open(process_path(path), "w") as f:
            toml.dump(self, f)
        object.__setattr__(self, "dirty", False)

    def load(self, path="default.conf"):
        self.clear()
        with open(process_path(path)) as f:
            self.update(toml.load(f))
        object.__setattr__(self, "dirty", False)

conf = Config()