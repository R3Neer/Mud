"""Document catalogue consistency and finite coordinate admission certificates.

No source parser, format inverse, numeric conversion or point runtime is built.
"""
from fractions import Fraction
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]


def prefix_rows(text):
    rows = re.findall(r"\|\s*`?(\w+)`?\s*\|\s*([^|]+?)\s*\|\s*10\^(-?\d+)\s*\|", text)
    return [(name, symbol.strip("`"), exponent) for name, symbol, exponent in rows]


class QuantitativeCatalogue(unittest.TestCase):
    def test_prefix_catalogue_matches_current_decision(self):
        chapter = (ROOT / "specification/19-magnitudes.md").read_text(encoding="utf-8")
        decision = (ROOT / "notes/decisions/ADR-076-named-units-prefixes-and-adjacent-notation.md").read_text(encoding="utf-8")
        actual, accepted = prefix_rows(chapter), prefix_rows(decision)
        self.assertEqual(actual, accepted)
        self.assertEqual(len(actual), 24)
        self.assertEqual(len({name for name, _, _ in actual}), 24)
        self.assertEqual(len({symbol for _, symbol, _ in actual}), 24)

    def test_literal_domain_does_not_apply_cycle_repair(self):
        lower, upper = Fraction(0), Fraction(1)
        inside, outside = Fraction(1, 2), Fraction(2)
        self.assertTrue(lower <= inside < upper)
        self.assertFalse(lower <= outside < upper)
        # A cycle would map 2 to zero, illustrating precisely the forbidden repair.
        self.assertEqual(outside % (upper - lower), lower)

    def test_absent_unit_text_does_not_erase_nominal_point_identity(self):
        cursor = ("point::Cursor", "magnitude::Offset", Fraction(1, 2))
        other = ("point::Other", "magnitude::Offset", Fraction(1, 2))
        scalar = ("Num", Fraction(1, 2))
        self.assertNotEqual(cursor, other)
        self.assertNotEqual(cursor, scalar)


if __name__ == "__main__":
    unittest.main()
