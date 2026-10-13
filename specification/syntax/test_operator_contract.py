"""Preclassified declaration tokens, not overload discovery or a compiler."""
import unittest
from test_generic_grammar import fixture, ROOT
from specification.grammar.ebnf_analysis import grammar_trees, lower_to_bnf, recognises
class OperatorFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.bnf=lower_to_bnf(grammar_trees((ROOT/'specification/grammar/mud.ebnf').read_text(encoding='utf-8')))
    def test_closed_set(self):
        for op in ('+','-','*','/','%','|','&','^','--'):
            tokens=['IDENTIFIER','"'+op+'"','IDENTIFIER','":"','IDENTIFIER','":="','IDENTIFIER']
            self.assertTrue(recognises(self.bnf,'operator-declaration',tokens),op)
        for op in ('==','!=','<','and','has','='):
            self.assertFalse(recognises(self.bnf,'operator-declaration',['IDENTIFIER','"'+op+'"','IDENTIFIER','":="','IDENTIFIER']),op)
    def test_typed_operand_and_unary(self):
        for source in ('a * (factor: Num): Vector2 := a','(factor: Num) * b := b','-a: Vector2 := a','+a := a'):
            self.assertTrue(recognises(self.bnf,'operator-declaration',fixture(source)),source)
    def test_descriptor_metadata_attachment_forms(self):
        for source in (
            'a * (factor: Num): V := a { ~summary = description }',
            'a * (factor: Num): V := { ~summary = description; a }',
            '-a := { ~summary = description; a }',
        ):
            tokens = ['TERMINATOR' if token == '";"' else token for token in fixture(source)]
            self.assertTrue(recognises(self.bnf, 'operator-declaration', tokens), source)
        mixed = 'a * b := { ~summary = description; a } { ~name = title }'
        tokens = ['TERMINATOR' if token == '";"' else token for token in fixture(mixed)]
        self.assertFalse(recognises(self.bnf, 'operator-declaration', tokens))
if __name__=='__main__': unittest.main()
