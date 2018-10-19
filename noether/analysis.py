import types

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


def repr_mod(obj):
    '''Return useful representation of an object.'''
    if isinstance(obj, func_like):
        return repr_function(obj)
    
    else:
        return repr(obj)