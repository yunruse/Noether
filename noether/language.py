"""Custom REPL language used by Noether."""

# pylint: disable=W0614,E0602

from astley import *  # noqa: F403
from .unit import Unit
from .helpers import tablify


def printEquation(*nv):
    namevals = []
    for name, val in nv:
        if isinstance(val, Unit):
            namevals.append((name, "=", *val._reprElements()))
        else:
            firstline, *rest = str(val).split("\n")
            namevals.append((name, "=", firstline))
            for line in rest:
                namevals.append(("", "", line))
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

    @match(kind=AugAssign, mode="exec", op=Mod, baseNode=True)
    def ModPrint(self, node):
        """Bare `a %= x` statements will print themselves."""
        name = node.target
        node = copy(node, Assign([name], self.visit(node.value)))

        self.assignments.append(Tuple([Str(name.id), Name(name.id)]))
        return node

    @match(kind=Lambda)
    def lambdaSignify(self, node):
        F = "____nF"
        self.locals[F] = assignFunctionID
        code = Str(node.asPython())

        return copyfix(node, Name(F)(node, code))

    # for some reason this causes errors
    # @match(kind=(FunctionDef, AsyncFunctionDef))
    def funcSignify(self, node):
        F = "____nF"
        self.locals[F] = assignFunctionID

        # wrap in `lambda x: F(x, str(node))`
        # it is around these points I wish LISP was a thing here
        code = Str(node.asPython())
        node.decorator_list.insert(
            0, copyfix(node, Lambda([Name("x")], Name(F)(Name("x"), code)))
        )
        return node

    def onVisitFinish(self):
        if self.mode == "exec" and self.assignments:
            F = "____nS"
            nodeFrom = self.assignments[0].elts[0]
            self.locals[F] = printEquation

            printer = copyfix(nodeFrom, Expr(Name(F)(*self.assignments)))
            printer.lineno += 1
            self.node.body.append(printer)

    @match(kind=Num, n=float)
    def alwaysUnit(self, node):
        return copyfix(node, Name("Unit")(node))

    @match(kind=BinOp, op=Add)
    def delta(self, node):
        """a +- b == Unit(a, _delta=b)"""
        r = node.right

        delta = None
        if isinstance(r, UnaryOp) and isinstance(r.op, USub):
            delta = r.operand
        elif (
            isinstance(r, BinOp)
            and isinstance(r.left, UnaryOp)
            and isinstance(r.left.op, USub)
        ):
            # a +- b/2 == a + (-b)/2
            r.left = copy(r.left, r.left.operand)
            delta = r

        if delta:
            return copyfix(node, Name("Unit")(node.left, _delta=delta))
        return node

    @match(kind=BinOp, op=Mod)
    def epsilon(self, node):
        """a %+- b == Unit(a, _epsilon=b)"""
        r = node.right
        if isinstance(r, UnaryOp) and isinstance(r.op, UAdd):
            q = r.operand
            if isinstance(q, UnaryOp) and isinstance(q.op, USub):
                e = q.operand / 100
                return copyfix(node, Name("Unit")(node.left, _epsilon=e))
        return node

    @match(kind=UnaryOp, op=UAdd)
    def plusMinus(self, node):
        o = node.operand
        if isinstance(o, UnaryOp) and isinstance(o.op, USub):
            return copyfix(node, Name("Unit")(Num(0), _delta=o.operand))
        return node
