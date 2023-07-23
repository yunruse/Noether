'''
Test various repr() and str() methods for objects.
'''
from unittest import TestCase

import noether
from noether import time, length
from noether.display import uncertainty

from pathlib import Path
REPR_TESTS = Path(__file__).parent / 'repr_tests.txt'

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

    def get_repr_tests(self):
        with open(REPR_TESTS) as f:
            text = f.read()
        for test in text.split('>>> '):
            test = test.strip()
            if not test:
                continue
            value, repr_test = test.split('\n')
            value, name = value.split('  # ')
            yield value, name, repr_test

    def test_value_repr_str(self):
        for value, name, repr_test in self.get_repr_tests():
            val = eval(value, {}, vars(noether))
            self.assertEqual(
                repr_test, val.__noether__(),
                msg=f'repr : {value} : {name}')
