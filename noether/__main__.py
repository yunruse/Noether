import sys
import os
import argparse

from . import namespace
from . import repl
from .language import Noether


def main(args):
    
    ns = dict(namespace.__dict__)
    ns['__name__'] = '__main__'

    doRepl = not (args.command or args.file)

    if doRepl:
        print('Noether\n')

    if args.command:
        Noether.exec(args.command, globals=ns)
    elif args.file:
        fname = os.path.join(os.getcwd(), args.file)
        if os.path.isfile(fname):
            with open(fname, encoding='utf8') as f:
                code = ''.join(f.readlines())
                Noether.exec(code, globals=ns)
    else:
        interactive = True
    
    if doRepl or args.interactive:
        repl.repl(ns)


parser = argparse.ArgumentParser(
    description='Python Physics REPL',
)

parser.add_argument(
    'file', nargs='?',
    help='File to execute.')

parser.add_argument(
    '-c', dest='command', type=str, default='',
    help='program passed in as string')

parser.add_argument(
    '-i', dest='interactive', action='store_true',
    help='enter REPL if given commands')
main(parser.parse_args())
