"""Supplied finite call/impact certificates, without Mud source analysis."""
import unittest


def supplied_graph(entries, transfer):
    pending, seen, edges = list(entries), set(), {}
    while pending:
        key = pending.pop(0)
        if key in seen:
            continue
        seen.add(key)
        children = set(transfer(*key))
        edges[key] = children
        pending.extend(sorted(children, key=repr))
    return edges


def has_cycle(edges):
    done, active = set(), set()
    def visit(node):
        if node in active:
            return True
        if node in done:
            return False
        active.add(node)
        if any(visit(child) for child in edges.get(node, ())):
            return True
        active.remove(node)
        done.add(node)
        return False
    return any(visit(node) for node in edges)


def supplied_dispatch(name, destinations):
    if name == "Dispatch":
        return [(target, ()) for target in destinations]
    if name == "A":
        return [("Dispatch", ("B",))]
    if name == "C":
        return [("Dispatch", ("A",))]
    if name == "Loop":
        return [("Dispatch", ("Loop",))]
    return []


class ContextualCallWitnesses(unittest.TestCase):
    def test_distinct_dispatch_contexts_remove_apparent_cycle(self):
        graph = supplied_graph([("C", ())], supplied_dispatch)
        self.assertFalse(has_cycle(graph))
        self.assertIn(("Dispatch", ("A",)), graph)
        self.assertIn(("Dispatch", ("B",)), graph)
        merged = {}
        for (name, _), children in graph.items():
            merged.setdefault(name, set()).update(child[0] for child in children)
        self.assertTrue(has_cycle(merged))

    def test_conservative_unknown_set_can_still_be_acyclic(self):
        graph = supplied_graph([("Dispatch", ("A", "B"))], supplied_dispatch)
        self.assertFalse(has_cycle(graph))

    def test_real_cycle_survives_context_separation(self):
        graph = supplied_graph([("Dispatch", ("A", "B", "Loop"))], supplied_dispatch)
        self.assertTrue(has_cycle(graph))

    def test_demonstrated_narrowing_changes_only_proven_targets(self):
        upper = {"A", "B", "Loop"}
        narrowed = upper - {"Loop"}
        graph = supplied_graph([("Dispatch", tuple(sorted(narrowed)))], supplied_dispatch)
        self.assertFalse(has_cycle(graph))
        self.assertEqual(upper, {"A", "B", "Loop"})

    def test_absence_does_not_invent_destination(self):
        self.assertEqual(supplied_graph([("Dispatch", ())], supplied_dispatch),
                         {("Dispatch", ()): set()})

    def test_summary_join_substitutes_the_actual_place(self):
        supplied = {"A": {("receiver", "balance")},
                    "B": {("receiver", "reserve")}}
        joined = {(root.replace("receiver", "Account7"), path)
                  for target in {"A", "B"} for root, path in supplied[target]}
        self.assertEqual(joined, {("Account7", "balance"), ("Account7", "reserve")})

    def test_unknown_key_region_does_not_prove_nonoverlap(self):
        regions = {("Ledger", "*")}
        concrete = ("Ledger", "key3")
        self.assertTrue(any(root == concrete[0] and (path == "*" or path == concrete[1])
                            for root, path in regions))


if __name__ == "__main__":
    unittest.main()
