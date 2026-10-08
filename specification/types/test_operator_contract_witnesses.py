"""Contrasting finite certificates for the static operator selection contract."""
import unittest

from operator_contract_witnesses import (
    SelectionError, Signature, check_local_duplicates,
    resolve_with_fallback, select, select_alternatives,
)


def signature(origin, owner, left, right, result):
    return Signature(origin, owner, (frozenset(left), frozenset(right)), result)


class OperatorContractWitnesses(unittest.TestCase):
    def test_specificity_and_original_inheritance(self):
        base = signature('base', 'Vector2', {'ordinary', 'special'}, {'num'}, 'Vector2')
        child = signature('child', 'SpecialVector', {'special'}, {'num'}, 'SpecialVector')
        self.assertEqual(select([base], ('special', 'num')), base)
        self.assertEqual(select([base, child], ('special', 'num')), child)
        self.assertEqual(select([base, child], ('ordinary', 'num')), base)
        self.assertEqual(base.owner, 'Vector2')
        self.assertEqual(base.result, 'Vector2')

    def test_crossed_specificity_is_ambiguous(self):
        left = signature('left', 'A', {'special'}, {'general', 'special'}, 'R')
        right = signature('right', 'B', {'general', 'special'}, {'special'}, 'R')
        with self.assertRaises(SelectionError):
            select([left, right], ('special', 'special'))

    def test_origin_diamond_deduplication_not_equal_signature_deduplication(self):
        original = signature('origin', 'A', {'a'}, {'b'}, 'R')
        self.assertEqual(select([original, original], ('a', 'b')), original)
        distinct = signature('other', 'B', {'a'}, {'b'}, 'OtherResult')
        with self.assertRaises(SelectionError):
            select([original, distinct], ('a', 'b'))

    def test_local_duplicate_rejected_independently_of_result(self):
        first = signature('first', 'A', {'a'}, {'b'}, 'R')
        second = signature('second', 'A', {'a'}, {'b'}, 'OtherResult')
        with self.assertRaises(SelectionError):
            check_local_duplicates([first, second])

    def test_union_coverage_and_narrowing(self):
        a = signature('a', 'Vector2', {'v2'}, {'num'}, 'Vector2')
        b = signature('b', 'Vector3', {'v3'}, {'num'}, 'Vector3')
        self.assertEqual(select_alternatives([a, b], ({'v2', 'v3'}, {'num'})),
                         frozenset({'Vector2', 'Vector3'}))
        with self.assertRaises(SelectionError):
            select_alternatives([a], ({'v2', 'v3'}, {'num'}))
        self.assertEqual(select_alternatives([a], ({'v2'}, {'num'})), frozenset({'Vector2'}))

    def test_direct_priority_and_ambiguity_never_falls_back(self):
        direct = signature('direct', 'Vector2', {'v'}, {'whole-pair'}, 'Vector2')
        reads = []
        def builtin():
            reads.append('builtin')
            return 'builtin'
        def lifted():
            reads.append('lifted')
            return 'lifted'
        self.assertEqual(resolve_with_fallback([direct], ('v', 'whole-pair'), builtin, lifted), direct)
        self.assertEqual(reads, [])
        competing = signature('other', 'OtherOwner', {'v'}, {'whole-pair'}, 'R')
        with self.assertRaises(SelectionError):
            resolve_with_fallback([direct, competing], ('v', 'whole-pair'), builtin, lifted)
        self.assertEqual(reads, [])
        self.assertEqual(resolve_with_fallback([], ('v', 'whole-pair'), builtin, lifted), 'builtin')
        self.assertEqual(reads, ['builtin'])
        self.assertEqual(resolve_with_fallback([], ('v', 'whole-pair'), None, lifted), 'lifted')

    def test_nominal_alias_and_dimension_are_not_representation_arguments(self):
        scalar = signature('scalar', 'Vector2', {'v'}, {'num'}, 'Vector2')
        self.assertIsNone(select([scalar], ('v', 'Scale')))
        self.assertIsNone(select([scalar], ('v', 'Length')))


if __name__ == '__main__':
    unittest.main()
