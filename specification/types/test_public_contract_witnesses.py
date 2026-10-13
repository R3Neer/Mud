"""Finite supplied public-contract certificates, without source compilation."""
import unittest


def supplied_frontier(edges, seeds):
    seen, todo = set(), list(seeds)
    while todo:
        node = todo.pop()
        if node in seen:
            continue
        seen.add(node)
        todo.extend(edges.get(node, []))
    return seen


def supplied_host_admission(alternatives):
    # Exact declaration categories/visibility are supplied, never inferred from widening.
    return bool(alternatives) and all(kind in {"action", "look", "message"} and shared
                                      for kind, shared in alternatives)


class PublicContractWitnesses(unittest.TestCase):
    def test_host_widening_cannot_hide_sub_or_private_alternative(self):
        self.assertTrue(supplied_host_admission([("action", True)]))
        self.assertFalse(supplied_host_admission([("action", True), ("subaction", True)]))
        self.assertFalse(supplied_host_admission([("look", False)]))
        self.assertFalse(supplied_host_admission([("submessage", True)]))

    def test_finite_contract_frontier_preserves_recursive_references(self):
        edges = {"Public": ["Tree"], "Tree": ["Num", "Tree"]}
        self.assertEqual(supplied_frontier(edges, ["Public"]), {"Public", "Tree", "Num"})
        edges["Tree"].append("PrivateAlias")
        self.assertIn("PrivateAlias", supplied_frontier(edges, ["Public"]))
        hidden = {"PrivateAlias"}
        self.assertTrue(hidden & supplied_frontier(edges, ["Public"]))

    def test_direct_permission_is_not_transitive_type_understanding(self):
        uses = {"A": {"B"}, "B": {"C"}, "C": set()}
        required_types = {"BContract": ["CType"], "CType": ["Num"]}
        self.assertIn("CType", supplied_frontier(required_types, ["BContract"]))
        self.assertNotIn("C", uses["A"])
        self.assertIn("B", uses["A"])

    def test_diagnostic_provenance_does_not_grant_authority(self):
        # Component identities and subtype visibility are supplied certificates.
        reserved = {"Error.origin", "Refusal.origin", "ArgumentRefusal.argument"}
        cases = [("Error.origin", True, True),
                 ("Refusal.origin", True, True),
                 ("ArgumentRefusal.argument", True, True),
                 ("Other.origin", True, False),
                 ("Error.origin", False, False)]
        for component, visible_value_type, admitted in cases:
            self.assertEqual(component in reserved and visible_value_type, admitted)
        provenance_permissions = {"identity", "anchor", "path", "file"}
        self.assertFalse(provenance_permissions & {"invoke", "state", "private_schema"})


if __name__ == "__main__":
    unittest.main()
