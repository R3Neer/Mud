"""Finite supplied truth/fault demand certificates, not source evaluation."""
import unittest


def supplied_demand(kind, labels, ordered=True, compatible_key_order=False):
    """Labels are externally supplied true/false/fault outcomes in semantic order."""
    if not ordered or (kind in ('min', 'max') and not compatible_key_order):
        visited = list(range(len(labels)))
        return visited, "fault" if "fault" in labels else "normal"
    indices = list(range(len(labels)))
    if kind == "max":
        indices.reverse()
    visited = []
    for i in indices:
        visited.append(i)
        if labels[i] == "fault":
            return visited, "fault"
        decisive = labels[i] is True if kind in ("exists", "min", "max") else labels[i] is False
        if kind != "count" and decisive:
            break
    return visited, "normal"


class QuantifierDemandWitnesses(unittest.TestCase):
    def test_ordered_truth_short_circuit(self):
        self.assertEqual(supplied_demand("exists", [True, "fault"]), ([0], "normal"))
        self.assertEqual(supplied_demand("forall", [False, "fault"]), ([0], "normal"))
        self.assertEqual(supplied_demand("exists", ["fault", True]), ([0], "fault"))

    def test_unordered_truth_and_count_do_not_hide_faults(self):
        for kind in ("exists", "forall", "count"):
            self.assertEqual(supplied_demand(kind, [True, "fault"], False), ([0, 1], "fault"))
        self.assertEqual(supplied_demand("count", [True, "fault"]), ([0, 1], "fault"))

    def test_extremum_direction_and_empty_demand(self):
        outcomes = [False, "fault", True]
        self.assertEqual(supplied_demand("min", outcomes, compatible_key_order=True), ([0, 1], "fault"))
        self.assertEqual(supplied_demand("max", outcomes, compatible_key_order=True), ([2], "normal"))
        for kind in ("exists", "forall", "count", "min", "max"):
            self.assertEqual(supplied_demand(kind, []), ([], "normal"))

    def test_bare_sequence_does_not_allow_extremum_short_circuit(self):
        for kind in ('min', 'max'):
            self.assertEqual(supplied_demand(kind, [True, 'fault', False]),
                             ([0, 1, 2], 'fault'))


if __name__ == "__main__":
    unittest.main()
