'''Custom REPL language used by Noether.'''

from astley import *
from .unit import Unit
from .helpers import tablify

def printEquation(*nv):
    namevals = []
    maxlen = []
    for name, val in nv:
        if isinstance(val, Unit):
            namevals.append((name, '=', *val._reprElements()))
        else:
            firstline, *rest = str(val).split('\n')
            namevals.append((name, '=', firstline))
            for line in rest:
                namevals.append(('', '', line))
    for line in tablify(namevals):
        print(line)

def assignFunctionID(f, r):
    f.____noetherRepr = r
    return f

@match
class Noether(Language):
    modEqualPrint = True
    
    def onVisitStart(self):
        self.assignments = []
        self.funcs = dict()
    
    @match(kind=AugAssign, mode='exec', op=Mod, baseNode=True)
    def ModPrint(self, node):
        '''Bare `a %= x` statements will print themselves.'''
        name = node.target
        node = copy(node, Assign(
            [name], self.visit(node.value),
        ))
        
        self.assignments.append(Tuple(
            [Str(name.id), Name(name.id)]
        ))
        return node
    
    @match(kind=Lambda)
    def lambdaSignify(self, node):
        F = '____nF'
        self.locals[F] = assignFunctionID
        code = Str(node.asPython())
        
        return copyfix(node, Name(F)(node, code))
    
    @match(kind=(FunctionDef, AsyncFunctionDef))
    def funcSignify(self, node):
        F = '____nF'
        self.locals[F] = assignFunctionID
        
        # wrap in `lambda x: F(x, str(node))`
        # it is around these points I wish LISP was a thing here
        code = Str(node.asPython())
        node.decorator_list.insert(0, copyfix(node, Lambda(
            [Name('x')], Name(F)(Name('x'), code)
        )))
        return node
    
    def onVisitFinish(self):
        if self.mode == 'exec' and self.assignments:
            F = '____nS'
            nodeFrom = self.assignments[0].elts[0]
            self.locals[F] = printEquation
            
            printer = copyfix(
                nodeFrom, Expr(Name(F)(*self.assignments)))
            printer.lineno += 1
            self.node.body.append(printer)
    
    @match(kind=Num, n=float)
    def alwaysUnit(self, node):
        return copyfix(node, Name('Unit')(node))
    
    @match(kind=BinOp, op=Add)
    def plusMinus(self, node):
        if not (isinstance(node.right, UnaryOp) and
            isinstance(node.right.op, USub)):
            return node
        'Unit'
        return copyfix(node, Name('Unit')(
            node.left, delta=node.right.operand))