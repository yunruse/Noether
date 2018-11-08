from unittest import TestCase
from noether.scale import numberString

class UnitDisplayTest(TestCase):
    equalityTests = (
        (0, 0,      '0'),
        (20, 0,     '20'),
        (0, 20,     '± 20'),
        (0, 20000,  '± 2×10^4'),
        (200, 1000, '200 ± 1000'),
        (2e5, 1,    '2×10^5 ± 1'),
        (2e6, 1e6,  '(2 ± 1)×10^6'),
        (2, 1,      '2 ± 1'),
        (2, 800000, '2 ± 8×10^5'),
        (0)
    )

    def test_equality(self):
        for num, delta, desired in self.equalityTests:
            actual = numberString(
                num, delta, parens=False,
                precision=3, unicode_exponent=False)
            self.assertEqual(desired, actual)