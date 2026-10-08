"""Finite integral interval-content certificates; no general Mud normalizer."""
import unittest
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
if __name__=='__main__': unittest.main()
