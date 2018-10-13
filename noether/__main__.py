from . import physics
from . import repl

def main():
    print('Noether\n')
    ns = dict(physics.__dict__)
    ns['__name__'] = '__main__'
    repl.repl(ns)

main()