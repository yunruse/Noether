import sys
import os

from . import physics
from . import repl
from .language import Noether

def main(argv):
    print('Noether\n')
    
    ns = dict(physics.__dict__)
    
    if len(argv):
        fname = os.path.join(os.getcwd(), argv[0])
        if os.path.isfile(fname):
            with open(fname, encoding='utf8') as f:
                code = ''.join(f.readlines())
                Noether.exec(code, globals=ns)
    
    ns['__name__'] = '__main__'
    repl.repl(ns)

main(sys.argv[1:])
