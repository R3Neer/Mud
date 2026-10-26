"""Preclassified fixture tokens and structural projection contracts, not a parser."""
from pathlib import Path
import re
import unittest

from specification.grammar.ebnf_analysis import grammar_trees, lower_to_bnf, recognises

ROOT = Path(__file__).resolve().parents[2]


class SelectorPatternSyntaxContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'specification/grammar/mud.ebnf').read_text(encoding='utf-8')
        cls.bnf = lower_to_bnf(grammar_trees(cls.source))
        cls.words = set(re.findall(r'"([A-Za-z_][A-Za-z_0-9]*)"', cls.source))

    def accepts(self, start, fixture):
        raw = re.findall(r'-->|:=|==|!=|>=|<=|->|\.\.|[A-Za-z_]\w*|\d+|[^\s]', fixture)
        tokens = [('EXACT_NUMBER_LITERAL' if token.isdigit() else
                   '"' + token + '"' if token in self.words or not token[0].isalnum()
                   else 'IDENTIFIER') for token in raw]
        return recognises(self.bnf, start, tokens)

    def test_tuple_field_and_nested_patterns(self):
        for fixture in ('(x,x)', '(0,y)', '(-1,y)', '(false,x)',
                        'Impact { damage: > 0, target: victim }',
                        'Impact { nested: (x,x) }', '(x, [y])'):
            self.assertTrue(self.accepts('structural-selector-pattern', fixture), fixture)

    def test_exact_collection_and_cons_forms(self):
        for fixture in ('[]', '[x]', '[x,y]', '[[]]', 'x:resto',
                        'x:y:resto', '(x:resto)', '0:resto'):
            start = 'match-pattern' if fixture == '(x:resto)' else 'structural-selector-pattern'
            self.assertTrue(self.accepts(start, fixture), fixture)

    def test_patterns_remain_branch_selectors(self):
        for fixture in ('(x,x) --> x', '[] --> 0', 'empty --> 0', '[empty] --> 0', 'x:resto --> x',
                        'Impact { active: false } --> 0',
                        '(x,y) and x > y --> x', 'true --> 1', '(false) --> 0',
                        '== (a,b) --> 1', '== [a,b] --> 1'):
            self.assertTrue(self.accepts('mapping-expression', fixture), fixture)

    def test_no_new_local_or_traversal_bindings_or_slice_dsl(self):
        for fixture in ('[x]', 'x:resto', 'Impact { target: x }'):
            self.assertFalse(self.accepts('binding-pattern', fixture), fixture)
        self.assertTrue(self.accepts('binding-pattern', '(x,y)'))
        self.assertFalse(self.accepts('local-pattern-declaration', 'let [x] = items'))
        self.assertFalse(self.accepts('postfix-expression', 'items[1:3:2]'))

    def test_cons_recurses_on_right_and_projection_retains_pattern_tree(self):
        body = self.source.split('\nmatch-pattern\n', 1)[1].split(';', 1)[0]
        self.assertIn('match-atom , [ ":" , match-pattern ]', body)
        ast = (ROOT / 'specification/syntax/mud-surface-ast.asdl').read_text(encoding='utf-8')
        for fragment in ('SelectorPattern(match_pattern value)',
                         'ConsMatch(match_pattern head, match_pattern tail)',
                         'CaptureMatch(variable_name name)', 'CollectionMatch(match_pattern* members)',
                         'PropertyMatch(declared_type type, match_field* fields)'):
            self.assertIn(fragment, ast)
        hir = (ROOT / 'specification/names/mud-nominal-hir.asdl').read_text(encoding='utf-8')
        self.assertIn('selector-capture', hir)
        self.assertIn('pattern-equality', hir)

    def test_malformed_pattern_delimiters_and_fields(self):
        for fixture in ('[x,]', 'x:', '(x,y', 'Impact { target x }', 'Impact { target: }'):
            self.assertFalse(self.accepts('structural-selector-pattern', fixture), fixture)


if __name__ == '__main__':
    unittest.main()
