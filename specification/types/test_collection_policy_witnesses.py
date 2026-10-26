"""Finite contrast cases for selector coverage and per-occurrence results."""
import unittest
from collection_policy_witnesses import (
    covers, apply_first, apply_all, comprehension, interval_member, coverage_admitted,
)


class CollectionPolicyWitnesses(unittest.TestCase):
    def test_coverage_requires_all_inputs_or_explicit_residual(self):
        members = ['Low', 'Medium', 'High']
        tests = [lambda x: x == 'Low', lambda x: x == 'Medium']
        self.assertFalse(covers(members, tests))
        self.assertTrue(covers(members, tests, fallback=True))
        tests.append(lambda x: x == 'High')
        self.assertTrue(covers(members, tests))
        self.assertFalse(covers(members + ['Critical'], tests))

    def test_uncovered_zero_admitting_application_is_normal_empty(self):
        selectors = [lambda x: x > 0]
        self.assertTrue(coverage_admitted([-1, 0, 1], selectors, 0))
        self.assertFalse(coverage_admitted([-1, 0, 1], selectors, 1))
        branches = [(selectors[0], lambda x: x)]
        self.assertEqual(apply_first(-1, branches), [])
        self.assertEqual(apply_all(-1, branches), [])

    def test_empty_is_handled_and_never_retries_fallback(self):
        def forbidden(_):
            self.fail('A matching empty result must not invoke fallback')
        branches = [(lambda _: True, lambda _: [])]
        self.assertEqual(apply_first(1, branches, forbidden), [])
        self.assertEqual(apply_all(1, branches, forbidden), [])

    def test_allmatches_aggregates_only_exterior_results(self):
        branches = [(lambda _: True, lambda _: [1, 2]),
                    (lambda _: True, lambda _: [2, 3])]
        self.assertEqual(apply_all(1, branches), [1, 2, 2, 3])
        nested = [(lambda _: True, lambda _: [[1, 2]])]
        self.assertEqual(apply_all(1, nested), [[1, 2]])

    def test_allmatches_fallback_contributes_without_a_wrapper(self):
        self.assertEqual(apply_all(0, [], lambda _: [1, 2]), [1, 2])

    def test_computed_bool_predicate_and_explicit_equality_differ(self):
        # A supplied computed false condition, not a false literal selector.
        condition = lambda _: False
        equal_false = lambda x: x is False
        self.assertFalse(covers([False, True], [condition]))
        self.assertEqual(apply_first(False, [(condition, lambda _: 'match')], lambda _: 'other'), 'other')
        self.assertEqual(apply_first(False, [(equal_false, lambda _: 'match')], lambda _: 'other'), 'match')

    def test_open_boundaries_are_not_closed_by_shorthand(self):
        self.assertFalse(interval_member(1, 1, 10, False, False))
        self.assertTrue(interval_member(2, 1, 10, False, False))
        self.assertFalse(interval_member(10, 1, 10, False, False))
        self.assertTrue(interval_member(10, 1, 10, True, True))

    def test_boolean_results_transform_rather_than_filter(self):
        self.assertEqual(comprehension([1, 2, 3], lambda x: x > 1), [False, True, True])
        self.assertEqual(comprehension([1, 2, 3], lambda x: x, lambda x: x > 1), [2, 3])

    def test_occurrences_order_and_nested_empty_results_survive(self):
        self.assertEqual(comprehension([2, 1, 2], lambda x: x * 2), [4, 2, 4])
        self.assertEqual(comprehension([1, 2], lambda x: [] if x == 1 else [x]), [[], [2]])

    def test_source_is_captured_once_and_faults_propagate(self):
        source = [1, 2]
        def body(x):
            source.append(3)
            return x
        self.assertEqual(comprehension(source, body), [1, 2])
        with self.assertRaises(ZeroDivisionError):
            comprehension([1, 0, 2], lambda x: 1 / x)


if __name__ == '__main__':
    unittest.main()
