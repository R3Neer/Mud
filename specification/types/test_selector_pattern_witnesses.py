"""Contrasting supplied selector certificates; not executed Mud programs."""
import unittest

from selector_pattern_witnesses import (
    ContractError, FieldFault, Record, Sequence, admitted,
    available_result_names, match_certificate, selector_literal_or_predicate,
)

C = lambda name: ('capture', name)
L = lambda value: ('literal', value)
T = lambda *items: ('tuple', items)
S = lambda *items: ('collection', items)
D = ('discard',)


class SelectorPatternWitnesses(unittest.TestCase):
    def test_repeated_capture_binds_once_and_tests_complete_equality(self):
        self.assertEqual(match_certificate(T(C('x'), C('x')), (4, 4)), {'x': 4})
        self.assertIsNone(match_certificate(T(C('x'), C('x')), (4, 5)))
        self.assertEqual(match_certificate(T(D, D), (4, 5)), {})
        self.assertEqual(match_certificate(T(C('x'), C('x')), ((1, 2), (1, 2))), {'x': (1, 2)})

    def test_unsupported_equality_is_not_a_failed_match(self):
        with self.assertRaises(ContractError):
            match_certificate(T(C('x'), C('x')), ('policy', 'policy'), equality_proved=False)
        # Admission remains independent of whether a sample will demand a comparison.
        with self.assertRaises(ContractError):
            admitted(needs_equality=True, equality_proved=False)

    def test_captures_do_not_shadow_or_become_outer_value_tests(self):
        with self.assertRaises(ContractError):
            match_certificate(T(C('x'), D), (1, 2), outer_names={'x'})
        self.assertEqual(match_certificate(T(L(1), C('y')), (1, 2), outer_names={'x'}), {'y': 2})

    def test_boolean_literals_test_values_and_computed_bool_is_predicate(self):
        self.assertTrue(selector_literal_or_predicate(literal=False, input_value=False))
        self.assertFalse(selector_literal_or_predicate(literal=False, input_value=True))
        self.assertFalse(selector_literal_or_predicate(literal=True, input_value=1))
        self.assertTrue(selector_literal_or_predicate(literal=None, input_value=False, predicate_result=True))
        self.assertEqual(match_certificate(T(L(False), C('x')), (False, 9)), {'x': 9})
        with self.assertRaises(ContractError):
            selector_literal_or_predicate(literal=None, input_value=False)
        with self.assertRaises(ContractError):
            selector_literal_or_predicate(literal=1, input_value=False)

    def test_empty_singleton_and_nested_empty_without_order(self):
        self.assertEqual(match_certificate(S(), Sequence(())), {})
        self.assertIsNone(match_certificate(S(), Sequence((Sequence(()),))))
        self.assertEqual(match_certificate(S(S()), Sequence((Sequence(()),))), {})
        self.assertEqual(match_certificate(S(C('x')), Sequence((8,))), {'x': 8})

    def test_multiple_positions_require_static_not_merely_actual_order(self):
        for value in (Sequence((1, 2)), Sequence((1, 2), ordered=True)):
            with self.assertRaises(ContractError):
                match_certificate(S(C('x'), C('y')), value)
        self.assertEqual(match_certificate(S(C('x'), C('y')), Sequence((1, 2), True, True)),
                         {'x': 1, 'y': 2})
        self.assertIsNone(match_certificate(S(C('x'), C('y')), Sequence((1, 2, 3), True, True)))

    def test_cons_right_nesting_tail_empty_and_member_nesting(self):
        pattern = ('cons', C('x'), ('cons', C('y'), C('resto')))
        value = Sequence((1, 2, 3), True, True, True)
        env = match_certificate(pattern, value)
        self.assertEqual(env, {'x': 1, 'y': 2, 'resto': Sequence((3,), True, True, True)})
        self.assertIsNone(match_certificate(pattern, Sequence((1,), True, True)))
        self.assertEqual(match_certificate(('cons', C('x'), C('resto')), Sequence((1,), True, True))['resto'].items, ())
        nested = Sequence((Sequence((1, 2)), Sequence((3,))), True, True)
        self.assertEqual(match_certificate(('cons', C('x'), C('resto')), nested)['x'], Sequence((1, 2)))

    def test_fields_keep_nominal_membership_and_require_visibility(self):
        value = Record(frozenset({'Impact', 'SpecialImpact'}), (('damage', 3), ('target', 'enemy')), frozenset({'damage', 'target'}))
        pattern = ('fields', 'Impact', (('damage', ('test', True)), ('target', C('victim'))))
        self.assertEqual(match_certificate(pattern, value), {'victim': 'enemy'})
        self.assertIsNone(match_certificate(('fields', 'Other', ()), value))
        with self.assertRaises(ContractError):
            match_certificate(('fields', 'Impact', (('private', D),)), value)
        with self.assertRaises(ContractError):
            match_certificate(('fields', 'Impact', (('target', D), ('target', D))), value)

    def test_failed_match_rolls_back_bindings_and_short_circuits_fields(self):
        pattern = T(C('x'), L(0))
        self.assertIsNone(match_certificate(pattern, (8, 1)))
        self.assertEqual(match_certificate(pattern, (9, 0)), {'x': 9})
        value = Record(frozenset({'Impact'}), (('first', 1), ('later', FieldFault('derived field'))), frozenset({'first', 'later'}))
        self.assertIsNone(match_certificate(('fields', 'Impact', (('first', L(0)), ('later', D))), value))
        with self.assertRaises(FieldFault):
            match_certificate(('fields', 'Impact', (('first', L(1)), ('later', C('x')))), value)

    def test_only_definite_names_can_reach_result(self):
        self.assertEqual(available_result_names([{'x': 1, 'local': 2}, {'x': 1}]), frozenset({'x'}))
        self.assertEqual(available_result_names([{'x': 1}, {}]), frozenset())
        self.assertEqual(available_result_names([{'x': 1}, {'x': 2}]), frozenset())
        self.assertEqual(available_result_names([]), frozenset())

    def test_complete_collection_comparison_uses_supplied_equality_contract(self):
        a = Sequence((1, 2), True, True, True)
        b = Sequence((1, 2), True, False, False)
        eq = lambda left, right: left.items == right.items
        self.assertEqual(match_certificate(T(C('x'), C('x')), (a, b), equality_test=eq), {'x': a})


if __name__ == '__main__':
    unittest.main()
