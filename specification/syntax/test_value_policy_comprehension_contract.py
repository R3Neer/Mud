"""Bounded preclassified-token witnesses; not a Mud scanner or typechecker."""
from pathlib import Path
import re
import unittest

from specification.grammar.ebnf_analysis import grammar_trees, lower_to_bnf, recognises

ROOT = Path(__file__).resolve().parents[2]


class ValuePolicyComprehensionContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = (ROOT / 'specification/grammar/mud.ebnf').read_text(encoding='utf-8')
        cls.bnf = lower_to_bnf(grammar_trees(source))
        cls.words = set(re.findall(r'"([A-Za-z_][A-Za-z_0-9]*)"', source))

    def accepts(self, start, source):
        raw = re.findall(r'-->|:=|==|!=|>=|<=|\+=|-=|->|\.\.|[A-Za-z_]\w*|\d+|[^\s]', source)
        tokens = []
        for token in raw:
            if token == ';':
                tokens.append('TERMINATOR')
            elif token.isdigit():
                tokens.append('EXACT_NUMBER_LITERAL')
            elif token in self.words or not token[0].isalnum():
                tokens.append('"' + token + '"')
            else:
                tokens.append('IDENTIFIER')
        return recognises(self.bnf, start, tokens)

    def test_constructor_calls_keep_ordinary_argument_syntax(self):
        for source in ('Vector2(1, 2)', 'Vector2(x = 1, y = 2)', 'Defaults()',
                       '(Pair with Num)(1, 2)'):
            self.assertTrue(self.accepts('postfix-expression', source), source)
        # Semantic construction later rejects mixed arguments; ordinary call AST retains them.
        self.assertTrue(self.accepts('postfix-expression', 'Vector2(1, y = 2)'))
        self.assertFalse(self.accepts('top-level-declaration', 'let f: Num --> Num = _ --> value'))

    def test_shared_selector_locals_retain_block_syntax(self):
        self.assertTrue(self.accepts('mapping-expression',
            '{ let adjusted := .power - .armor; adjusted > 0 } --> adjusted'))
        self.assertFalse(self.accepts('mapping-expression',
            '{ let adjusted = .power - .armor; adjusted > 0 } --> adjusted'))

    def test_alias_stored_components_require_let(self):
        for source in ('let x: Num', 'let x: Num = 0', 'let x: _ = 0'):
            self.assertTrue(self.accepts('component-declaration', source))
        for source in ('x: Num', 'x: Num = 0', 'mut x: Num', 'let x = 0'):
            self.assertFalse(self.accepts('component-declaration', source))
        self.assertTrue(self.accepts('inherited-default-override', 'x = 0'))
        self.assertFalse(self.accepts('inherited-default-override', 'let x = 0'))

    def test_stored_markers_and_partial_annotations(self):
        for source in ('let x = item', 'mut x = item', 'let x: _ = item',
                       'let x in Items = item', 'mut x [* ordered] = empty',
                       'let x: Box with _ = item',
                       'let f: Person --> _ [ordered] = _ --> .name'):
            with self.subTest(source=source):
                self.assertTrue(self.accepts('local-stored-declaration', source))
        self.assertFalse(self.accepts('local-stored-declaration', 'x: _ = item'))
        self.assertFalse(self.accepts('local-stored-declaration', 'mut x := item'))

    def test_derived_and_positional_bindings_require_let(self):
        self.assertTrue(self.accepts('local-calculated-declaration', 'let x := item'))
        self.assertFalse(self.accepts('local-calculated-declaration', 'x := item'))
        self.assertTrue(self.accepts('local-pattern-declaration', 'let (x, _) = item'))
        self.assertFalse(self.accepts('local-pattern-declaration', 'mut (x, y) = item'))

    def test_executable_and_result_separators(self):
        self.assertTrue(self.accepts('local-for-each', 'foreach x in items : total += x'))
        self.assertFalse(self.accepts('local-for-each', 'for each x in items : total += x'))
        self.assertFalse(self.accepts('local-for-each', 'foreach x in items --> x'))
        self.assertTrue(self.accepts('comprehension-expression', 'foreach x in items --> x * 2'))
        self.assertTrue(self.accepts('comprehension-expression', 'foreach x in items if x > 0 --> x'))
        self.assertFalse(self.accepts('comprehension-expression', 'foreach x in items : x'))

    def test_selector_shorthand_stays_in_branch_position(self):
        for source in ('== expected --> result', '!= expected --> result',
                       'not expected --> result', '> limit --> result',
                       'is Person --> result', 'iis Person --> result',
                       '== Low or == Medium --> result',
                       '.age >= 18 and .hasPermit --> result'):
            with self.subTest(source=source):
                self.assertTrue(self.accepts('mapping-expression', source))
        self.assertFalse(self.accepts('comparison-expression', '== expected'))

    def test_input_is_not_a_contextual_token(self):
        lex = (ROOT / 'specification/grammar/mud-lexico.ebnf').read_text(encoding='utf-8')
        contextual = lex.split('contextual-word\n    ::=')[1].split(';')[0]
        self.assertNotIn('"value"', contextual)
        self.assertNotIn('"each"', lex.split('keyword-word\n    ::=')[1].split(';')[0])


if __name__ == '__main__':
    unittest.main()
