'''
Test various repr() and str() methods for objects.
'''
from unittest import TestCase

from noether import time, length
from noether.core.display import uncertainty


class test_unit_display(TestCase):
    dimension_display = (
        (time, 'time  # time'),
        (length / time, 'length / time  # speed'),
        (length / time**2, 'length / time**2  # acceleration'),
        (time / length**0.5, 'time * length**(-1/2)'),
        ((time * length) ** 0.5, 'length**(1/2) * time**(1/2)'),
    )

    def test_dimension_display(self):
        '''Test for desired behaviour for numbers with uncertainties '''
        for dim, string in self.dimension_display:
            self.assertEqual(repr(dim), string)

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
