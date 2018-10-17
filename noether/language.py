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

def printEquation(names, values):
    if not isinstance(names, tuple):
        names = (names, )
    if not isinstance(values, tuple):
        values = (values, )
    maxlen = max(map(len, names))
    for n, v in zip(names, values):
        spacing = ' ' * (maxlen-len(n))
        print('{}{} = {!r}'.format(n, spacing, v))

class Noether(Language):
    
    modified = True

    @classmethod
    def _process(cls, f, code, globals=None, locals=None):
        if cls.modified:
            return super()._process(f, code, globals, locals)
        else:
            return f(code, globals, locals)

    def visit_Assign(self, node):
        '''Print out bare assignments'''
        b = self.tree.body
        if self.mode == 'exec' and node in b:
            names, values = node.targets[0], node.value
            
            if isinstance(names, ast.Tuple):
                names = names.elts
            else:
                names = (names, )

            # callify
            self.locals['____nS'] = printEquation
            printer = self.parse("____nS(0, 0)").body[0]

            def tuplify(f):
                return ast.Tuple(elts=list(map(f, names)), ctx=ast.Load())

            def nameToString(n):
                if isinstance(n, ast.Starred):
                    n = n.value
                return ast.Str(s=n.id)

            def nameLoad(n):
                if isinstance(n, ast.Starred):
                    n = n.value
                return ast.Name(id=n.id, ctx=ast.Load())

            printer.value.args = [tuplify(nameToString), tuplify(nameLoad)]
            
            b.append(ast.fix_missing_locations(
                ast.copy_location(printer, node)))
        
        return node
             
