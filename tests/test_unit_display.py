from unittest import TestCase
from noether.unit.scale import number_string


class number_plus_minus(TestCase):
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
        (0),
    )

    def test_equality(self):
        for num, stddev, desired in self.equalityTests:
            actual = number_string(
                num, stddev, asUnit=False, precision=3, unicode_exponent=False
            )
            self.assertEqual(desired, actual)
