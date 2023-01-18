from unittest import TestCase

from noether2 import Dimension
from noether2.display import number_string


class test_unit_display(TestCase):
    equalityTests = (
        (0, 0, "0"),
        (20, 0, "20"),
        (0, 20, "± 20"),
        (0, 20000, "± 2×10^4"),
        (200, 1000, "200 ± 1000"),
        (2e5, 1, "2×10^5 ± 1"),
        (2e6, 1e6, "(2 ± 1)×10^6"),
        (2, 1, "2 ± 1"),
        (2, 800000, "2 ± 8×10^5"),
    )

    def test_plus_minus(self):
        '''Test for desired behaviour for numbers with uncertainties ''' q
        for num, stddev, desired in self.equalityTests:
            actual = number_string(
                num, stddev, decimals=3, as_unit=False, unicode_exponent=False
            )
            self.assertEqual(desired, actual)


class test_measure(TestCase):
    def test_dimension_repr_evals(self):
        '''Assert eval(repr(dim)) == dim'''
        for dim, names in Dimension._names.items():
            for n in names:
                self.assertEqual(dim, eval(repr(dim)))
