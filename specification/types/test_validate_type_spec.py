"""Regression tests for finite formal witnesses and editorial coverage."""
from pathlib import Path
import tempfile
import unittest

from validate_type_spec import (
    ROOT, callable_substitution, equivalent, includes, productive, validate,
    witness_result,
)


class FiniteWitnessTests(unittest.TestCase):
    def test_malformed_graph_is_not_semantic_rejection(self):
        for witness in (
            {"kind": "representation", "left": "A", "right": "A", "nodes": {"A": {"kind": "product", "children": ["Missing"]}}},
            {"kind": "productivity", "root": "Missing", "nodes": {}},
            {"kind": "productivity", "root": "A", "nodes": {"A": {"kind": "transparent", "children": []}}},
        ):
            with self.subTest(witness=witness), self.assertRaises(ValueError):
                witness_result(witness)

    def test_invalid_bound_or_permission_is_not_a_proof(self):
        for invalid in ({"name": "Nat", "card": [2, 1]},
                        {"name": "Nat", "card": [True, 3]},
                        {"name": "Nat", "domain": [4, 1]},
                        {"name": "Nat", "inner_mut": "true"}):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                witness_result({"kind": "inclusion", "source": invalid, "target": {"name": "Nat"}})

    def test_nominal_cycles_are_invalid_certificates(self):
        with self.assertRaises(ValueError):
            witness_result({"kind": "inclusion", "source": {"name": "A"}, "target": {"name": "A"},
                            "parents": {"A": ["B"], "B": ["A"]}})

    def test_unknown_proof_context_cannot_silently_pass(self):
        with self.assertRaises(ValueError):
            witness_result({"kind": "proof-boundary", "context": "invented", "proof": "proved"})

    def test_empty_domain_is_not_a_leaf_witness(self):
        nodes = {"Leaf": {"kind": "leaf", "valid": False},
                 "Parent": {"kind": "product", "children": ["Leaf"]}}
        self.assertNotIn("Parent", productive(nodes))

    def test_domain_inclusion_does_not_erase_nominal_identity(self):
        narrow = {"name": "A", "domain": [2, 4]}
        self.assertTrue(includes(narrow, {"name": "A", "domain": [0, 9]}, {}))
        self.assertFalse(includes(narrow, {"name": "B", "domain": [0, 9]}, {}))

    def test_covariance_does_not_allow_writable_substitution(self):
        parents = {"Dog": ["Animal"]}
        dog, animal = {"name": "Dog"}, {"name": "Animal"}
        self.assertTrue(includes(dog, animal, parents))
        source = {"inputs": [{"mode": "write", "type": dog}], "output": dog}
        target = {"inputs": [{"mode": "write", "type": animal}], "output": animal}
        self.assertFalse(callable_substitution(source, target, parents))

    def test_readonly_variance_direction(self):
        parents = {"Dog": ["Animal"]}
        dog, animal = {"name": "Dog"}, {"name": "Animal"}
        source = {"inputs": [{"mode": "read", "type": animal}], "output": dog}
        target = {"inputs": [{"mode": "read", "type": dog}], "output": animal}
        self.assertTrue(callable_substitution(source, target, parents))
        self.assertFalse(callable_substitution(target, source, parents))

    def test_mutability_and_order_cannot_be_manufactured(self):
        source = {"name": "Person", "order": "age"}
        for target in ({"name": "Person", "inner_mut": True}, {"name": "Person", "order": "name"}):
            with self.subTest(target=target):
                self.assertFalse(includes(source, target, {}))

    def test_zero_cardinality_exit_changes_productivity(self):
        nodes = {"Tree": {"kind": "product", "children": ["Children"]},
                 "Children": {"kind": "container", "minimum": 1, "children": ["Tree"]}}
        self.assertNotIn("Tree", productive(nodes))
        nodes["Children"]["minimum"] = 0
        self.assertIn("Tree", productive(nodes))

    def test_positive_unique_cardinality_requires_multiple_witnesses(self):
        nodes = {"One": {"kind": "leaf"},
                 "Set": {"kind": "container", "minimum": 2, "unique": True,
                         "witness_count": 1, "children": ["One"]}}
        self.assertNotIn("Set", productive(nodes))
        nodes["Set"]["witness_count"] = 2
        self.assertIn("Set", productive(nodes))

    def test_recursive_pairs_cannot_hide_a_mismatched_leaf(self):
        nodes = {"A": {"kind": "product", "children": ["A", "Text"]},
                 "B": {"kind": "product", "children": ["B", "Int"]},
                 "Text": {"kind": "leaf", "label": "Text"},
                 "Int": {"kind": "leaf", "label": "Int"}}
        self.assertFalse(equivalent(nodes, "A", "B"))
        nodes["B"]["children"][1] = "Text"
        self.assertTrue(equivalent(nodes, "A", "B"))

    def test_shape_equivalence_does_not_prove_inhabitation(self):
        nodes = {"A": {"kind": "product", "children": ["A"]},
                 "B": {"kind": "product", "children": ["B"]}}
        self.assertTrue(equivalent(nodes, "A", "B"))
        self.assertEqual(productive(nodes), set())

    def test_runtime_admission_cannot_replace_a_static_cardinality_proof(self):
        witness = {"kind": "proof-boundary", "context": "value-admission", "proof": "unknown"}
        self.assertEqual(witness_result(witness), "runtime-check")
        witness["context"] = "stored-cardinality"
        self.assertEqual(witness_result(witness), "static-reject")

    def test_current_repository(self):
        self.assertEqual(validate(), [])

    def test_losing_an_expression_or_rule_case_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ("10-type-system.md", "14-fields-and-mutability.md", "19-expressions.md",
                             "types/typing-cases.yaml", "types/expression-coverage.yaml",
                             "syntax/mud-surface-ast.asdl"):
                target = root / "specification" / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / "specification" / relative).read_bytes())
            path = root / "specification/types/expression-coverage.yaml"
            import yaml
            coverage = yaml.safe_load(path.read_text(encoding="utf-8"))
            del coverage["expressions"]["CallExpr"]
            path.write_text(yaml.safe_dump(coverage), encoding="utf-8")
            self.assertTrue(any("CallExpr" in problem for problem in validate(root)))


if __name__ == "__main__":
    unittest.main()
