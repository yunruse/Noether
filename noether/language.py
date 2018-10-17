import ast
from ast import PyCF_ONLY_AST

class Language(ast.NodeTransformer):

    def __init__(self, mode, tree, globals=None, locals=None):
        self.mode = mode
        self.tree = tree
        self.globals = globals or dict()
        self.locals = locals or dict()

    @classmethod
    def parse(cls, source, filename='<unknown>', mode='exec', globals=None, locals=None):
        tree = compile(source, filename, mode, flags=PyCF_ONLY_AST)
        return cls(mode, tree, globals, locals).visit(tree)

    @classmethod
    def _process(cls, f, code, g, l):
        gl = g or globals(), l or locals()
        nm = f'<{cls.__name__}>', f.__name__
        tree = cls.parse(code, *nm, *gl)
        binary = compile(tree, *nm)
        return f(binary, *gl)
    
    @classmethod
    def eval(cls, code, globals=None, locals=None):
        return cls._process(eval, code, globals, locals)
    
    @classmethod
    def exec(cls, code, globals=None, locals=None):
        cls._process(exec, code, globals, locals)
