"""Regression checks for nominal resolution and foreign syntax boundaries."""
from pathlib import Path
import re
import unittest

from validate_syntax_model import foreign_contract_problems, nominal_hir_contract_problems


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


class ForeignContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[2]
        cls.grammar = (root / "specification/grammar/mud.ebnf").read_text(encoding="utf-8")
        cls.ast = (root / "specification/syntax/mud-surface-ast.asdl").read_text(encoding="utf-8")

    def test_current_contract(self):
        self.assertEqual(foreign_contract_problems(self.grammar, self.ast), [])

    def test_multiple_short_items_are_rejected(self):
        bad = self.grammar.replace('foreign-body\n    ::= foreign-item', 'foreign-body\n    ::= foreign-item , { required-separation , foreign-item }')
        self.assertTrue(foreign_contract_problems(bad, self.ast))

    def test_foreign_rhs_cannot_become_mud_expression(self):
        bad = self.grammar.replace('::= FOREIGN_EXPRESSION', '::= expression')
        self.assertTrue(foreign_contract_problems(bad, self.ast))

    def test_exports_cannot_gain_mutable_slots(self):
        bad = self.ast.replace('ForeignValueExport(variable_name name', 'ForeignValueExport(flag mutable, variable_name name')
        self.assertTrue(foreign_contract_problems(self.grammar, bad))

    def test_foreign_text_and_rhs_origin_cannot_be_lost(self):
        bad = self.ast.replace('foreign_code value)', 'expr value)')
        self.assertTrue(foreign_contract_problems(self.grammar, bad))

    def test_preambles_cannot_drop_foreign_items(self):
        bad = self.ast.replace('pure_preamble_statement* preamble', 'local_value_decl* locals')
        self.assertTrue(foreign_contract_problems(self.grammar, bad))

    def test_value_owner_cannot_drop_foreign_statement(self):
        bad = self.ast.replace('| ForeignBlockValueStatement(foreign_block value)', '')
        self.assertTrue(foreign_contract_problems(self.grammar, bad))


if __name__ == "__main__":
    unittest.main()
