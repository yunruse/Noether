'''
Test various repr() and str() methods for objects.
'''
from unittest import TestCase

import noether
from noether import time, length
from noether.display import uncertainty

noether.conf.reset()


class test_unit_display(TestCase):
    dim_mult_display = (
        (time, 'time'),
        (length / time, 'speed'),
        (length / time**2, 'acceleration'),
        (time / length**0.5, 'time / length**0.5'),
        ((time * length) ** 0.5, 'length**0.5 * time**0.5'),
    )

    def test_dimension_display(self):
        '''Test for desired behaviour for numbers with uncertainties '''
        for dim, string in self.dim_mult_display:
            self.assertEqual(dim.name(), string)

    uncertainty_display = (
        ('1.00794', '0.00007', '1.00794(7)'),
        ('1.45', '0.12', '1.45(12)'),
        ('1.04', '0.012', '1.040(12)'),
        ('1.04', '0.0012', '1.0400(12)'),
        ('0.15', '0.06', '0.15(6)'),
        ('1243', '3', '1243(3)'),
    )

    def test_uncertainty_display(self):
        for a, b, c in self.uncertainty_display:
            d = uncertainty(a, b)
            self.assertEqual(c, d)

    value_repr_str = (
        (
            'length',  # Dimension
            'length  # length, distance, height, width, breadth, depth',
            'length',
        ),
        (
            'kelvin * meter * 1',  # Measure
            '1 K m  # temperature * length',
            '1 K m'
        ),
        (
            'meter',  # Unit
            'meter  # length',
            'meter'
        ),
        (
            'foot & inch',  # ChainedUnit
            'foot & inch  # length',
            'foot & inch'
        ),
    )

    def test_value_repr_str(self):
        for k, n, s in self.value_repr_str:
            val = eval(k, {}, vars(noether))
            self.assertEqual(n, val.__noether__())
            self.assertEqual(s, str(val))
