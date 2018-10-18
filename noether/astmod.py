from ast import *

def copy(old_node, new_node):
    return copy_location(new_node, old_node)

fix = fix_missing_locations

def copyfix(old_node, new_node):
    return fix(copy_location(new_node, old_node))

load = Load()
store = Store()

class Language(NodeTransformer):
    '''Abstract syntax tree stateful transformer.

    Instances holds state on node, such that __init__ may be defined.

    As such, depending on if you want to retrieve state or not:

    
    node = DerivedClass.translate(node, 'eval', globals, locals)
    '''

    def __init__(self):
        self.translate = self._translate

    def _translate(self, node, mode='exec', g=None, l=None):
        self.node = node
        self.mode = mode
        self.globals = g or globals()
        self.locals = l or dict()
        self.init()
        self.visit(node)
        self.finish()
        return node

    # overwritable methods

    def init(self):
        pass

    def finish(self):
        pass

    # public methods

    @classmethod
    def translate(cls, node, mode='exec', globals=None, locals=None):
        return cls()._translate(node, mode, globals, locals)
    
    @classmethod
    def parse(cls, source, filename='<unknown>', mode='exec', globals=None, locals=None):
        node = compile(source, filename, mode, flags=PyCF_ONLY_AST)
        return cls.translate(node, mode, globals, locals)

    @classmethod
    def _process(cls, f, code, g, l):
        gl = g or globals(), l or locals()
        nm = f'<{cls.__name__}>', f.__name__
        tree = cls.parse(code, *nm, *gl)
        binary = compile(tree, *nm)
        return f(binary, *gl)
    
    @classmethod
    def eval(cls, code, globals=None, locals=None):
        return cls()._process(eval, code, globals, locals)
    
    @classmethod
    def exec(cls, code, globals=None, locals=None):
        cls._process(exec, code, globals, locals)
