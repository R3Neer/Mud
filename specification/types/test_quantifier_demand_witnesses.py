"""Finite supplied truth/fault demand certificates, not source evaluation."""
import unittest


def supplied_demand(kind, labels, ordered=True):
    """Labels are externally supplied true/false/fault outcomes in semantic order."""
    if not ordered:
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
        self.assertEqual(supplied_demand("min", outcomes), ([0, 1], "fault"))
        self.assertEqual(supplied_demand("max", outcomes), ([2], "normal"))
        for kind in ("exists", "forall", "count", "min", "max"):
            self.assertEqual(supplied_demand(kind, []), ([], "normal"))


if __name__ == "__main__":
    unittest.main()
