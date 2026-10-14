"""Finite supplied arithmetic/ranking certificates; no Mud analyzer or executor."""
from fractions import Fraction
import unittest
from test_rum_witnesses import power, supplied_nearest_even


def supplied_rational_feasible(rows, width):
    rows = [(tuple(map(Fraction, a)), Fraction(b), strict) for a, b, strict in rows]
    for _ in range(width):
        positive = [r for r in rows if r[0][0] > 0]
        negative = [r for r in rows if r[0][0] < 0]
        following = [(a[1:], b, strict) for a, b, strict in rows if a[0] == 0]
        for a, b, strict in positive:
            for c, d, other_strict in negative:
                following.append((tuple(-c[0]*x+a[0]*y for x, y in zip(a[1:], c[1:])),
                                  -c[0]*b+a[0]*d, strict or other_strict))
        rows = following
    return not any(b < 0 or b == 0 and strict for _, b, strict in rows)


def supplied_farkas(rows, goal, multipliers):
    if len(rows) != len(multipliers) or any(len(a) != len(goal[0]) for a, _ in rows):
        return False
    if any(v < 0 for v in multipliers):
        return False
    coefficients = tuple(sum(Fraction(v)*a[i] for (a, _), v in zip(rows, multipliers))
                         for i in range(len(goal[0])))
    bound = sum(Fraction(v)*b for (_, b), v in zip(rows, multipliers))
    return coefficients == tuple(goal[0]) and bound <= goal[1]


def supplied_period_candidates(lower_bounds, upper, modulus, offset):
    return [b+r for b in lower_bounds for r in range(modulus)
            if all(b+r >= bound for bound in lower_bounds)
            and (upper is None or b+r <= upper) and (b+r+offset) % modulus == 0]


class StaticCertificationWitnesses(unittest.TestCase):
    def test_unvalidated_schema_bound_cannot_remove_private_prefix(self):
        # Actual finite count can be 2 at a private prefix despite a declared [1].
        actual = [((-1,), 0, False), ((1,), 2, False), ((-1,), -2, False)]
        self.assertTrue(supplied_rational_feasible(actual, 1))
        self.assertFalse(supplied_rational_feasible(actual+[((1,), 1, False)], 1))

    def test_exact_affine_feasibility_without_coefficient_trial_cap(self):
        rows = [((-1, 1), -1, False), ((1, -2), -1, False),
                ((-1, 0), 0, False), ((0, -1), 0, False)]
        self.assertTrue(supplied_rational_feasible(rows, 2))
        self.assertTrue(all(sum(a*w for a, w in zip(row, (3, 2))) <= bound
                            for row, bound, _ in rows))
        self.assertFalse(supplied_rational_feasible(rows+[((1, 1), 4, False)], 2))

    def test_open_rational_interval_is_not_an_integer_interval(self):
        self.assertTrue(supplied_rational_feasible([((-1,), 0, True), ((1,), 1, True)], 1))
        self.assertEqual(supplied_period_candidates([1], 0, 1, 0), [])
        self.assertFalse(supplied_rational_feasible([((-1,), -1, False), ((1,), 1, True)], 1))

    def test_one_sided_rational_bounds_are_satisfiable(self):
        self.assertTrue(supplied_rational_feasible([((1,), -100, False)], 1))
        self.assertFalse(supplied_rational_feasible([((0,), -1, False)], 1))

    def test_farkas_implication_preserves_correlated_bounds(self):
        rows = [((-1, 0), 0), ((0, -1), 0), ((1, 1), 10)]
        self.assertTrue(supplied_farkas(rows, ((1, 0), 10), (0, 1, 1)))
        self.assertFalse(supplied_farkas(rows, ((1, 0), 9), (0, 1, 1)))
        self.assertFalse(supplied_farkas(rows, ((1, 0), 10), (0, -1, 1)))

    def test_malformed_farkas_evidence_is_rejected(self):
        rows = [((1,), 2)]
        self.assertFalse(supplied_farkas(rows, ((1,), 2), (1, 100)))
        self.assertFalse(supplied_farkas(rows, ((1,), 2), ()))
        self.assertFalse(supplied_farkas([((1, 0), 2)], ((1,), 2), (1,)))

    def test_integral_period_certificate_and_negative_infinity(self):
        candidates = supplied_period_candidates([-10, -9], -5, 3, 1)
        self.assertIn(-7, candidates)
        # With no lower bound, a residue can be translated arbitrarily far below.
        value = 2-3*100
        self.assertLessEqual(value, -5)
        self.assertEqual((value+1) % 3, 0)

    def test_arbitrarily_large_finite_endpoint_and_modulus_witness(self):
        base = 2**1300
        candidates = supplied_period_candidates([base], base+16, 17, 0)
        self.assertEqual(len(set(candidates)), 1)
        self.assertEqual(candidates[0] % 17, 0)

    def test_lexicographic_reset_is_strict(self):
        for major in range(1, 8):
            self.assertLess((major-1, major), (major, 0))
        for minor in range(1, 8):
            self.assertLess((3, minor-1), (3, minor))
        self.assertFalse((3, 0) < (3, 0))

    def test_mutual_phase_is_constant_per_declaration(self):
        for n in range(1, 8):
            self.assertLess((n, 0), (n, 1))
            self.assertLess((n-1, 1), (n, 0))
        self.assertFalse((5, 1) < (5, 1))

    def test_synthesized_affine_certificate(self):
        def rank(x, y):
            return 3*x+2*y
        for x in range(6):
            for y in range(6):
                if x > 0:
                    self.assertEqual(rank(x-1, y+1), rank(x, y)-1)
                elif y > 1:
                    self.assertEqual(rank(x+1, y-2), rank(x, y)-1)
        self.assertEqual(sum(w*d for w, d in zip((3, 2), (-1, 1))), -1)
        self.assertEqual(sum(w*d for w, d in zip((3, 2), (1, -2))), -1)
        self.assertEqual(sum(w*d for w, d in zip((1, 1), (-1, 1))), 0)

    def test_rational_halving_has_no_positive_stable_advance(self):
        values = [Fraction(1, 2**n) for n in range(100)]
        self.assertTrue(all(v > 0 for v in values))
        self.assertTrue(all(b < a for a, b in zip(values, values[1:])))
        self.assertLess(values[-1]/2, Fraction(1, 1000))

    def test_exact_step_count_and_boundary_clamp(self):
        def count(v, lower, step):
            q = (v-lower)/step
            return max(0, -(-q.numerator//q.denominator))
        for value in (Fraction(1, 10), Fraction(1), Fraction(73, 10)):
            step = Fraction(3, 10)
            self.assertEqual(count(value-step, Fraction(0), step),
                             count(value, Fraction(0), step)-1)

    def test_actual_rum_subnormal_descent_and_absorbed_decrement(self):
        spacing = power(-1074)
        self.assertTrue(supplied_nearest_even(spacing/2, spacing, 0))
        self.assertLess(Fraction(0), spacing)
        below_one_spacing = power(-53)
        self.assertTrue(supplied_nearest_even(1-Fraction(1, 10**20),
                                            below_one_spacing, 2**53))
        self.assertEqual((2**53)*below_one_spacing, 1)


if __name__ == "__main__":
    unittest.main()
