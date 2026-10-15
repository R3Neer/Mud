"""Boundary tests for the source-only example planner, not Mud execution."""
from pathlib import Path
import shutil
import subprocess
import sys
import json
import tempfile
import unittest

from tooling.examples.spell_metadata import EXAMPLE, Inventory, metadata, check_dictionary_arguments, mask


class SpellMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = Inventory(EXAMPLE)

    def test_every_scenario_is_classified_and_has_an_independent_world(self):
        plan = self.inventory.plan([])
        self.assertEqual(len(plan['worlds']), 50)
        self.assertFalse(plan['executesMud'])
        self.assertEqual(len({w['root'] for w in plan['worlds']}), 50)
        for world in plan['worlds']:
            self.assertEqual(world['tests'], [world['root']])
            self.assertIn('spells.CanSelect', world['activation'])
            self.assertIn('sympathy.ExclusiveSympathy', world['activation'])

    def test_support_is_exactly_eleven_plus_two_plus_one(self):
        expected = {
            'Core': {'world.Entity', 'world.Creature', 'spells.Spellcaster', 'spells.Magic',
                     'spells.CanSelect', 'spells.CanAttempt', 'spells.ConcentrationWithinLimit',
                     'sympathy.TargetUsable', 'sympathy.CanLink', 'sympathy.ExclusiveSympathy',
                     'spells.PublishSpellEvents'},
            'Feedback': {'feedback.FeedbackChannel', 'feedback.PlanSpellFeedback'},
            'LinkEffects': {'sympathy.PrepareLinkEffects'},
        }
        actual = {feature: {name for name, value in self.inventory.support.items() if value==feature}
                  for feature in self.inventory.features}
        self.assertEqual(actual, expected)
        world = self.inventory.activation(self.inventory.tests['scenarios.NoConcentrationRoomRejectsSelection'])
        self.assertIn('fixtures.NoFocus', world)
        self.assertNotIn('fixtures.Player', world)
        self.assertNotIn('fixtures.Turret', world)

    def test_union_selection_and_repeated_concerns(self):
        def roots(cs): return {w['root'] for w in self.inventory.plan(cs)['worlds']}
        self.assertEqual(roots(['Feedback', 'PairAdmission', 'Feedback']), roots(['Feedback']) | roots(['PairAdmission']))
        for concern in ['Feedback', 'PairAdmission', 'Selection']:
            self.assertIn('scenarios.FeedbackModelsARealSympathyCast', roots([concern]))

    def test_explicit_concern_replaces_file_default(self):
        self.assertEqual(self.inventory.checks['scenarios.InversionChangesTheRelationWithoutAnInteractorCache'], {'Contributions'})

    def test_unknown_concern_is_an_error(self):
        with self.assertRaisesRegex(ValueError, 'Unknown requested concern'):
            self.inventory.plan(['Typo'])

    def test_cli_json_and_diagnostics_use_separate_streams(self):
        script = Path(__file__).resolve().parents[1] / 'examples/spell_metadata.py'
        success = subprocess.run([sys.executable, str(script), '--concern', 'Feedback', '--ascii'],
                                 capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(success.returncode, 0, success.stderr)
        self.assertEqual(success.stderr, '')
        self.assertFalse(json.loads(success.stdout)['executesMud'])
        failure = subprocess.run([sys.executable, str(script), '--concern', 'Typo', '--ascii'],
                                 capture_output=True, text=True, encoding='utf-8')
        self.assertNotEqual(failure.returncode, 0)
        self.assertEqual(failure.stdout, '')
        self.assertIn('Unknown requested concern', failure.stderr)

    def test_cli_help_documents_every_operational_option(self):
        script = Path(__file__).resolve().parents[1] / 'examples/spell_metadata.py'
        result = subprocess.run([sys.executable, str(script), '--help'],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        for option in ['--root', '--concern', '--colour', '--ascii']:
            self.assertIn(option, result.stdout)

    def test_compound_resource_is_not_partial_capability(self):
        self.assertEqual(self.inventory.assets['SynchronizedBurst'], {'Audio', 'Visual'})
        self.assertFalse(self.inventory.assets['SynchronizedBurst'] <= {'Audio'})
        self.assertTrue(self.inventory.assets['SynchronizedBurst'] <= {'Audio', 'Visual'})

    def test_dynamic_metadata_and_empty_requirements_are_rejected(self):
        for value in ['[]', '[FeedbackModality.Audio] | [FeedbackModality.Visual]', 'Compute()']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                metadata('~modalities: FeedbackModality [1..* unique] = '+value,
                         'modalities', 'FeedbackModality [1..* unique]', 'FeedbackModality', True)

    def mutate(self, relative, transform):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / 'spell'
        shutil.copytree(EXAMPLE, root)
        path = root / relative
        path.write_text(transform(path.read_text(encoding='utf-8-sig')), encoding='utf-8')
        return root

    def test_missing_metadata_fails_instead_of_empty_selection(self):
        root = self.mutate('scenarios/feedbackCapabilities.mud', lambda s:s.replace(
            '~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Feedback]', ''))
        with self.assertRaisesRegex(ValueError, 'missing checks'):
            Inventory(root)

    def test_unclassified_resource_cannot_disappear_from_inventory(self):
        root = self.mutate('feedback/contracts.mud', lambda s:s.replace('family FeedbackAsset {', 'family FeedbackAsset {\n    Untagged,'))
        with self.assertRaisesRegex(ValueError, 'Every resource member'):
            Inventory(root)

    def test_omitted_support_registration_is_detected(self):
        root = self.mutate('configuration/activationSelection.mud', lambda s:s.replace('CanSelect, CanAttempt', 'CanAttempt'))
        with self.assertRaisesRegex(ValueError, 'Unregistered activation support'):
            Inventory(root)

    def test_called_test_closure_keeps_a_different_concern_and_its_fixtures(self):
        root = self.mutate('scenarios/selection.mud', lambda s:s.replace(
            'then (MagicWorld, Player).SelectSpell(Spell.Sympathy)',
            'then FeedbackSelectedEffectsAreMerged()', 1))
        inventory = Inventory(root)
        worlds = inventory.plan(['Selection'])['worlds']
        world = next(w for w in worlds if w['root']=='scenarios.SelectionReservesConcentrationBeforeLink')
        self.assertIn('scenarios.FeedbackSelectedEffectsAreMerged', world['tests'])
        self.assertIn('fixtures.PlayerFeedback', world['activation'])
        self.assertIn('feedback.PlanSpellFeedback', world['activation'])

    def test_call_cycles_are_rejected(self):
        root = self.mutate('scenarios/selection.mud', lambda s:s.replace(
            'then (MagicWorld, Player).SelectSpell(Spell.Sympathy)',
            'then SelectionReservesConcentrationBeforeLink()', 1))
        with self.assertRaisesRegex(ValueError, 'Cyclic test calls'):
            Inventory(root)

    def test_indirect_test_values_require_a_real_call_graph(self):
        root = self.mutate('scenarios/selection.mud', lambda s:s.replace(
            'then (MagicWorld, Player).SelectSpell(Spell.Sympathy)',
            'then { let indirect = FeedbackSelectedEffectsAreMerged; indirect() }', 1))
        with self.assertRaisesRegex(ValueError, 'Indirect test references'):
            Inventory(root)

    def test_nested_parts_are_not_silently_treated_as_accessible(self):
        root = self.mutate('scenarios/selection.mud', lambda s:s)
        (root/'scenarios/mud.part').write_text('')
        with self.assertRaisesRegex(ValueError, 'one comment-only root part'):
            Inventory(root)

    def test_calls_via_actions_are_not_silently_omitted(self):
        root = self.mutate('spells/selection.mud', lambda s:s.replace(
            'then (magic, caster).EndSpell(spell)',
            'then FeedbackSelectedEffectsAreMerged()', 1))
        with self.assertRaisesRegex(ValueError, 'outside scenario bodies'):
            Inventory(root)

    def test_changed_activation_semantics_require_a_new_supported_template(self):
        root = self.mutate('configuration/activationSelection.mud', lambda s:s.replace(
            'has declaration~activationFeature',
            'has declaration~activationFeature and false'))
        with self.assertRaisesRegex(ValueError, 'Unsupported activation catalogue'):
            Inventory(root)

    def test_tuple_shaped_dictionary_argument_is_not_accepted_as_a_plan(self):
        root = self.mutate('fixtures/feedback.mud', lambda s:s.replace(
            'byStage = [', 'byStage = (', 1).replace('\n        ],', '\n        ),', 1))
        with self.assertRaisesRegex(ValueError, 'not a tuple'):
            Inventory(root)

    def test_grouping_one_association_is_distinct_from_an_association_tuple(self):
        check_dictionary_arguments(mask('byStage = (Stage.Key -> [one, two])'))
        check_dictionary_arguments(mask('byStage = [Stage.A -> [one, two], Stage.B -> [three]]'))
        with self.assertRaisesRegex(ValueError, 'not a tuple'):
            check_dictionary_arguments(mask('byStage = (Stage.A -> [one, two], Stage.B -> [three])'))

    def test_sublook_is_inventoried_and_cannot_hide_test_references(self):
        self.assertEqual(self.inventory.declarations['PlanSympathy'].category, 'sublook')
        root = self.mutate('sympathy/targetPlan.mud', lambda s:s.replace(
            'decision[aim]', 'FeedbackSelectedEffectsAreMerged()'))
        with self.assertRaisesRegex(ValueError, 'outside scenario bodies'):
            Inventory(root)

    def test_layout_changes_do_not_change_activation_template_meaning(self):
        root = self.mutate('configuration/activationSelection.mud', lambda s:s.replace(
            'has declaration~activationFeature', 'has\n        declaration~activationFeature'))
        inventory = Inventory(root)
        self.assertEqual(inventory.plan([]), self.inventory.plan([]))


if __name__ == '__main__':
    unittest.main()
