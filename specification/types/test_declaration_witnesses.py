"""Finite supplied declaration certificates; no source parser or evaluator.

These cases distinguish reachability from strict membership, declaration origin
from inherited paths, and closed member identity from ordering and data values.
"""
import unittest

from specification.types.validate_type_spec import ancestors


class DeclarationWitnesses(unittest.TestCase):
    def test_ancestry_is_reflexive_but_membership_strict(self):
        graph = {"Egypt": ["Kingdom"], "Kingdom": ["Thing"]}
        self.assertEqual(ancestors("Egypt", graph), {"Egypt", "Kingdom", "Thing"})
        self.assertIn("Kingdom", ancestors("Kingdom", graph))
        population = [x for x in ("Egypt", "Kingdom", "Thing")
                      if x != "Kingdom" and "Kingdom" in ancestors(x, graph)]
        self.assertEqual(population, ["Egypt"])

    def test_diamond_is_one_origin_but_incomparable_initializers_conflict(self):
        paths = [("Left", "field::Base::score"),
                 ("Right", "field::Base::score")]
        self.assertEqual({origin for _, origin in paths}, {"field::Base::score"})
        candidates = {"Left": "init::Left", "Right": "init::Right"}
        graph = {"Leaf": ["Left", "Right"], "Left": ["Base"], "Right": ["Base"]}
        self.assertNotIn("Left", ancestors("Right", graph))
        self.assertNotIn("Right", ancestors("Left", graph))
        self.assertEqual(len(set(candidates.values())), 2)
        # Add an explicit more-specific initializer: only Leaf is maximal.
        candidates["Leaf"] = "init::Leaf"
        maximal = [x for x in candidates if not any(
            x != y and x in ancestors(y, graph) for y in candidates)]
        self.assertEqual(maximal, ["Leaf"])

    def test_closed_member_identity_excludes_data_and_preserves_arguments(self):
        source_anchor = "family::Slot::Empty"
        cat = ("Slot", ("Cat",), "Empty")
        dog = ("Slot", ("Dog",), "Empty")
        self.assertNotEqual(cat, dog)
        descriptors = [(source_anchor, cat), (source_anchor, dog)]
        self.assertEqual(descriptors[0][0], descriptors[1][0])
        schema_origin = "family::Terrain::cost"
        projected = {"Plain": (schema_origin, 1), "Mountain": (schema_origin, 4)}
        self.assertEqual(len({origin for origin, _ in projected.values()}), 1)
        self.assertNotEqual(projected["Plain"][1], projected["Mountain"][1])

    def test_family_enumeration_is_not_member_comparison_or_key_order(self):
        members = ("Plain", "Forest", "Mountain", "Water")
        costs = {"Plain": 1, "Forest": 2, "Mountain": 4, "Water": 0}
        key_order = tuple(sorted(members, key=costs.__getitem__))
        self.assertEqual(key_order, ("Water", "Plain", "Forest", "Mountain"))
        self.assertNotEqual(key_order, members)
        has_member_comparison = {"unordered": False, "ordered": True}
        self.assertFalse(has_member_comparison["unordered"])
        self.assertTrue(has_member_comparison["ordered"])


if __name__ == "__main__":
    unittest.main()
