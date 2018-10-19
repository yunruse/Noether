import sys
import types
import functools

#% Function analysis

def analyse(f):
    print('f.__defaults__', f.__defaults__)
    print('f.__kwdefaults__', f.__kwdefaults__)
    c = f.__code__
    for i in dir(c):
        if '__' in i:
            continue
        print(i, getattr(c, i))

func_like = (
    types.FunctionType,
    types.BuiltinFunctionType, types.BuiltinMethodType,
    types.MethodType, types.MethodWrapperType, types.MethodDescriptorType,
    types.WrapperDescriptorType,
    types.ClassMethodDescriptorType,
    )

def repr_function(f):
    '''Describe function input in a helpful manner'''
    
    if isinstance(f, func_like) and not isinstance(f, types.FunctionType):
        name = 'builtin ' + f.__name__
        
        textsig = getattr(f, '__text_signature__', None)
        if textsig:
            for i in ('$self, ', '$module, ', ', /'):
                textsig = textsig.replace(i, '')
            name += textsig
        else:
            name += ':'
        
        doc = (getattr(f, '__doc__', None) or '').split('\n\n')[0]
        return name + '\n' + doc

    elif not isinstance(f, types.FunctionType):
        raise TypeError('f must be function or function-like')

    # check for already-modified repr
    if '<' not in repr(f):
        return repr(f)
    
    c = f.__code__
    n = c.co_argcount
    n_k = c.co_kwonlyargcount
    
    hasKwargs = (c.co_flags & 0b0001000) >> 3
    hasArgs = (c.co_flags & 0b0000100) >> 2
    
    args_var = c.co_varnames[n+1] if hasArgs else None
    kwargs_var = c.co_varnames[n+1+hasArgs] if hasKwargs else None

    args = []
    defaults = f.__defaults__ or tuple()

    n_required = n - len(defaults)
    
    def argify(variables, isKwargsOnly):
        for i, a in enumerate(variables):

            isKeyword = bool(len(defaults))

            # for some reason Python places untoward attention
            # to the '*args' separation, giving the defaults
            # different locations. how odd!
            
            if isKwargsOnly:
                default = f.__kwdefaults__.get(a, '')
            elif defaults:
                # __defaults__ applies to the tail of the variables
                dindex = i - n_required
                if dindex < 0:
                    default = None
                    isKeyword = False
                else:
                    default = f.__defaults__[dindex]
            
            typ = f.__annotations__.get(a, object).__name__
            annotated = typ != 'object'

            if annotated and isKeyword:
                args.append('{}: {} = {}'.format(a, typ, default))
            elif annotated:
                args.append('{}: {}'.format(a, typ))
            elif isKeyword:
                args.append('{}={}'.format(a, default))
            else:
                args.append(a)

    argify(c.co_varnames[:n], False)
    
    if args_var:
        args.append('*' + args_var)
        argify(c.co_varnames[n:n+n_k], True)

    if kwargs_var:
        args.append('**' + kwargs_var)

    args = ', '.join(args)
    returned = f.__annotations__.get('return', object).__name__

    name = c.co_name
    if name == '<lambda>':
        name = 'f'
    
    if returned == 'object':
        return '{}({})'.format(name, args)
    
    else:
        return '{}({}) -> {}'.format(name, args, returned)

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
            if val is None:
                pass
            
            elif isinstance(val, func_like):
                print(repr_function(val))
                print()
            
            else:
                print(repr(val))
            
        else:
            lines = '\n'.join(lines)
            exec(lines, _globals, _locals)
        
    except KeyboardInterrupt:
        pass
    except Exception as e:
        _globals['_e'] = e
        print(e, file=sys.stderr)

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
            print()
            continue
        
        if isinstance(exitVal.value, Exception):
            # user wishes to view traceback
            raise exitVal.value
        
        return (exitVal.value, _globals, _locals)
