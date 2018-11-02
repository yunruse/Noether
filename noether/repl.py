'''Noether: Read-Eval-Print loop and tools'''

import sys
import functools
import linecache

from astley import Python

from .repr import repr_mod, repr_exception

def defaultInput(prompt='', default=''):
    ret = input(prompt + default + chr(8) * len(default))
    return ret or default

def get_input(ps1='>>> ', ps2='... '):
    indent = 0
    lines = []
    while True:
        line = input((ps2 if lines else ps1) + '  • ' *indent).strip()
        
        if line:
            lines.append(' ' * 4 * indent + line)
        else:
            indent -= 1
        
        if line.endswith(':'):
            indent += 1
        elif len(lines) == 1 and not line.endswith('\\'):
            break
        
        if indent < 0:
            break
    
    return lines

def push_history(ns, val):
    h = '__history__'
    hist = ns.get(h, [])
    hist.append(val)
    ns[h] = hist
    for i in range(1, min(10, len(hist))+1):
        token = '_' + str(i) * (i!=1) #_, _2, _3
        ns[token] = ns[h][-i]

#% REPL loops

def rep(lang, n, globals_, locals_):
    try:
        lines = get_input()
    except KeyboardInterrupt:
        print(' <KeyboardInterrupt>')
        return
    source = '\n'.join(lines)
    filename = '<Noether#{}>'.format(n)
    chars = len('\n'.join(lines)) + 1
    linecache.cache[filename] = chars, 0, lines, filename
    
    try:
        code = lang(
            source, filename=filename, globals=globals_, locals=locals_)
    except SyntaxError as e:
        globals_['_e'] = e
        print(repr_exception(e))
        return
    
    try:
        if code.mode == 'eval':
            val = code.eval()
            if isinstance(val, ExitValue):
                return val
            
            push_history(globals_, val)
            if val is not None:
                print(repr_mod(val))
            
        else:
            code.exec()
        
    except KeyboardInterrupt:
        pass
    except Exception as e:
        globals_['_e'] = e
        print(repr_exception(e), file=sys.stderr)

# exit magic to pass through
class ExitValue():
    __slots__ = 'value'.split()
    
    @functools.wraps(exit)
    def __init__(self, value=0):
        self.value = value

def repl(lang=Python, **kw):
    globals_ = kw.get('globals', globals())
    locals_ = kw.get('locals', dict())
    locals_['exit'] = ExitValue
    
    n = 0
    while True:
        n += 1
        exitVal = rep(
            lang, n, globals_, locals_)
        if exitVal is None:
            continue
        
        if isinstance(exitVal.value, Exception):
            # user wishes to view traceback
            raise exitVal.value
        
        return (exitVal.value, globals_, locals_)
