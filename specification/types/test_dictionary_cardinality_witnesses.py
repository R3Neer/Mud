"""Finite owner/cardinality contrasts; no source typechecker or runtime."""
import unittest

from dictionary_cardinality_witnesses import effective_cardinality, admits, checked_interval


class DictionaryCardinalityWitnesses(unittest.TestCase):
    def test_immutable_exact_literal_and_contextual_empty(self):
        for count in (0, 1, 2, 7):
            self.assertEqual(effective_cardinality("immutable-stored", [count, count]),
                             ((count, count), "InferredFromInitializer"))

    def test_dictionary_exterior_and_association_layers_are_independent(self):
        exterior = effective_cardinality("immutable-stored", [1, 1])[0]
        entries = effective_cardinality("immutable-stored", [3, 3])[0]
        self.assertEqual((exterior, entries), ((1, 1), (3, 3)))

    def test_mutable_empty_map_needs_written_zero_admitting_bounds(self):
        ordinary, origin = effective_cardinality("mutable-stored", [0, 0])
        growing, _ = effective_cardinality("mutable-stored", [0, 0], [0, None])
        self.assertEqual(origin, "OrdinaryScalarDefault")
        self.assertFalse(admits([0, 0], ordinary))
        self.assertTrue(admits([0, 0], growing))
        self.assertTrue(admits([2, 2], growing))

    def test_literal_size_does_not_widen_a_receiving_signature(self):
        signature, _ = effective_cardinality("type-only", [2, 2])
        self.assertEqual(signature, (1, 1))
        self.assertFalse(admits([2, 2], signature))
        self.assertTrue(admits([2, 2], [0, None]))

    def test_partial_firstmatch_preserves_zero_without_explicit_minimum(self):
        counts = [0 if x <= 0 else 1 for x in (-3, 0, 4)]
        interval = (min(counts), max(counts))
        self.assertEqual(effective_cardinality("immutable-stored", interval)[0], (0, 1))
        required, _ = effective_cardinality("immutable-stored", interval, [1, 1])
        self.assertFalse(admits(interval, required))

    def test_allmatches_overlap_and_residual_are_not_singleton_by_default(self):
        counts = []
        for x in (-2, 0, 3):
            matches = int(x > 0) + int(x >= 0)
            counts.append(matches if matches else 1)  # supplied scalar residual
        inferred = (min(counts), max(counts))
        self.assertEqual(effective_cardinality("immutable-stored", inferred)[0], (1, 2))
        self.assertFalse(admits(inferred, [1, 1]))

    def test_live_policy_inference_accounts_for_both_state_views(self):
        counts = [int(enabled and x > 0) for enabled in (False, True) for x in (-1, 1)]
        self.assertEqual(effective_cardinality("derived", [min(counts), max(counts)])[0], (0, 1))

    def test_derived_map_keeps_an_interval_not_first_observed_count(self):
        self.assertEqual(effective_cardinality("derived", [0, 10]),
                         ((0, 10), "InferredFromExpression"))

    def test_public_empty_default_needs_a_broad_component_contract(self):
        inferred, _ = effective_cardinality("immutable-stored", [0, 0])
        explicit, _ = effective_cardinality("immutable-stored", [0, 0], [0, None])
        self.assertFalse(admits([3, 3], inferred))
        self.assertTrue(admits([3, 3], explicit))

    def test_nested_dictionary_counts_are_separate_and_written_bounds_win(self):
        inner, _ = effective_cardinality("immutable-stored", [2, 2], [0, 5])
        outer, _ = effective_cardinality("immutable-stored", [3, 3])
        self.assertEqual((inner, outer), ((0, 5), (3, 3)))

    def test_malformed_or_missing_certificates_are_not_inferred_defaults(self):
        for invalid in ([True, 2], [-1, 1], [2, 1], [0, "*"], [0]):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                checked_interval(invalid)
        with self.assertRaises(ValueError):
            effective_cardinality("derived")
        with self.assertRaises(ValueError):
            effective_cardinality("unknown", [1, 1])


if __name__ == "__main__":
    unittest.main()
