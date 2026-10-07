"""Regression checks for stored annotation and binding context boundaries."""
from pathlib import Path
import unittest

from validate_syntax_model import local_contract_problems

ROOT = Path(__file__).resolve().parents[2]


class LocalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grammar = (ROOT / "specification/grammar/mud.ebnf").read_text(encoding="utf-8")
        cls.ast = (ROOT / "specification/syntax/mud-surface-ast.asdl").read_text(encoding="utf-8")

    def test_baseline(self):
        self.assertEqual(local_contract_problems(self.grammar, self.ast), [])

    def test_holes_cannot_leak_into_signatures(self):
        grammar = self.grammar.replace('declared-type\n    ::= type-reference',
                                       'declared-type\n    ::= type-inference-hole | type-reference')
        self.assertTrue(local_contract_problems(grammar, self.ast))

    def test_pure_patterns_cannot_allocate_value_storage(self):
        grammar = self.grammar.replace('positional-binding-pattern , ":=" , value-expression',
                                       'positional-binding-pattern , ":=" , value-body')
        self.assertTrue(local_contract_problems(grammar, self.ast))

    def test_shared_preamble_cannot_admit_mutable_locals(self):
        grammar = self.grammar.replace('      | immutable-local-stored-declaration',
                                       '      | local-stored-declaration')
        self.assertTrue(local_contract_problems(grammar, self.ast))

    def test_quantifier_cannot_lose_discard_or_nested_patterns(self):
        grammar = self.grammar.replace('quantifier , iteration-binding', 'quantifier , variable-name')
        self.assertTrue(local_contract_problems(grammar, self.ast))

    def test_local_pattern_cannot_become_bare_assignment_declaration(self):
        grammar = self.grammar.replace('positional-binding-pattern , ( "=" | ":=" )',
                                       'binding-pattern , ( "=" | ":=" )')
        self.assertTrue(local_contract_problems(grammar, self.ast))

    def test_discard_node_cannot_become_an_ordinary_named_binding(self):
        self.assertTrue(local_contract_problems(self.grammar, self.ast.replace('DiscardBinding', 'NameBinding')))


if __name__ == "__main__":
    unittest.main()
