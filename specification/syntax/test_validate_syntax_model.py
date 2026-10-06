"""Regression checks for the nominal-HIR phase boundary and pending calls."""
from pathlib import Path
import re
import unittest

from validate_syntax_model import nominal_hir_contract_problems


class NominalHIRContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hir = (Path(__file__).resolve().parents[1] / "names/mud-nominal-hir.asdl").read_text(encoding="utf-8")

    def test_current_contract(self):
        self.assertEqual(nominal_hir_contract_problems(self.hir), [])

    def test_candidate_set_cannot_be_replaced_with_selected_target(self):
        malformed = self.hir.replace("symbol_id* candidates", "symbol_id target")
        self.assertTrue(any("PendingReceiverCall" in p for p in nominal_hir_contract_problems(malformed)))

    def test_pending_call_must_retain_lookup_level(self):
        malformed = self.hir.replace("lookup_level level,", "")
        self.assertTrue(any("PendingReceiverCall" in p for p in nominal_hir_contract_problems(malformed)))

    def test_bindings_cannot_drop_pending_calls(self):
        malformed = self.hir.replace("nominal_reference* bindings", "symbol_id* bindings")
        self.assertTrue(any("bindings" in p for p in nominal_hir_contract_problems(malformed)))

    def test_pending_constructor_must_belong_to_reference_sum(self):
        malformed = self.hir.replace("nominal_reference = ResolvedReference", "resolved_reference = ResolvedReference")
        self.assertTrue(any("nominal_reference" in p for p in nominal_hir_contract_problems(malformed)))

    def test_lookup_priority_cannot_be_collapsed(self):
        malformed = self.hir.replace("ExactUsingLevel | RecursiveUsingLevel", "UsingLevel")
        self.assertTrue(any("lookup_level" in p for p in nominal_hir_contract_problems(malformed)))

    def test_pending_call_cannot_contain_elaborated_types(self):
        malformed = self.hir.replace("lookup_level level,", "lookup_level level, semantic_type receiver_type,")
        problems = nominal_hir_contract_problems(malformed)
        self.assertTrue(any("forbidden elaboration" in p for p in problems))
        self.assertTrue(any("PendingReceiverCall" in p for p in problems))

    def test_layout_and_comments_are_not_contract_changes(self):
        reformatted = re.sub(r"\s+", " ", self.hir)
        # Preserve the type-definition boundaries used by the ASDL reader.
        reformatted = re.sub(r" (?=[a-z][a-z0-9_]* =)", "\n    ", reformatted).replace(" }", "\n}")
        self.assertEqual(nominal_hir_contract_problems(reformatted), [])
        self.assertEqual(nominal_hir_contract_problems(self.hir + "\n-- semantic_type is excluded\n"), [])


if __name__ == "__main__":
    unittest.main()
