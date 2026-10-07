"""Finite newline certificates and independently preclassified EBNF fixtures.

This checks supplied grammatical premises, not source scanning/parsing. The
source fragments require review; the existing recogniser checks only tokens.
"""
import json
from pathlib import Path
import unittest

import yaml
from specification.grammar.ebnf_analysis import grammar_trees, lower_to_bnf, recognises

ROOT = Path(__file__).resolve().parents[2]


def boundary(p):
    """Evaluate MUD-SYN-015 over one supplied finite certificate."""
    if p['separator'] == 'semicolon' or p['enclosing_end']:
        return 'separate' if p['current_complete'] else 'error'
    if not p['current_complete']:
        return 'continue' if p['can_extend'] else 'error'
    if p['next_unit_start']:
        return 'separate'
    return 'continue' if p['can_extend'] else 'error'


class NewlineContractWitnesses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = json.loads((ROOT / 'specification/syntax/cases/newline-cases.json').read_text(encoding='utf-8'))
        cls.bnf = lower_to_bnf(grammar_trees((ROOT / 'specification/grammar/mud.ebnf').read_text(encoding='utf-8')))

    def test_contrasting_boundary_certificates(self):
        cases = self.corpus['cases']
        ids = {c['id'] for c in cases}
        self.assertEqual(len(ids), len(cases))
        self.assertTrue({'start-wins-over-extension', 'next-incomplete-assignment',
                         'later-error-keeps-start', 'comments-and-blanks',
                         'semicolon-is-explicit', 'unfinished-at-block-end',
                         'leading-or', 'postfix-member'} <= ids)
        for c in cases:
            with self.subTest(case=c['id']):
                self.assertIn(c['premises']['separator'], ('newline', 'semicolon'))
                for key in ('current_complete', 'next_unit_start', 'can_extend', 'enclosing_end'):
                    self.assertIsInstance(c['premises'][key], bool)
                self.assertEqual(boundary(c['premises']), c['expected_boundary'])

    def test_preclassified_grouping_fixtures(self):
        # Independent EBNF recognition contrasts one joined assignment, two
        # separate statements, ambiguous starts and explicit-separator errors.
        fixtures = [c for c in self.corpus['cases'] if 'tokens' in c]
        self.assertGreaterEqual(len(fixtures), 5)
        for c in fixtures:
            with self.subTest(case=c['id']):
                self.assertEqual(recognises(self.bnf, c['grammar_start'], c['tokens']),
                                 c['expected_acceptance'])

    def test_continued_newline_has_lossless_trivia_kind(self):
        catalogue = yaml.safe_load((ROOT / 'specification/syntax/mud-syntax-kinds.yaml').read_text(encoding='utf-8'))
        kinds = [x['kind'] for x in catalogue['trivia_kinds']]
        self.assertEqual(kinds.count('ContinuationNewlineTrivia'), 1)
        self.assertIn('HorizontalWhitespaceTrivia', kinds)


if __name__ == '__main__':
    unittest.main()
