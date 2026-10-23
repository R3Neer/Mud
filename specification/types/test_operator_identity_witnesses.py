"""Finite supplied quotient-graph certificates, not a Mud signature encoder.

Labels, symbolic normalization, binders, visibility and bisimulation quotients
are premises supplied by these fixtures; no source or contract normalization
is implemented here.
"""
import itertools
import json
import unittest


def canonical_supplied_graph(nodes):
    """Exhaustive numbering certificate for a small already-normalized graph."""
    encodings = []
    for rest in itertools.permutations(range(1, len(nodes))):
        order = (0,) + rest
        numbers = {old: new for new, old in enumerate(order)}
        graph = []
        for old in order:
            tag, labels, edges = nodes[old]
            graph.append([tag, labels, sorted([label, numbers[target]] for label, target in edges)])
        encodings.append(json.dumps(graph, ensure_ascii=True, separators=(',', ':')))
    return min(encodings)


class OperatorIdentityWitnesses(unittest.TestCase):
    def test_numbering_and_recursive_edges(self):
        first = [('tuple', ['named'], [('field:x', 1), ('field:y', 2)]),
                 ('nominal', ['alias::A'], [('argument:0', 2)]),
                 ('nominal', ['alias::B'], [('argument:0', 1)])]
        renumbered = [('tuple', ['named'], [('field:y', 1), ('field:x', 2)]),
                      ('nominal', ['alias::B'], [('argument:0', 2)]),
                      ('nominal', ['alias::A'], [('argument:0', 1)])]
        self.assertEqual(canonical_supplied_graph(first), canonical_supplied_graph(renumbered))

    def test_unordered_alternatives_and_ordered_positions(self):
        union = [('union', [], [('alternative', 1), ('alternative', 2)]),
                 ('basic', ['Int'], []), ('basic', ['String'], [])]
        reverse = [('union', [], [('alternative', 2), ('alternative', 1)]),
                   ('basic', ['String'], []), ('basic', ['Int'], [])]
        self.assertEqual(canonical_supplied_graph(union), canonical_supplied_graph(reverse))
        ordered = [('tuple', ['positional'], [('0', 1), ('1', 2)]), *union[1:]]
        swapped = [('tuple', ['positional'], [('0', 2), ('1', 1)]), *union[1:]]
        self.assertNotEqual(canonical_supplied_graph(ordered), canonical_supplied_graph(swapped))

    def test_nominal_domain_shape_and_binder_labels(self):
        def leaf(tag, labels):
            return canonical_supplied_graph([(tag, labels, [])])
        self.assertNotEqual(leaf('nominal', ['alias::A']), leaf('nominal', ['alias::B']))
        self.assertNotEqual(leaf('domain', ['rule::P']), leaf('domain', ['rule::Q']))
        self.assertNotEqual(leaf('many', [1, 1, 'readonly']), leaf('many', [2, 2, 'readonly']))
        # Renamed binders have already been resolved to the same supplied slot.
        self.assertEqual(leaf('binder', [0, 1]), leaf('binder', [0, 1]))
        self.assertNotEqual(leaf('binder', [0, 1]), leaf('binder', [1, 1]))

    def test_escaped_labels_round_trip_without_delimiter_collision(self):
        for label in ['a,b', 'a\"b', 'a\\b', 'a::b~c', 'á', '\U0001f600', '\n']:
            encoded = canonical_supplied_graph([('label', [label], [])])
            self.assertEqual(json.loads(encoded)[0][1][0], label)
            self.assertTrue(encoded.isascii())
        self.assertNotEqual(canonical_supplied_graph([('label', ['a,b'], [])]),
                            canonical_supplied_graph([('label', ['a', 'b'], [])]))


if __name__ == '__main__':
    unittest.main()
