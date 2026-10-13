"""Exact-rational certificates for supplied binary64 sites, not a runtime.

Spacings, exponents and candidates are supplied premises. This checks finite
rounding/exception/contraction examples; it does not parse or evaluate Mud.
"""
from fractions import Fraction
import unittest


def power(exponent):
    return Fraction(2 ** exponent) if exponent >= 0 else Fraction(1, 2 ** -exponent)


def supplied_nearest_even(value, spacing, candidate):
    """Check the chosen integer lattice neighbor by exact distance and parity."""
    choices = (candidate - 1, candidate, candidate + 1)
    best = min(choices, key=lambda k: (abs(value - k * spacing), k % 2))
    return best == candidate


def supplied_remainder(a, b):
    quotient = a / b
    q = abs(quotient.numerator) // quotient.denominator
    if quotient < 0:
        q = -q
    return a - q * b


class RumWitnesses(unittest.TestCase):
    def test_decimal_tenth_single_rounding(self):
        value = Fraction(1, 10)
        candidate = 7205759403792794
        spacing = power(-56)
        self.assertTrue(supplied_nearest_even(value, spacing, candidate))
        self.assertEqual(candidate * spacing, Fraction(3602879701896397, 36028797018963968))

    def test_normal_halfway_parity(self):
        spacing = power(-52)
        base = 2 ** 52
        self.assertTrue(supplied_nearest_even(1 + spacing / 2, spacing, base))
        self.assertTrue(supplied_nearest_even(1 + 3 * spacing / 2, spacing, base + 2))

    def test_subnormal_zero_and_normal_boundary(self):
        spacing = power(-1074)
        self.assertTrue(supplied_nearest_even(spacing / 2, spacing, 0))
        self.assertTrue(supplied_nearest_even(3 * spacing / 4, spacing, 1))
        self.assertTrue(supplied_nearest_even(3 * spacing / 2, spacing, 2))
        boundary = power(-1022)
        self.assertTrue(supplied_nearest_even(boundary - spacing / 2, spacing, 2 ** 52))
        self.assertEqual((2 ** 52) * spacing, boundary)

    def test_overflow_carry_is_not_saturation(self):
        spacing = power(971)
        threshold = power(1024) - power(970)
        self.assertTrue(supplied_nearest_even(threshold, spacing, 2 ** 53))
        self.assertEqual((2 ** 53) * spacing, power(1024))
        # The supplied carry changes exponent 1023 to 1024: not a finite value.
        self.assertGreater(1023 + 1, 1023)

    def test_truncating_remainder_and_unrounded_quotient(self):
        for a, b, expected in ((Fraction(-11, 2), Fraction(2), Fraction(-3, 2)),
                               (Fraction(5), Fraction(3), Fraction(2)),
                               (Fraction(5), Fraction(-3), Fraction(2))):
            self.assertEqual(supplied_remainder(a, b), expected)
        self.assertEqual(supplied_remainder(power(1023), power(-1074)), 0)
        with self.assertRaises(ZeroDivisionError):
            supplied_remainder(Fraction(1), Fraction(0))

    def test_fma_changes_the_supplied_observable_result(self):
        a, b, c = 1 + power(-27), 1 - power(-27), Fraction(-1)
        exact_product = a * b
        self.assertTrue(supplied_nearest_even(exact_product, power(-53), 2 ** 53))
        separately_rounded = Fraction(1) + c
        fused = exact_product + c
        self.assertEqual(separately_rounded, 0)
        self.assertEqual(fused, -power(-54))
        self.assertNotEqual(separately_rounded, fused)


if __name__ == '__main__':
    unittest.main()
