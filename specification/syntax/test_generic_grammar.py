"""Token-level witnesses for generic factoring and contextual header boundaries.

Names are preclassified IDENTIFIER fixtures. This does not test the Mud scanner,
nominal arity resolution or static admission of a parsed type.
"""
from pathlib import Path
import re
import unittest

from specification.grammar.ebnf_analysis import (
    grammar_trees, left_corner_graph, left_recursion_path, lower_to_bnf, recognises,
)
from validate_syntax_model import generic_contract_problems

ROOT = Path(__file__).resolve().parents[2]


def fixture(source, header=False):
    """Apply the established header nesting classification to fixture tokens."""
    words = re.findall(r'[A-Za-z_][A-Za-z0-9_]*|\d+|===|!==|:=|->|[^\s]', source)
    keywords = {'abstract', 'thing', 'with', 'as', 'action', 'rule', 'look',
                'for', 'on', 'given', 'then', 'after', 'in', 'ordered', 'unique',
                'alias', 'family', '_', 'type', 'Interval'}
    depth, in_header = 0, header
    result = []
    for word in words:
        if in_header and depth == 0 and word in ('for', 'on', 'given', '{', ':=', ':', '='):
            in_header = False
        if word == 'with' and in_header and depth == 0:
            result.append('HEADER_WITH')
        elif word in keywords or not word[0].isalnum():
            result.append('"' + word + '"')
        elif word.isdigit():
            result.append('EXACT_NUMBER_LITERAL')
        else:
            result.append('IDENTIFIER')
        if word in ('(', '['):
            depth += 1
        elif word in (')', ']'):
            depth -= 1
    return result


class GenericGrammarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'specification/grammar/mud.ebnf').read_text(encoding='utf-8')
        cls.ast = (ROOT / 'specification/syntax/mud-surface-ast.asdl').read_text(encoding='utf-8')
        cls.lexicon = (ROOT / 'specification/grammar/mud-lexico.ebnf').read_text(encoding='utf-8')
        cls.bnf = lower_to_bnf(grammar_trees(cls.source))

    def admits(self, start, source, header=False):
        return recognises(self.bnf, start, fixture(source, header))

    def test_generic_nodes_have_no_indirect_left_recursion(self):
        graph = left_corner_graph(self.source)
        for name in ('generic-argument', 'generic-type-application', 'callable-type',
                     'stored-generic-argument', 'stored-generic-type-application',
                     'stored-callable-type'):
            with self.subTest(production=name):
                self.assertEqual(left_recursion_path(graph, name), [])

    def test_old_postfix_cycle_is_detected(self):
        for prefix in ('', 'stored-'):
            mutated = self.source.replace(
                prefix + 'postfix-generic-type-application\n    ::= ' + prefix + 'generic-argument-head',
                prefix + 'postfix-generic-type-application\n    ::= ' + prefix + 'generic-argument')
            mutated = mutated.replace(
                prefix + 'generic-argument\n    ::= ' + prefix + 'generic-argument-head , { generic-constructor | ' + prefix + 'callable-type-suffix }',
                prefix + 'generic-argument\n    ::= ' + prefix + 'declared-type | "(" , ' + prefix + 'generic-union-argument , ")"')
            with self.subTest(context=prefix):
                self.assertTrue(generic_contract_problems(mutated, self.ast, self.lexicon))

    def test_reflected_primary_cannot_reintroduce_cycle(self):
        mutated = self.source.replace(
            '    ::= generic-family-member\n      | explicit-generic-type-application',
            '    ::= generic-family-member\n      | generic-type-application')
        self.assertTrue(generic_contract_problems(mutated, self.ast, self.lexicon))

    def test_ordinary_parameter_with_is_detected(self):
        mutated = self.source.replace('::= HEADER_WITH , type-parameter-list', '::= "with" , type-parameter-list')
        self.assertTrue(generic_contract_problems(mutated, self.ast, self.lexicon))

    def test_application_cannot_consume_parameter_boundary(self):
        mutated = self.source.replace('generic-constructor , "with" , generic-argument-list',
                                      'generic-constructor , HEADER_WITH , generic-argument-list')
        self.assertTrue(generic_contract_problems(mutated, self.ast, self.lexicon))

    def test_explicit_postfix_nested_product_union_and_callable_arguments(self):
        for source in ('Box with Cat', 'Cat Box', 'Pair with Cat, Dog', '(Cat, Dog) Pair',
                       '(Nat, Nat) Wrapper', 'Cat Box Wrapper', 'Box with (Nat | Text)',
                       'Box with (Pair with Cat, Dog)', '(Box with Cat) Wrapper',
                       'Cat.action() Box', 'Box with Cat.action()',
                       '(Cat Box).action() Wrapper', 'Cat Box.action() Wrapper',
                       'item~type Box', 'Nat Interval'):
            with self.subTest(source=source):
                self.assertTrue(self.admits('generic-type-application', source))

    def test_holes_remain_stored_annotation_only(self):
        for source in ('Box with _', '_ Box', 'Box with (_ | Cat)', '(_ Box).action()'):
            with self.subTest(source=source):
                self.assertTrue(self.admits('stored-declared-type', source))
                self.assertFalse(self.admits('declared-type', source))

    def test_direct_outer_shape_cannot_be_an_argument(self):
        self.assertFalse(self.admits('generic-type-application', 'Box with (Cat [*])'))
        self.assertFalse(self.admits('generic-type-application', 'Box with (Cat in Items)'))
        self.assertTrue(self.admits('type-expression', 'Box with Cat [*]'))

    def test_header_boundary_cannot_be_swallowed_by_ancestor_or_bound(self):
        self.assertTrue(self.admits('thing-declaration', 'abstract thing X as Base with T', True))
        self.assertFalse(self.admits('nominal-type', 'Base with T', True))
        self.assertFalse(self.admits('generic-bound-list', 'Base with U', True))
        self.assertTrue(self.admits('thing-declaration', 'abstract thing X with T as Base with U', True))
        self.assertTrue(self.admits('nominal-type', 'Base with T'))

    def test_delimited_and_postfix_ancestors_and_bounds(self):
        for source in ('abstract thing X as (Base with T) with T',
                       'abstract thing X as [Base with T] with T',
                       'abstract thing X as T Base with T',
                       'abstract thing X with T as (Base with U) with U',
                       'abstract thing X with T as [Base with U] with U'):
            with self.subTest(source=source):
                self.assertTrue(self.admits('thing-declaration', source, True))

    def test_header_boundary_also_blocks_reflected_application(self):
        source = 'abstract thing X as Box with T~type Wrapper'
        self.assertFalse(self.admits('thing-declaration', source, True))
        self.assertTrue(self.admits('thing-declaration',
                                   'abstract thing X as (Box with T~type Wrapper)', True))

    def test_header_view_ends_before_representation_and_signature(self):
        self.assertTrue(self.admits('alias-declaration', 'alias A with T := Box with T', True))
        self.assertTrue(self.admits('alias-declaration', 'alias A := Box with Cat', True))
        self.assertTrue(self.admits('action-declaration',
                                   'action A with T given x: Box with T { then Run() }', True))

    def test_postfix_expression_and_applied_family_members(self):
        for source in ('Cat Box', '(Cat, Dog) Pair', 'Cat Slot.Empty',
                       '(Cat Slot).Empty', '(Slot with Cat).Empty',
                       'Slot with Cat.Empty', '(a, b).Equal() with Person',
                       'Cat.action() Box', 'Cat Box.action() Wrapper',
                       '(Cat.action()) Box', '(Cat [*], Dog) Wrapper',
                       '(Cat in Animals, Dog) Wrapper', '(Nat | Text) Box',
                       '(Cat [*], Dog) Pair.action() Wrapper',
                       '(key: Cat, value: Dog) Wrapper',
                       '(Cat -> Dog, Nat) Wrapper',
                       '(Cat, Dog).action() Box'):
            with self.subTest(source=source):
                self.assertTrue(self.admits('postfix-expression', source))

    def test_nullable_prefix_analysis(self):
        graph = left_corner_graph('a ::= [ "x" ] , b ; b ::= a | "y" ;')
        self.assertTrue(left_recursion_path(graph, 'a'))
        graph = left_corner_graph('a ::= "x" , b ; b ::= a | "y" ;')
        self.assertEqual(left_recursion_path(graph, 'a'), [])

    def test_recogniser_handles_nullable_completion(self):
        bnf = lower_to_bnf(grammar_trees('a ::= [ "x" ] , [ "y" ] ;'))
        for tokens in ([], ['"x"'], ['"y"'], ['"x"', '"y"']):
            self.assertTrue(recognises(bnf, 'a', tokens))
        self.assertFalse(recognises(bnf, 'a', ['"y"', '"x"']))


if __name__ == '__main__':
    unittest.main()
