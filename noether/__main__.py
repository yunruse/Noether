"""Script that carries out file and/or REPL"""

import os
import argparse
import threading

from astley import Python

from . import repl
from .language import Noether

import noether

def test():
    from unittest import TextTestRunner

    os.sys.path.append(os.path.abspath(".."))
    from ..tests import suite

    TextTestRunner(verbosity=1).run(suite)


def main(args):
    doRepl = not (args.command or args.file or args.doTest)

    if doRepl:
        print("Noether (dev)\n")

    lang = Noether if args.languageChange else Python
    ns = noether.__dict__
    ns.update(
        dict(exec=lang.staticExec, eval=lang.staticEval, compile=lang.staticCompile)
    )

    if args.doTest:
        test()

    if args.command:
        lang.staticExec(args.command, globals=ns)
    elif args.file:
        fname = os.path.join(os.getcwd(), args.file)
        if os.path.isfile(fname):
            with open(fname, encoding="utf8") as f:
                code = "".join(f.readlines())
                lang.staticExec(code, globals=ns)

    if doRepl or args.interactive:
        repl.repl(lang, globals=ns, locals=dict())


parser = argparse.ArgumentParser(description="Python Physics REPL")

parser.add_argument("file", nargs="?", help="File to execute.")

parser.add_argument(
    "-c", dest="command", type=str, default="", help="program passed in as string"
)

parser.add_argument(
    "-i", dest="interactive", action="store_true", help="enter REPL if given commands"
)

parser.add_argument(
    "-s",
    dest="languageChange",
    action="store_false",
    help="suppress Noether's syntax changes",
)

parser.add_argument("--test", dest="doTest", action="store_true", help="run unit tests")

main(parser.parse_args())
