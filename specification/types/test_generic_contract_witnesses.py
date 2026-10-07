"""Regression tests for equality labels and independent static call candidates."""
import copy
import unittest

from generic_contract_witnesses import structural_equal, selected_candidates
from validate_type_spec import includes


class GenericContractWitnessTests(unittest.TestCase):
    def graph(self):
        return {
            "Nat": {"kind": "primitive", "identity": "type::Nat"},
            "A": {"kind": "alias", "identity": "alias::A", "children": ["RA"]},
            "B": {"kind": "alias", "identity": "alias::B", "children": ["RB"]},
            "RA": {"kind": "record", "children": ["FA"]},
            "RB": {"kind": "record", "children": ["FB"]},
            "FA": {"kind": "field", "contract": {"name": "x", "storage": "calculated", "card": [1, 1]}, "children": ["Nat"], "body": "1"},
            "FB": {"kind": "field", "contract": {"name": "x", "storage": "calculated", "card": [1, 1]}, "children": ["Nat"], "body": "2"},
        }

    def test_alias_identity_and_body_are_ignored(self):
        self.assertTrue(structural_equal(self.graph(), "A", "B"))

    def test_storage_kind_and_shape_are_observable(self):
        for key, value in (("storage", "stored"), ("card", [0, 1]),
                           ("order", "ordered"), ("domain", "other-symbolic-domain")):
            graph = self.graph()
            graph["FB"]["contract"][key] = value
            self.assertFalse(structural_equal(graph, "A", "B"), key)

    def test_family_arguments_remain_opaque(self):
        graph = {"A": {"kind": "family", "identity": "family::Slot", "arguments": ["Cat"]},
                 "B": {"kind": "family", "identity": "family::Slot", "arguments": ["Dog"]}}
        self.assertFalse(structural_equal(graph, "A", "B"))
        self.assertTrue(structural_equal(graph, "A", "A"))

    def test_recursive_mismatch_is_not_hidden_by_revisiting(self):
        graph = {"A": {"kind": "record", "children": ["A", "X"]},
                 "B": {"kind": "record", "children": ["B", "Y"]},
                 "X": {"kind": "primitive", "identity": "Nat"},
                 "Y": {"kind": "primitive", "identity": "Text"}}
        self.assertFalse(structural_equal(graph, "A", "B"))
        graph["Y"]["identity"] = "Nat"
        self.assertTrue(structural_equal(graph, "A", "B"))

    def test_alias_only_cycle_rejected(self):
        with self.assertRaises(ValueError):
            structural_equal({"A": {"kind": "alias", "children": ["A"]}}, "A", "A")

    def test_union_source_order_does_not_affect_equality(self):
        graph = {"A": {"kind": "union", "children": ["X", "Y"]},
                 "B": {"kind": "union", "children": ["Y", "X"]},
                 "X": {"kind": "primitive", "identity": "Nat"},
                 "Y": {"kind": "primitive", "identity": "Text"}}
        self.assertTrue(structural_equal(graph, "A", "B"))
        graph["B"]["children"] = ["X", "X"]
        self.assertFalse(structural_equal(graph, "A", "B"))

    def test_product_source_order_remains_observable(self):
        graph = {"A": {"kind": "product", "children": ["X", "Y"]},
                 "B": {"kind": "product", "children": ["Y", "X"]},
                 "X": {"kind": "primitive", "identity": "Nat"},
                 "Y": {"kind": "primitive", "identity": "Text"}}
        self.assertFalse(structural_equal(graph, "A", "B"))

    def fixture(self):
        return {"receivers": [{"name": "Actor"}], "arguments": [{"types": [{"name": "Text"}]}],
                "candidates": [
                    {"identity": "a.Play", "receivers": [{"name": "Actor"}], "givens": [{"name": "value", "type": {"name": "Nat"}}]},
                    {"identity": "b.Play", "receivers": [{"name": "Actor"}], "givens": [{"name": "value", "type": {"name": "Text"}}]},
                ]}

    def test_written_type_selects_and_import_order_does_not(self):
        fixture = self.fixture()
        self.assertEqual(selected_candidates(fixture, includes, {}), ["b.Play"])
        fixture["candidates"].reverse()
        self.assertEqual(selected_candidates(fixture, includes, {}), ["b.Play"])

    def test_named_given_selects_without_return_context(self):
        fixture = self.fixture()
        fixture["arguments"] = [{"name": "text", "types": [{"name": "Text"}]}]
        fixture["candidates"][0]["givens"][0] = {"name": "number", "type": {"name": "Any"}}
        fixture["candidates"][1]["givens"][0]["name"] = "text"
        self.assertEqual(selected_candidates(fixture, includes, {}), ["b.Play"])

    def test_contextual_literal_checks_candidates_independently(self):
        fixture = self.fixture()
        fixture["arguments"] = [{"types": [{"name": "Nat"}, {"name": "Money"}]}]
        fixture["candidates"][1]["givens"][0]["type"] = {"name": "Money"}
        original = copy.deepcopy(fixture)
        self.assertEqual(selected_candidates(fixture, includes, {}), ["a.Play", "b.Play"])
        self.assertEqual(fixture, original)

    def test_defaults_allow_omission_without_preference(self):
        fixture = self.fixture()
        fixture["arguments"] = []
        self.assertEqual(selected_candidates(fixture, includes, {}), [])
        for candidate in fixture["candidates"]:
            candidate["givens"][0]["default"] = True
        self.assertEqual(selected_candidates(fixture, includes, {}), ["a.Play", "b.Play"])

    def test_no_later_lookup_level_after_incompatibility(self):
        fixture = self.fixture()
        fixture["arguments"][0]["types"] = [{"name": "Bool"}]
        self.assertEqual(selected_candidates(fixture, includes, {}), [])

    def test_unknown_admission_is_not_exclusion_evidence(self):
        fixture = self.fixture()
        fixture["arguments"] = [{"types": [{"name": "Nat", "card": [0, 10], "unknown_admission": True}]}]
        for candidate in fixture["candidates"]:
            candidate["givens"][0]["type"] = {"name": "Nat", "card": [0, 5]}
        self.assertEqual(selected_candidates(fixture, includes, {}), ["a.Play", "b.Play"])

    def test_unknown_admission_cannot_repair_nominal_incompatibility(self):
        fixture = self.fixture()
        fixture["arguments"][0]["types"][0]["unknown_admission"] = True
        self.assertEqual(selected_candidates(fixture, includes, {}), ["b.Play"])

    def test_given_witness_cannot_override_primitive_ancestry(self):
        from validate_type_spec import check_witness
        fixture = self.fixture()
        fixture.update(kind="given-selection", parents={"Nat": ["Text"]})
        with self.assertRaises(ValueError):
            check_witness(fixture)


if __name__ == "__main__":
    unittest.main()
