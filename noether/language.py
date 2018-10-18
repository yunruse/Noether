'''Custom REPL language used by Noether.'''

from noether import astmod as ast

def printEquation(*namevals):
    maxlen = max(len(n) for n,v in namevals)
    for n, v in namevals:
        spacing = ' ' * (maxlen-len(n))
        print('{}{} = {!r}'.format(n, spacing, v))

class Noether(ast.Language):
    
    modified = True

    @classmethod
    def _process(cls, f, code, globals=None, locals=None):
        if cls.modified:
            return super()._process(f, code, globals, locals)
        else:
            return f(code, globals, locals)

    modEqualPrint = True

    def init(self):
        self.assignments = []

    def visit_AugAssign(self, node):
        '''Bare `a %= x` statements will print themselves.'''
        b = self.node.body
        if (
            self.modEqualPrint and self.mode == 'exec' and
            isinstance(node.op, ast.Mod) and node in b):
            
            name = node.target
            node = ast.copy(node, ast.Assign(
                targets=[name],
                value=node.value,
            ))

            self.assignments.append((ast.Tuple(
                ctx=ast.load, elts=[
                    ast.Str(s=name.id),
                    ast.Name(id=name.id, ctx=ast.load),
            ])))

        return node

    def finish(self):
        if self.mode == 'exec' and self.assignments:
            nodeFrom = self.assignments[0].elts[0]
            self.locals['____nS'] = printEquation
            printer = ast.copyfix(nodeFrom, ast.Expr(value=ast.Call(
                func=ast.Name(ctx=ast.load, id='____nS'),
                args=self.assignments, keywords=[]
            )))
            printer.lineno = 18
            self.node.body.append(printer)
                               
            
