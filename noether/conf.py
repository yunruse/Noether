
import os
import nestedtext as conf_provider

from collections import namedtuple
from warnings import warn

ConfigEntry = namedtuple(
    "ConfigEntry", "name type default description at_import".split())

CONF_DIR = os.path.expanduser('~/.config/noether')
conf_new = not os.path.exists(os.path.join(CONF_DIR, "default.conf"))
os.makedirs(CONF_DIR, exist_ok=True)


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

    def register(self, name, kind=object, default=None, description="", at_import=False):
        """
        Register a config variable.
        """
        self.info[name] = ConfigEntry(
            name, kind, default, description, at_import)
        self[name] = default

    def __repr__(self):
        s = "# Current noether config:\n"
        names = list(sorted(self.keys()))
        longest = max(map(len, names))
        for name in names:
            n = name + ':'
            s += f"{n.ljust(longest+1)} {repr(self[name])}\n"
        return s.strip()

    def __contains__(self, name):
        return name in self.info

    def __getattr__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            return self.info[name].default

    def __setattr__(self, name, value):
        typ = self.info[name].type
        if not isinstance(value, typ):
            raise TypeError(
                f"conf.{name} must be {typ.__name__}, not {type(value).__name__}")
        dict.__setitem__(self, name, value)
        object.__setattr__(self, "dirty", True)
        if self.info[name].at_import:
            msg = f"'{name}' is only evaluated when noether is imported; "
            msg += "do noe.conf.save() and sys.reload(noe) to see effects."
            warn(msg, RuntimeWarning, stacklevel=2)

    def __delattr__(self, name):
        dict.__setitem__(self, name, self.info[name].default)
        object.__setattr__(self, "dirty", True)

    def save(self, path="default.conf", rich=True):
        """
        Save the current config as a TOML file.

        If rich is kept as True, config descriptions are added as TOML comments.
        """
        s = ""
        # alphabetical sort important
        for name in sorted(self.info.keys()):
            # add comments hackily by tricking TOML with a dict
            desc = self.info[name].description
            if rich and desc:
                s += "\n"
                for l in desc.split('\n'):
                    s += f"# {l}\n"
            s += conf_provider.dumps({name: self[name]})
        with open(process_path(path), "w") as f:
            f.write(s)
        object.__setattr__(self, "dirty", False)

    def load(self, path="default.conf"):
        self.clear()
        with open(process_path(path)) as f:
            config = conf_provider.load(f)
            if config is not None:
                self.update(config)
        object.__setattr__(self, "dirty", False)


conf = Config()
if not conf_new:
    conf.load()
