"""Bounded certificates for normalized type graphs and static given selection.

Inputs are supplied, already normalized contracts. This module neither parses
MUD nor computes generic instantiation, variance or arbitrary domain proofs.
"""
from __future__ import annotations

import json


def structural_equal(nodes, left, right):
    """Erase alias wrappers, then check all labels/edges by a greatest fixed point."""
    if not isinstance(nodes, dict) or not nodes or left not in nodes or right not in nodes:
        raise ValueError("Undefined normalized type graph root")
    allowed = {"alias", "record", "field", "product", "collection", "union",
               "exact-dictionary", "functional-dictionary", "callable", "interval",
               "primitive", "thing", "family", "produced"}
    for name, node in nodes.items():
        children = node.get("children", [])
        if node.get("kind") not in allowed or not isinstance(children, list) or any(x not in nodes for x in children):
            raise ValueError(f"{name}: malformed normalized constructor")
        if node["kind"] == "alias" and len(children) != 1:
            raise ValueError("Alias erasure needs exactly one representation target")
        if node["kind"] in {"primitive", "thing", "family", "produced"}:
            if not isinstance(node.get("identity"), str) or children:
                raise ValueError("Opaque types require exact identity and no structural children")
        if not isinstance(node.get("contract", {}), dict):
            raise ValueError("Normalized local contract must be a map")

    def erase(name):
        seen = set()
        while nodes[name]["kind"] == "alias":
            if name in seen:
                raise ValueError("Alias-only cycle has no structural constructor")
            seen.add(name)
            name = nodes[name]["children"][0]
        return name

    canonical = {name: erase(name) for name in nodes}
    graph = {}
    for name in set(canonical.values()):
        node = nodes[name]
        # These are normalized contract labels, not evaluated default/body values.
        label = {key: node.get(key) for key in ("kind", "identity", "arguments", "contract")}
        graph[name] = (json.dumps(label, sort_keys=True, allow_nan=False),
                       tuple(canonical[x] for x in node.get("children", [])))
    pairs = {(a, b) for a, (la, ca) in graph.items() for b, (lb, cb) in graph.items()
             if la == lb and len(ca) == len(cb)}
    def children_match(a, b):
        left_children, right_children = graph[a][1], graph[b][1]
        if nodes[a]["kind"] != "union":
            return all(pair in pairs for pair in zip(left_children, right_children))
        # Union source order is not observable. Match the complete normalized
        # alternatives bijectively, without dropping nominally distinct ones.
        assigned = {}
        def match(index, visited):
            for target, right_child in enumerate(right_children):
                if target in visited or (left_children[index], right_child) not in pairs:
                    continue
                visited.add(target)
                if target not in assigned or match(assigned[target], visited):
                    assigned[target] = index
                    return True
            return False
        return all(match(index, set()) for index in range(len(left_children)))

    while True:
        remaining = {(a, b) for a, b in pairs
                     if children_match(a, b)}
        if remaining == pairs:
            return (canonical[left], canonical[right]) in pairs
        pairs = remaining


def selected_candidates(witness, includes, parents):
    """Check one lookup-level fixture with pretyped argument possibilities.

    Each possibility represents an independently admitted contextual type. The
    witness has no body/default evaluation, expected-result tie-break or later
    lookup level. Generic inference is deliberately not implemented here.
    unknown_admission is a supplied proof-boundary premise: incomplete
    domain/cardinality admission of nominally compatible values cannot exclude
    the candidate. Other fixtures supply closed static compatibility facts.
    """
    candidates = witness["candidates"]
    if not isinstance(candidates, list):
        raise ValueError("Candidates must belong to one supplied lookup level")
    actuals = witness.get("arguments", [])
    named = bool(actuals) and "name" in actuals[0]
    if any(("name" in item) != named for item in actuals):
        raise ValueError("Mixed positional/named witness arguments")
    if named and len({x["name"] for x in actuals}) != len(actuals):
        raise ValueError("Repeated supplied argument name")
    identities, selected = set(), []
    def compatible(actual, target):
        if includes(actual, target, parents):
            return True
        unknown = actual.get("unknown_admission", False)
        if type(unknown) is not bool:
            raise ValueError("Unknown admission premise must be Boolean")
        return unknown and includes({"name": actual["name"]}, {"name": target["name"]}, parents)

    for candidate in candidates:
        identity = candidate["identity"]
        if identity in identities:
            raise ValueError("Candidates must already be deduplicated by identity")
        identities.add(identity)
        receivers = candidate.get("receivers", [])
        supplied = witness.get("receivers", [])
        if len(receivers) != len(supplied) or any(not includes(a, b, parents) for a, b in zip(supplied, receivers)):
            continue
        slots = candidate.get("givens", [])
        names = [slot["name"] for slot in slots]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate formal given name")
        if named:
            if any(x["name"] not in names for x in actuals):
                continue
            binding = {names.index(x["name"]): x for x in actuals}
        else:
            if len(actuals) > len(slots):
                continue
            binding = dict(enumerate(actuals))
        if any(i not in binding and not slot.get("default", False) for i, slot in enumerate(slots)):
            continue
        if all(any(compatible(t, slots[i]["type"]) for t in actual["types"])
               for i, actual in binding.items()):
            selected.append(identity)
    return sorted(selected)
