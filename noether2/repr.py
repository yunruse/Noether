import traceback
import types
import astley

func_like = (
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodType,
    types.MethodWrapperType,
    types.MethodDescriptorType,
    types.WrapperDescriptorType,
    types.ClassMethodDescriptorType,
)


def repr_function(f):
    """Describe function input in a helpful manner"""

    if hasattr(f, "____noetherRepr"):
        return f.____noetherRepr

    if isinstance(f, func_like) and not isinstance(f, types.FunctionType):
        name = "builtin " + f.__name__

        textsig = getattr(f, "__text_signature__", None)
        if textsig:
            for i in ("$self, ", "$module, ", ", /"):
                textsig = textsig.replace(i, "")
            name += textsig
        else:
            name += ":"

        doc = (getattr(f, "__doc__", None) or "").split("\n\n")[0]
        return name + "\n" + doc

    elif not isinstance(f, types.FunctionType):
        raise TypeError("f must be function or function-like")

    # check for already-modified repr
    if "<" not in repr(f):
        return repr(f)

    args = astley.funcSignature(f)
    returned = f.__annotations__.get("return", object).__name__

    name = f.__name__
    if name == "<lambda>":
        name = "f"

    if returned == "object":
        return "{}({})".format(name, args)

    else:
        return "{}({}) -> {}".format(name, args, returned)


def repr_exception(err):
    return "".join(traceback.format_exception(type(err), err, err.__traceback__))


def repr_mod(obj):
    """Return useful representation of an object."""
    if isinstance(obj, func_like):
        return repr_function(obj)
    elif isinstance(obj, Exception):
        return repr_exception(obj)
    else:
        return repr(obj)
