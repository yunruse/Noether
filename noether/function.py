from .unit import Unit

class Function:
    '''Base class for rich functions that support Units.'''

APPROXIMATE_INTEGRAL_SLICES = 100
APPROXIMATE_DIFFERENTIAL_EPSILON = 1e-9

class UnaryFunction(Function):
    '''Single-input function that supports Unit and certain algebra.'''

    @staticmethod
    def function(value):
        '''Actual numeric function.'''
        return NotImplemented
    
    @staticmethod
    def integral(value):
        '''Definite integral as function or Function'''
        return NotImplemented
    
    @staticmethod
    def differential(value):
        '''Differential as function or Function.'''
        return NotImplemented

    # Overwrite to redefine certain aspects (eg sin -> radian)
    output_dimension = None
    
    @classmethod
    def integrate(self, x, to=None):
        '''Definite or indefinite integral via given function or approximation.'''
        I = self.integral(x)
        if I == NotImplemented:
            # Attempt approximate integration
            if to is None:
                x, to = 0, x
            
            x, to = min(x, to), max(x, to)
            dist = to - x
            for i in range(APPROXIMATE_INTEGRAL_SLICES):
                pass # ugh, trapezoid
        
        else:
            # Use integral given
            if to is None:
                return I
            else:
                return self.integral(to) - I
        
    @classmethod
    def differentiate(self, x):
        d = self.differential(x)
        if d == NotImplemented:
            x1 = float(x - APPROXIMATE_DIFFERENTIAL_EPSILON/2)
            x2 = float(x + APPROXIMATE_DIFFERENTIAL_EPSILON/2)
            return (self.function(x2) - self.function(x1)) / APPROXIMATE_DIFFERENTIAL_EPSILON
        else:
            return d
    
    def __new__(self, x):
        dim = self.output_dimension
        if isinstance(x, Unit):
            value = self.function(float(x))
            new = Unit(value)
            if dim:
                new.dim = dim
            else:
                new.dim = x.dim
            return new

        else:
            value = self.function(x)
            if dim:
                return Unit(value, dim=dim)
            else:
                return value