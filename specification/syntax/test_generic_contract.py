"""Mutation regressions for generic/type syntax boundaries."""
from pathlib import Path
import unittest

from validate_syntax_model import generic_contract_problems

ROOT = Path(__file__).resolve().parents[2]


class GenericSyntaxContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grammar = (ROOT / "specification/grammar/mud.ebnf").read_text(encoding="utf-8")
        cls.ast = (ROOT / "specification/syntax/mud-surface-ast.asdl").read_text(encoding="utf-8")
        cls.lexicon = (ROOT / "specification/grammar/mud-lexico.ebnf").read_text(encoding="utf-8")

    def test_baseline(self):
        self.assertEqual(generic_contract_problems(self.grammar, self.ast, self.lexicon), [])

    def test_type_equality_cannot_become_value_equality(self):
        mutated = self.ast.replace("StructuralTypeEqualityExpr(type_expr left, type_expr right", "StructuralTypeEqualityExpr(expr left, expr right")
        self.assertTrue(generic_contract_problems(self.grammar, mutated, self.lexicon))

    def test_shorter_token_cannot_replace_structural_token(self):
        mutated = self.lexicon.replace(' | "!=="', '')
        self.assertTrue(generic_contract_problems(self.grammar, self.ast, mutated))

    def test_grouped_application_provenance_is_required(self):
        mutated = self.ast.replace("generic_application_form form", "flag inferred_grouping")
        self.assertTrue(generic_contract_problems(self.grammar, mutated, self.lexicon))

    def test_generic_message_is_not_admitted(self):
        mutated = self.ast.replace("MessageDecl(nominal_name name,", "MessageDecl(nominal_name name, generic_parameter* parameters,")
        self.assertTrue(generic_contract_problems(self.grammar, mutated, self.lexicon))


if __name__ == "__main__":
    unittest.main()
