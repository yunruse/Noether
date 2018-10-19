'''Script that carries out file and/or REPL'''

import sys
import os
import argparse
import threading


from . import repl
from .language import Noether

from . import namespace as ns
ns = ns.__dict__
ns['__name__'] = '__main__'

def importer():
    '''Defer numpy-importing to cheekily look faster'''
    from . import graphing
    ns.update(graphing.__dict__)

def main(args):    
    doRepl = not (args.command or args.file)

    if doRepl:
        print('Noether 1.0.0\n')
        threading.Thread(target=importer).start()
    else:
        importer()

    if args.languageChange:
        exec = Noether.exec

    if args.command:
        exec(args.command, globals=ns)
    elif args.file:
        fname = os.path.join(os.getcwd(), args.file)
        if os.path.isfile(fname):
            with open(fname, encoding='utf8') as f:
                code = ''.join(f.readlines())
                exec(code, globals=ns)
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

parser.add_argument(
    '-s', dest='languageChange', action='store_false',
    help="suppress Noether's syntax changes")

main(parser.parse_args())
