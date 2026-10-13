"""Supplied finite dimension/scale certificates, not a Mud unit analyzer."""
from fractions import Fraction
import unittest


def supplied_factors(left, right, divide=False):
    result = dict(left)
    for anchor, exponent in right.items():
        result[anchor] = result.get(anchor, 0) + (-exponent if divide else exponent)
    return tuple(sorted((anchor, power) for anchor, power in result.items() if power))


class DimensionWitnesses(unittest.TestCase):
    def test_factor_cancellation_and_order(self):
        length = {'magnitude::Length': 1}
        time = {'magnitude::Time': 1}
        self.assertEqual(supplied_factors(length, time, True),
                         (('magnitude::Length', 1), ('magnitude::Time', -1)))
        self.assertEqual(supplied_factors(length, length), (('magnitude::Length', 2),))
        self.assertEqual(supplied_factors(length, length, True), ())

    def test_distinct_nominal_unitless_bases(self):
        self.assertNotEqual(supplied_factors({'magnitude::CountA': 1}, {}),
                            supplied_factors({'magnitude::CountB': 1}, {}))

    def test_checked_exact_scale_certificate(self):
        # Supplied positive root equivalences and enabled decimal prefix.
        kilo = Fraction(1000)
        hour = Fraction(3600)
        scale = kilo / hour
        self.assertEqual(scale, Fraction(5, 18))
        self.assertEqual(Fraction(90) * scale, Fraction(25))
        self.assertTrue(scale > 0)

    def test_representation_admission_precedes_cancellation(self):
        # Only these already-established numeric signatures are supplied.
        signatures = {('Money', '*', 'Num'): 'Money',
                      ('Money', '/', 'Money'): 'Num'}
        self.assertEqual(signatures[('Money', '*', 'Num')], 'Money')
        self.assertEqual(signatures[('Money', '/', 'Money')], 'Num')
        self.assertNotIn(('Money', '*', 'Money'), signatures)
        self.assertEqual(supplied_factors({'magnitude::Cost': 1},
                                         {'magnitude::Cost': 1}, True), ())
        # Equal final dimensions supply no missing intermediate signature.
        self.assertNotIn(('Money', '*', 'Money'), signatures)


if __name__ == '__main__':
    unittest.main()
