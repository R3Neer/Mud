"""Finite supplied declaration certificates; no source parser or evaluator.

These cases distinguish reachability from strict membership, declaration origin
from inherited paths, and closed member identity from ordering and data values.
"""
import unittest

from specification.types.validate_type_spec import ancestors


def supplied_comparison_reaches_functional(nodes, root):
    """Check a supplied finite equality-edge certificate, not source eligibility."""
    seen, todo = set(), [root]
    while todo:
        node = todo.pop()
        if node in seen:
            continue
        seen.add(node)
        if nodes[node]["kind"] == "functional":
            return True
        todo.extend(nodes[node].get("compared", []))
    return False


class DeclarationWitnesses(unittest.TestCase):
    def test_functional_equality_exclusion_is_transitive(self):
        nodes = {"F": {"kind": "functional"},
                 "Alias": {"kind": "alias", "compared": ["F"]},
                 "Tuple": {"kind": "tuple", "compared": ["Alias"]},
                 "Tree": {"kind": "alias", "compared": ["Tree", "Nat"]},
                 "Nat": {"kind": "basic"}}
        self.assertTrue(supplied_comparison_reaches_functional(nodes, "Tuple"))
        self.assertFalse(supplied_comparison_reaches_functional(nodes, "Tree"))

    def test_projected_key_and_derived_or_empty_contents_are_separate(self):
        nodes = {"F": {"kind": "functional"}, "Nat": {"kind": "basic"},
                 "Record": {"kind": "alias", "compared": ["Nat"], "derived": ["F"]},
                 "Empty": {"kind": "zero-maximum-container", "compared": []},
                 "WithPolicy": {"kind": "alias", "compared": ["Nat", "F"]}}
        self.assertFalse(supplied_comparison_reaches_functional(nodes, "Record"))
        self.assertFalse(supplied_comparison_reaches_functional(nodes, "Empty"))
        self.assertTrue(supplied_comparison_reaches_functional(nodes, "WithPolicy"))
        self.assertFalse(supplied_comparison_reaches_functional(nodes, "Nat"))

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
