'''
A quick pocket-calculator-like interpreter for Noether.

Launches quickly by making heavy imports (numpy, matplotlib) in the background.
'''

NOETHER_IMPORT = '''
import noether
from noether import *

display = Unit.display
'''

class EOF_during_input(EOFError):
    '''sentinel to passthrough'''

class REPLHistory(list):
    def __repr__(self):
        l = len(self) - 1
        return '<REPLHistory(list) of {} item{}>'.format(
            l, 's'*(l != 1)
        )

glob = dict(globals())
loc = dict(locals())

class NoetherInstance:
    '''
    Simple REPL example meant, for now, to replicate `python -i`.
    '''
    __slots__ = ('globals', 'locals', 'input', 'had_error', 'history')
    def __init__(self, script=NOETHER_IMPORT):
        self.input = ''
        self.had_error = False
        self.history = REPLHistory()
        self.globals = dict(globals())
        self.locals = dict(locals())
        self.locals['_'] = None
        self.locals['__'] = self.history
        self.eval(script)
    
    def eval(self, string) -> str:
        # TODO: maybe see how IDLE does this
        try:
            return eval(string, self.globals, self.locals)
        except EOFError:
            return EOF_during_input
        except SyntaxError:
            return exec(string, self.globals, self.locals)
    
    def push_history(self, item):
        self.history.append(item)
        self.locals['_'] = item
        self.locals['__'] = self.history
    
    def ps(self):
        if self.input:
            ps = '...'
        elif self.had_error:
            ps = '!>>'
        else:
            ps = '>>>'
        
        return ps + ' '

    def step(self):
        line = ''
        while not line:
            try:
                line = input(self.ps())
            except EOFError:  # ^Z
                exit(0)
            except KeyboardInterrupt:  # ^C
                print('\nKeyboardInterrupt: to exit, type `exit()` or Ctrl-Z, and then hit Return')
            else:
                break  # no errors; line is acceptable
        
        self.input += line
        try:
            result = self.eval(self.input)
            # result will be `EOFError
            if result is EOF_during_input:
                pass # to next step()
            else:
                self.push_history(result)
                self.input = ''
                self.had_error = False
                if result is not None:
                    print(repr(result))

        except Exception as e:
            self.input = ''
            self.had_error = True
            print(type(e).__name__ + ': ' + str(e))
            raise 
    
    def loop(self):
        error = None
        while not error:
            error = self.step()

if __name__ == '__main__':
    import noether
    from noether import *
    display = Unit.display
    NoetherInstance().loop()
