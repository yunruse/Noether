'''Noether: Read-Eval-Print loop and tools'''

import sys
import functools

from .analysis import repr_mod, repr_exception

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

def rep(_globals, _locals, eval=eval, exec=exec):
    try:
        lines = get_input()

        wasEvaluated = False
        # do parse magic FIRST so you can raise Syntax error nicely
        if len(lines) == 1:
            try:
                val = eval(lines[0], _globals, _locals)
                wasEvaluated = True
            except SyntaxError:
                pass

        if wasEvaluated:
            if isinstance(val, ExitValue):
                return val
            
            push_history(_globals, val)
            if val is not None:
                print(repr_mod(val))
            
        else:
            lines = '\n'.join(lines)
            exec(lines, _globals, _locals)
        
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
    
    while True:
        exitVal = rep(_globals, _locals, eval, exec)
        if exitVal is None:
            continue
        
        if isinstance(exitVal.value, Exception):
            # user wishes to view traceback
            raise exitVal.value
        
        return (exitVal.value, _globals, _locals)
