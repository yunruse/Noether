'''Noether: Scaling of numbers (a×10^b)'''

from .helpers import sign, intify
from math import log, floor

__all__ = 'prefix exp_mantissa prefixify scinot numberString'.split()

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

superscript = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')

def scinot(num, precision=4, unicode_exponents=True, lower=-2, upper=3):
    '''Return number in scientific notation.
    
    If the exponent of 10 is in the range of `lower` and `upper`, will simply round.'''
    
    exp, man = exp_mantissa(num)
    
    # try avoiding exponent for small exponents if provided
    if lower is not None and upper is not None:
        if lower < exp < upper:
            precision -= exp
            exp = None
            man = num
    
    man = intify(man)
    
    if exp and man == 1:
        num = ''
    elif exp and man == -1:
        num = '-'
    else:
        num = str(intify(round(man, precision)))
    
    if exp:
        # special case of 10^n, -10^n
        if abs(man) != 1:
            num += '×'
        if unicode_exponents:
            num += '10' + str(exp).translate(superscript)
        else:
            num += '10^' + str(exp)
    return num

def numberString(number, delta=0, parens=False, precision=2, unicode_exponent=False, lower=-2, upper=3):
    '''
    Format a number and uncertainty.
    
    Specify parens=True to guarantee parentheses - otherwise
    will only provide if there is a common factor to the number
    and uncertainty.        
    '''
    eN, _ = exp_mantissa(number)
    eD, _ = exp_mantissa(delta)
    print(number, eN)
    print(delta, eD)

    sharedExp = 0
    
    if delta:
        exponentsDiffer = abs(eN - eD) < 4
        humanN = lower < eN < upper
        humanD = lower < eD < upper
        
        if not (exponentsDiffer or humanN or humanD):
            sharedExp = max(eN, eD)

    if sharedExp:
        sharedFactor = 10 ** sharedExp
        number /= sharedFactor
        delta /= sharedFactor
        sExp = scinot(sharedFactor, 1, unicode_exponent, lower=None, upper=None)
    else:
        sExp = ''
    
    sNum = ''
    if number:
        sNum += scinot(number, precision, unicode_exponent, lower=-2, upper=3)
    if delta:
        sNum += ' ± ' + scinot(delta, precision, unicode_exponent, lower=-2, upper=3)
    
    sNum = sNum.strip() or '0'
    if parens or sExp:
        sNum = '(' + sNum + ')' + sExp
    
    return sNum