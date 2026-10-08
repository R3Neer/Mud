"""Preclassified raise fixtures; no scanner, typechecker or evaluator."""
import unittest
from test_generic_grammar import fixture,ROOT
from specification.grammar.ebnf_analysis import grammar_trees,lower_to_bnf,recognises
class RaiseFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.bnf=lower_to_bnf(grammar_trees((ROOT/'specification/grammar/mud.ebnf').read_text(encoding='utf-8')))
    def test_expression_and_statement_contexts(self):
        tokens=['"raise"','IDENTIFIER']
        for start in ('expression','value-statement','effect','raise-expression'):
            self.assertTrue(recognises(self.bnf,start,tokens),start)
    def test_nested_recovery(self):
        tokens=['"{"','"raise"','IDENTIFIER','"}"','"otherwise"','"then"','IDENTIFIER']
        self.assertTrue(recognises(self.bnf,'value-body',tokens))
    def test_not_declaration_or_missing_payload(self):
        self.assertFalse(recognises(self.bnf,'expression',['"raise"']))
        self.assertFalse(recognises(self.bnf,'top-level-declaration',['"raise"','IDENTIFIER']))
if __name__=='__main__':unittest.main()
