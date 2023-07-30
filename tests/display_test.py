'''
Test various repr() and str() methods for objects.
'''
from typing import Any, Callable
from unittest import TestCase

import noether
from noether import time, length, Dimension
from noether.display import uncertainty

from pathlib import Path

DIR = Path(__file__).parent

noether.conf.reset()


class test_unit_display(TestCase):
    dim_mult_display: list[tuple[Dimension, str]] = [
        (time, 'time'),
        (length / time, 'speed'),
        (length / time**2, 'acceleration'),
        (time / length**0.5, 'time / length**0.5'),
        ((time * length) ** 0.5, 'length**0.5 * time**0.5'),
    ]

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

    def get_tests(self, name: str):
        with open(DIR / f'{name}.txt') as f:
            text = f.read()
        for test in text.split('>>> '):
            test = test.strip()
            if not test:
                continue
            value, repr_test = test.split('\n')
            value, name = value.split('  # ')
            yield value, name, repr_test

    def evaluate(
        self,
        name: str,
        func: Callable[[Any], str],
        namespace: dict[str, Any] | None = None
    ):
        for value, name, repr_test in self.get_tests(name):
            val = eval(value, noether.__dict__, namespace or {})
            self.assertEqual(
                repr_test, func(val),
                msg=f'repr : {value} : {name}')

    def test_value_repr(self):
        self.evaluate('repr_tests', repr)
