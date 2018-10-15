class _asNamed:
    '''Nicety to allow statements to carry out functions'''
    __slots__ = 'f'
    def __init__(s, f):
        s.f = f
    
    def __repr__(s):
        return s.f()

@_asNamed
def clear():
    return '\n' * 200

def intify(x):
    i = int(x)
    return i if x == i else x
