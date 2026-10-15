"""Preclassified body-omission witnesses, not a Mud scanner or typechecker."""
from pathlib import Path
import re
import unittest

from specification.grammar.ebnf_analysis import grammar_trees, lower_to_bnf, recognises

ROOT = Path(__file__).resolve().parents[2]


class MagnitudeBodyContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = (ROOT / 'specification/grammar/mud.ebnf').read_text(encoding='utf-8')
        cls.bnf = lower_to_bnf(grammar_trees(source))
        cls.keywords = set(re.findall(r'"([A-Za-z_]\w*)"', source))

    def accepts(self, start, source, eof=False):
        tokens = []
        for token in re.findall(r':=|\.\.|[A-Za-z_]\w*|\d+|[^\s]', source):
            if token == ';':
                tokens.append('TERMINATOR')
            elif token.isdigit():
                tokens.append('EXACT_NUMBER_LITERAL')
            elif token in self.keywords or not token[0].isalnum():
                tokens.append('"' + token + '"')
            else:
                tokens.append('IDENTIFIER')
        if eof:
            tokens.append('EOF')
        return recognises(self.bnf, start, tokens)

    def test_base_and_point_bodies_can_be_omitted_or_empty(self):
        for source in (
            'magnitude Strength',
            'magnitude Strength: Num',
            'magnitude Probability: Num in [0..1]',
            'magnitude Coordinate point over Length',
            'magnitude Clock point over Time in [0..10) cycle',
        ):
            for suffix in ('', ' {}'):
                with self.subTest(source=source, suffix=suffix):
                    self.assertTrue(self.accepts('magnitude-declaration', source + suffix))

    def test_derived_omission_and_nonempty_bodies_remain_valid(self):
        for source in (
            'magnitude Speed := Length / Time',
            'magnitude Speed := Length / Time {}',
            'magnitude Length: Rum { root unit meter {} }',
            'magnitude Coordinate point over Length { ~name = label }',
        ):
            self.assertTrue(self.accepts('magnitude-declaration', source), source)

    def test_omission_does_not_complete_malformed_headers_or_unbrace_contents(self):
        for source in (
            'magnitude', 'magnitude Strength:', 'magnitude Strength in',
            'magnitude Coordinate point over', 'magnitude Clock point over Time cycle',
            'magnitude Length root unit meter {}',
            'magnitude Coordinate point over Length ~name = label',
        ):
            self.assertFalse(self.accepts('magnitude-declaration', source), source)

    def test_complete_declarations_still_need_classified_separation(self):
        self.assertTrue(self.accepts('mud-file',
            'magnitude Length; magnitude Coordinate point over Length', eof=True))
        self.assertFalse(self.accepts('mud-file',
            'magnitude Length magnitude Coordinate point over Length', eof=True))
        self.assertFalse(self.accepts('mud-file',
            'magnitude Length:; magnitude Other', eof=True))


if __name__ == '__main__':
    unittest.main()
