---
id: Q-075
title: Alias operator resolution and identity
priority: P0
opened: 2026-10-08
resolved:
closed:
decisions:
  - D-149
  - D-146
affects:
  - specification/10-names-and-anchors.md
  - specification/11-type-system.md
  - specification/21-expressions.md
superseded-by: []
---

# Q-075 — Alias operator resolution and identity

## Question

How are visible alias operator candidates discovered, inherited, disambiguated and identified publicly?

## Already decided

D-146 fixes source signatures, owner participation, the overloadable set, result inference, explicit inverses and replacement-style derived updates. Proofs and metadata cannot select signatures. Result ambiguity requires annotation. D-149 fixes bilateral lookup, unique static specificity, original inheritance/diamond deduplication, union narrowing, restricted arithmetic lifting, explicit-before-builtin priority, duplicate declaration rejection, subordinate signature identity and descriptor catalogues.

## Pending

- Specify collision-free canonical anchor encoding for every complete operand contract, including generic binders, applications, domains, cardinalities and escaping, under source-origin identity rules.
- Complete the reflective property/type schema and source representation of operator metadata, preserving the selected whole-declaration ownership and nominal/typed phase separation.

## Closure criterion

- C1: A deterministic selection contract and contrasting ambiguous/inherited cases exist.
- C2: Nominal HIR and public identity/descriptor contracts cover operator declarations and applications.
- C3: Union/collection matching and builtin interactions have static evidence.

## Resolution

Partially resolved by [[../decisions/ADR-149-alias-operator-selection-inheritance-and-reflection]]. Chapter 21 and supplied finite candidate witnesses cover selected policies; full anchor encoding and reflective schema evidence remain required before closure.
