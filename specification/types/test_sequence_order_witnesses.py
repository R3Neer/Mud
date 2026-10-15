"""Contrast sequence order and contextual whole/member keys with fixed premises."""
import unittest

from sequence_order_witnesses import (
    establish_order, value_key, extremum_witness, replace_association,
)


class SequenceOrderWitnesses(unittest.TestCase):
    def test_bare_order_never_selects_a_numeric_comparator(self):
        self.assertEqual(establish_order([3, 1, 2]), [3, 1, 2])
        self.assertEqual(establish_order([3, 1, 2], key=lambda x: x), [1, 2, 3])

    def test_explicit_order_does_not_replace_history(self):
        history = ['a', 'b', 'c']
        values = {'a': 3, 'b': 1, 'c': 2}
        sorted_ids = establish_order(history, key=values.get)
        self.assertEqual(sorted_ids, ['b', 'c', 'a'])
        self.assertEqual(establish_order(sorted_ids, history=history), history)
        self.assertEqual(establish_order(['c', 'a'], history=['a', 'c']), ['a', 'c'])

    def test_mapping_preserves_sequence_even_when_value_order_reverses(self):
        self.assertEqual(establish_order([-x for x in [1, 2, 3]]), [-1, -2, -3])

    def test_field_precedence_and_stable_equal_key_ties(self):
        self.assertEqual(value_key([(True, True, True, True)]), 'member')
        rows = [('first', 2), ('second', 1), ('third', 2)]
        self.assertEqual(establish_order(rows, key=lambda x: x[1]),
                         [('second', 1), ('first', 2), ('third', 2)])

    def test_invalid_present_member_never_falls_back_to_whole(self):
        for facts in [(True, False, True, True), (True, True, False, True)]:
            with self.assertRaises(ValueError):
                value_key([facts])

    def test_whole_and_union_interpretation_are_static_requirements(self):
        self.assertEqual(value_key([(False, False, False, True)]), 'whole')
        with self.assertRaises(ValueError):
            value_key([(False, False, False, False)])
        with self.assertRaises(ValueError):
            value_key([(True, True, True, True), (False, False, False, True)])

    def test_extrema_compare_values_instead_of_arbitrary_positions(self):
        self.assertEqual(extremum_witness([3, 1, 2], [True] * 3), [1])
        self.assertEqual(extremum_witness([3, 1, 2], [True] * 3, maximum=True), [3])
        self.assertEqual(extremum_witness([3, 1, 2], [False] * 3), [])

    def test_association_replacement_keeps_position_but_reinsertion_appends(self):
        entries = [(3, 'three'), (1, 'one'), (2, 'two')]
        self.assertEqual(replace_association(entries, 1, 'changed'),
                         [(3, 'three'), (1, 'changed'), (2, 'two')])
        without_one = [entry for entry in entries if entry[0] != 1]
        self.assertEqual(replace_association(without_one, 1, 'new'),
                         [(3, 'three'), (2, 'two'), (1, 'new')])


if __name__ == '__main__':
    unittest.main()
