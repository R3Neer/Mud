"""Contrast omission boundaries and supplied structural/schema certificates."""
import unittest
from access_schema_witnesses import (
    dependent_demand, emitted_values, tuple_component, project_input,
    initialization_admitted,
)


class AccessSchemaWitnesses(unittest.TestCase):
    def test_absence_skips_only_pending_dependent_work(self):
        self.assertEqual(dependent_demand(['normal', 'omit', 'fault']), ('omit', 2))
        self.assertEqual(dependent_demand(['fault', 'omit']), ('fault', 1))
        # A subsequent statement has its own independent demand boundary.
        self.assertEqual(dependent_demand(['normal']), ('normal', 1))

    def test_omitted_emission_is_not_a_normal_empty_member(self):
        self.assertEqual(emitted_values([('normal', []), ('omit', None), ('normal', 3)]), [[], 3])
        with self.assertRaises(ValueError):
            emitted_values([('fault', None)])

    def test_static_tuple_position_determines_one_complete_type(self):
        self.assertEqual(tuple_component(['Int', 'String'], '*'), 'String')
        self.assertEqual(tuple_component(['Int', 'String'], 1), 'Int')
        for bad in [0, 3, 'dynamic', True]:
            with self.assertRaises(ValueError):
                tuple_component(['Int', 'String'], bad)

    def test_input_projection_relabels_without_casting_components(self):
        args = (['departure', 'arrival'], ['City', 'City'], ['origin', 'destination'], ['City', 'City'], [1, 2])
        self.assertEqual(project_input(*args), (('origin', 1), ('destination', 2)))
        # Different outer alias names disappear, but component types do not.
        with self.assertRaises(ValueError):
            project_input(['a', 'b'], ['City', 'Town'], ['x', 'y'], ['City', 'City'], [1, 2])

    def test_exact_keys_have_the_same_projected_equality_basis(self):
        left = project_input(['a', 'b'], ['Int', 'Int'], ['x', 'y'], ['Int', 'Int'], [3, 4])
        right = project_input(['c', 'd'], ['Int', 'Int'], ['x', 'y'], ['Int', 'Int'], [3, 4])
        self.assertEqual({left: 'found'}[right], 'found')

    def test_abstract_deferral_does_not_admit_incomplete_concrete_schema(self):
        self.assertTrue(initialization_admitted(True, ['root.a', 'root.b'], ['root.a']))
        self.assertFalse(initialization_admitted(False, ['root.a', 'root.b'], ['root.a']))
        self.assertTrue(initialization_admitted(False, ['root.a', 'root.a'], ['root.a']))
