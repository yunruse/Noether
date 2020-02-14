from .measure import Measure 

class Function:
    '''Base class for rich functions that support Measures.'''

APPROXIMATE_INTEGRAL_SLICES = 100
APPROXIMATE_DIFFERENTIAL_EPSILON = 1e-9

class UnaryFunction(Function):
    '''Single-input function that supports Measure and certain algebra.'''

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
    def integrate(cls, x, to=None):
        '''Definite or indefinite integral via given function or approximation.'''
        I = cls.integral(x)
        if I == NotImplemented:
            raise NotImplementedError("Todo: trapezoid method")
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
                return cls.integral(to) - I
        
    @classmethod
    def differentiate(cls, x):
        d = cls.differential(x)
        if d == NotImplemented:
            x1 = float(x - APPROXIMATE_DIFFERENTIAL_EPSILON/2)
            x2 = float(x + APPROXIMATE_DIFFERENTIAL_EPSILON/2)
            return (cls.function(x2) - cls.function(x1)) / APPROXIMATE_DIFFERENTIAL_EPSILON
        else:
            return d
    
    def __new__(cls, x):
        dim = cls.output_dimension
        if isinstance(x, Measure):
            value = cls.function(float(x))
            new = Measure(value)
            if dim is not None:
                new.dim = dim
            else:
                new.dim = x.dim
            return new

        else:
            value = cls.function(x)
            if dim:
                return Measure(value, dim=dim)
            else:
                return value
