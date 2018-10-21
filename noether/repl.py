'''Noether: Read-Eval-Print loop and tools'''

import sys
import functools
import linecache

from .repr import repr_mod, repr_exception

#% I/O niceties
    
def get_input(ps1='>>> ', ps2='... '):
    indent = 0
    lines = []
    while True:
        line = input((ps2 if indent else ps1) + '   ' *indent).strip()
        
        if line:
            lines.append('   ' * indent + line)
        else:
            indent -= 1
        
        if line.endswith(':'):
            indent += 1

        if indent <= 0:
            break
    
    return lines

def push_history(namespace, val):
    hist = namespace.get('__history__', list())
    hist.append(val)
    namespace['__history__'] = hist
    for i in range(min(10, len(hist))):
        # needs fixin'
        token = '_' + str(i+1) * bool(i) #_, _2, _3
        namespace[token] = hist[-i]

#% REPL loops

def rep(n, _globals, _locals, eval=eval, exec=exec):
    lines = get_input()
    source = '\n'.join(lines)
    filename = '<Noether#{}>'.format(n)
    chars = len('\n'.join(lines)) + 1
    linecache.cache[filename] = chars, 0, lines, filename
    
    doEval = True
    try:
        code = compile(source, filename, 'eval')
    except SyntaxError:
        doEval = False
        try:
            code = compile(source, filename, 'exec')
        except SyntaxError as e:
            _globals['_e'] = e
            print(''.join(traceback.format_exception(
                type(e), e, e.__traceback__)), file=sys.stderr)
            return
    
    try:
        if doEval:
            val = eval(code, _globals, _locals)
            if isinstance(val, ExitValue):
                return val
            
            push_history(_globals, val)
            if val is not None:
                print(repr_mod(val))
            
        else:
            exec(code, _globals, _locals)
        
    except KeyboardInterrupt:
        pass
    except Exception as e:
        _globals['_e'] = e
        print(repr_exception(e), file=sys.stderr)

# exit magic to pass through
class ExitValue():
    __slots__ = 'value'.split()
    
    @functools.wraps(exit)
    def __init__(self, value=0):
        self.value = value

def repl(_globals=None, _locals=None, eval=eval, exec=exec):
    _globals = _globals or globals()
    _locals = _locals or dict()
    _locals['exit'] = ExitValue
    
    n = 0
    while True:
        n += 1
        exitVal = rep(n, _globals, _locals, eval, exec)
        if exitVal is None:
            continue
        
        if isinstance(exitVal.value, Exception):
            # user wishes to view traceback
            raise exitVal.value
        
        return (exitVal.value, _globals, _locals)
