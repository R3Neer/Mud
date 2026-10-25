"""Counterexamples and finite certificates for order-sensitive arithmetic."""
import unittest

from collection_arithmetic_witnesses import (
    Layer, View, cardinality_bounds, pair_shape, readonly_view,
    result_certificate, selected_pairs,
)


class CollectionArithmeticWitnesses(unittest.TestCase):
    def test_both_ordered_pairs_positions_and_discards_tail(self):
        self.assertEqual(selected_pairs(3, 2, True, True), ((0, 0), (1, 1)))
        self.assertEqual(selected_pairs(2, 3, True, True), ((0, 0), (1, 1)))

    def test_each_other_mode_selects_every_occurrence_pair(self):
        for a, b in ((False, False), (False, True), (True, False)):
            self.assertEqual(set(selected_pairs(2, 3, a, b)),
                             {(i, j) for i in range(2) for j in range(3)})

    def test_ordered_singleton_is_not_broadcast(self):
        self.assertEqual(len(selected_pairs(1, 3, True, True)), 1)
        self.assertEqual(len(selected_pairs(1, 3, False, True)), 3)

    def test_empty_absorbs_in_every_mode(self):
        for a in (False, True):
            for b in (False, True):
                for n, m in ((0, 3), (3, 0), (0, 0)):
                    self.assertEqual(selected_pairs(n, m, a, b), ())
                    self.assertEqual(result_certificate((), {}), ((), True, False))

    def test_occurrences_not_distinct_values_determine_population(self):
        pairs = selected_pairs(2, 2, False, False)
        values, unique, _ = result_certificate(pairs, {p: 7 for p in pairs})
        self.assertEqual(values, (7, 7, 7, 7))
        self.assertFalse(unique)

    def test_unique_operands_can_collide_in_both_modes(self):
        paired = ((0, 0), (1, 1))
        self.assertFalse(result_certificate(paired, {(0, 0): 3, (1, 1): 3})[1])
        pairs = selected_pairs(2, 2, False, False)
        labels = dict(zip(pairs, (11, 12, 12, 13)))
        self.assertFalse(result_certificate(pairs, labels)[1])

    def test_admitted_pair_injectivity_not_global_injectivity(self):
        pairs = selected_pairs(2, 1, False, False)
        # Supplied x*x results on {1,2}: injective here, not over all Int.
        self.assertTrue(result_certificate(pairs, {(0, 0): 1, (1, 0): 4})[1])

    def test_rounding_collision_and_equality_eligibility(self):
        pairs = ((0, 0), (1, 0))
        self.assertFalse(result_certificate(pairs, {p: 'same-rounded-Rum' for p in pairs})[1])
        self.assertFalse(result_certificate(((0, 0),), {(0, 0): 'policy'}, equality=False)[1])

    def test_key_guarantee_needs_valid_noncolliding_result_keys(self):
        pairs = ((0, 0), (1, 1))
        labels = {(0, 0): 'a', (1, 1): 'b'}
        self.assertFalse(result_certificate(pairs, labels, keys={p: 0 for p in pairs}, key_valid=True)[2])
        keys = {(0, 0): 1, (1, 1): 2}
        self.assertFalse(result_certificate(pairs, labels, keys=keys)[2])
        self.assertTrue(result_certificate(pairs, labels, keys=keys, key_valid=True)[2])
        with self.assertRaisesRegex(ValueError, 'Equal values'):
            result_certificate(pairs, {p: 'same' for p in pairs}, keys=keys, key_valid=True)

    def test_discarded_fault_is_not_demanded(self):
        pairs = selected_pairs(1, 2, True, True)
        self.assertEqual(result_certificate(pairs, {(0, 0): 5}, fault_pairs={(0, 1)})[0], (5,))
        with self.assertRaisesRegex(ValueError, 'Selected member'):
            result_certificate(selected_pairs(1, 2, False, True), {}, fault_pairs={(0, 1)})
        with self.assertRaisesRegex(ValueError, 'Operand production'):
            result_certificate((), {}, operand_fault=True)

    def test_nested_layers_choose_modes_independently_and_retain_empty(self):
        a = Layer((Layer(('a', 'b')), Layer(())), True)
        b = Layer((Layer(('x', 'y')), Layer(('z',))), True)
        shaped = pair_shape(a, b)
        self.assertTrue(shaped.ordered)
        self.assertEqual(len(shaped.members), 2)
        self.assertFalse(shaped.members[0].ordered)
        self.assertEqual(len(shaped.members[0].members), 4)
        self.assertEqual(shaped.members[1], Layer(()))

    def test_nested_ordered_rows_zip_without_matrix_contraction(self):
        a = Layer((Layer(('a', 'b'), True),), True)
        b = Layer((Layer(('x', 'y', 'z'), True),), True)
        self.assertEqual(pair_shape(a, b),
                         Layer((Layer((('a', 'x'), ('b', 'y')), True),), True))

    def test_member_base_case_and_scalar_against_nested_layer(self):
        self.assertEqual(pair_shape('a', 'b'), ('a', 'b'))
        self.assertEqual(pair_shape('a', Layer(('x', 'y'), True)),
                         Layer((('a', 'x'), ('a', 'y'))))

    def test_known_and_unknown_mode_bounds(self):
        self.assertEqual(cardinality_bounds((2, 3), (4, 5), both_ordered=True), (2, 3))
        self.assertEqual(cardinality_bounds((2, 3), (4, 5), both_ordered=False), (8, 15))
        self.assertEqual(cardinality_bounds((2, 3), (4, 5), both_ordered=None), (2, 15))
        self.assertEqual(cardinality_bounds((0, 0), (1, None), both_ordered=None), (0, 0))
        self.assertEqual(cardinality_bounds((1, None), (2, 3), both_ordered=True), (1, 3))
        self.assertEqual(cardinality_bounds((1, None), (2, 3), both_ordered=None), (1, None))

    def test_bounds_cover_all_finite_counts_and_modes(self):
        for la in range(3):
            for ua in range(la, 4):
                for lb in range(3):
                    for ub in range(lb, 4):
                        for mode in (True, False, None):
                            low, high = cardinality_bounds((la, ua), (lb, ub), both_ordered=mode)
                            for n in range(la, ua + 1):
                                for m in range(lb, ub + 1):
                                    counts = (min(n, m), n*m) if mode is None else (min(n, m) if mode else n*m,)
                                    self.assertTrue(all(low <= count <= high for count in counts))

    def test_view_hides_guarantees_without_changing_value_order(self):
        source = View(Layer(('a', 'b'), True), True, True)
        general = readonly_view(source)
        self.assertIs(general.value, source.value)
        self.assertFalse(general.order_guaranteed)
        self.assertTrue(general.value.ordered)
        self.assertTrue(source.inner_mut)
        self.assertFalse(general.inner_mut)
        with self.assertRaisesRegex(ValueError, 'Write authority'):
            readonly_view(general, require_mut=True)
        with self.assertRaisesRegex(ValueError, 'Order guarantee'):
            readonly_view(general, require_order=True)
        self.assertEqual(len(selected_pairs(2, 2, general.value.ordered, True)), 2)
        # An inferred copy retains the known contract rather than requesting a view.
        inferred_copy = source
        self.assertTrue(inferred_copy.order_guaranteed)

    def test_malformed_certificates_rejected(self):
        for counts in ((-1, 2), (True, 2)):
            with self.assertRaises(ValueError):
                selected_pairs(*counts, False, False)
        with self.assertRaises(ValueError):
            selected_pairs(1, 2, 'ordered', False)
        with self.assertRaises(ValueError):
            cardinality_bounds((2, 1), (1, 1), both_ordered=True)


if __name__ == '__main__':
    unittest.main()
