"""Bounded token fixtures, not a Mud scanner/typechecker."""
import unittest
from test_generic_grammar import fixture, ROOT
from specification.grammar.ebnf_analysis import grammar_trees, lower_to_bnf, recognises
class NestedCollectionContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.bnf=lower_to_bnf(grammar_trees((ROOT/'specification/grammar/mud.ebnf').read_text(encoding='utf-8')))
    def test_shapes(self):
        for start in ('type-expression','stored-type-expression'):
            for source in ('Int [3] [2]','(Int [3]) [2]','Int [4] [3] [2]','Int [3 ordered] [2 ordered]','Int [0] [1]'):
                self.assertTrue(recognises(self.bnf,start,['EXACT_INTEGER_LITERAL' if t == 'EXACT_NUMBER_LITERAL' else t for t in fixture(source)]),(start,source))
    def test_generic_boundary(self): self.assertFalse(recognises(self.bnf,'generic-type-application',fixture('Box with (Int [3] [2])')))
    def test_wrapper(self): self.assertIn('NestedCollectionType(type_expr inner)',(ROOT/'specification/syntax/mud-surface-ast.asdl').read_text(encoding='utf-8'))
if __name__=='__main__': unittest.main()
