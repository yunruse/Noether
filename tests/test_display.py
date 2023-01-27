'''
Test various repr() and str() methods for objects.
'''
from unittest import TestCase

import noether
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

    value_code_noether_str = (
        (
            'length',  # Dimension
            'Dimension(length=1)',
            'length  # length, distance, height, width, breadth, depth',
            'length',
        ),
        (
            'K * m',  # Measure
            'Measure(1, dim=Dimension(temperature=1, length=1))',
            '1 K * m  # temperature * length',
            '1 K m'
        ),
        (
            'meter',  # Unit
            "Unit(Measure(1, dim=Dimension(length=1)), ['meter', 'metre'], 'm', SI_large + SI_small + SI_conventional)",
            'meter  # length',
            'meter'
        ),
        (
            'foot & inch',  # ChainedUnit
            'ChainedUnit(foot, inch)',
            'foot & inch  # length',
            'foot & inch'
        ),
    )

    def test_value_code_repr_str(self):
        for cat in noether.conf.categories()['info']:
            noether.conf[f'info_{cat}'] = False
        noether.conf[f'info_dimension'] = True
        for k, c, n, s in self.value_code_noether_str:
            val = eval(k, {}, vars(noether))
            self.assertEqual(c, val.repr_code())
            self.assertEqual(n, val.__noether__())
            self.assertEqual(s, str(val))
