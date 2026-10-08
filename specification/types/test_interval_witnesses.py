"""Finite integral interval-content certificates; no general Mud normalizer."""
import unittest
from fractions import Fraction
class IntervalCertificates(unittest.TestCase):
    def test_supplied_segment_normal_forms(self):
        cases=[([(1,3),(7,9)],[(1,3),(7,9)]), ([(7,9),(1,3)],[(1,3),(7,9)]), ([(1,5),(3,9)],[(1,9)]), ([],[]), ([(1,3),(4,6)],[(1,6)])]
        for source,normal in cases:
            members=lambda xs: {i for a,b in xs for i in range(a,b+1)}
            self.assertEqual(members(source),members(normal))
            self.assertTrue(all(a<=b for a,b in normal))
            self.assertTrue(all(b+1<c for (_,b),(c,_) in zip(normal,normal[1:])))
    def test_negative_steps_restart(self):
        segments=[(1,3),(7,9)]
        self.assertEqual([x for a,b in reversed(segments) for x in range(b,a-1,-2)],[9,7,3,1])
    def test_supplied_exact_rational_grid_is_not_all_interval_members(self):
        lower, upper, step = Fraction(0), Fraction(1), Fraction(1, 5)
        count = int((upper - lower) / step) + 1
        ascending = [lower + i * step for i in range(count)]
        descending = [upper - i * step for i in range(count)]
        self.assertEqual(ascending, [Fraction(i, 5) for i in range(6)])
        self.assertEqual(descending, list(reversed(ascending)))
        self.assertTrue(lower < Fraction(1, 7) < upper)
        self.assertNotIn(Fraction(1, 7), ascending)
if __name__=='__main__': unittest.main()
