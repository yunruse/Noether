'''Noether: Scaling of numbers (a×10^b)'''

from .helpers import sign, intify
from math import log, floor

__all__ = 'prefix exp_mantissa prefixify powerify scinot'.split()

class prefix:
    pass
_prefixes = {}

for exp, sym in enumerate('yzafpnμm kMGTPEZY', -8):
    if exp:
        _prefixes[sym] = exp
        setattr(prefix, sym, 10 ** (exp * 3))

def exp_mantissa(num, base=10):
    '''Returns e, m such that x = m×10^e'''
    if num == 0:
        return 1, 0
    exp = floor(log(abs(num), base))
    mantissa = num / (base ** exp)
    return exp, mantissa

def prefixify(num):
    '''Returns a number and any fitting SI prefix.'''
    if not isinstance(num, (float, int)):
        return num, ''
    exp, mantissa = exp_mantissa(num, 10)        
    for prefix, pExp in _prefixes.items():
        if -2 < exp - pExp < 3:
            return mantissa * 10**exp, prefix
    else:
        return num, ''

powerify = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')

def scinot(num, precision=4, unicode_exponents=True):
    '''Return number in scientific notation.'''
    
    # -1, 0, 1: special cases
    if num == sign(num):
        return str(num)
    
    exp, man = exp_mantissa(num)
    
    if -3 <= exp <= 2:
        # easily naturalised
        precision -= exp
        exp = None
        man = num
    
    man = intify(man)
    
    if man == 1:
        num = ''
    elif man == -1:
        num = '-'
    elif isinstance(man, int):
        num = str(man)
    else:
        num = str(round(man, precision))
    
    if exp:
        # unicode exponents
        if abs(man) != 1:
            num += '×'
        powers = str(exp)
        if unicode_exponents:
            num += '10' + powers.translate(powerify)
        else:
            num += '10^' + powers
    
    return num
