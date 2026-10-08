---
id: Q-075
title: Alias operator resolution and identity
priority: P0
opened: 2026-10-08
resolved:
closed:
decisions:
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

D-146 fixes source signatures, owner participation, the overloadable set, result inference, explicit inverses and replacement-style derived updates. Proofs and metadata cannot select signatures. Result ambiguity requires annotation.

## Pending

- Define lookup across operand aliases and specializations, inheritance, diamond contributions, duplicate signatures and builtin/overload intersections.
- Define public identity/anchors, descriptor exposure and metadata ownership without inventing a type-dependent nominal anchor accidentally.
- Specify matching/lifting of overload signatures with union/collection operands and fixture-independent selection diagnostics.

## Closure criterion

- C1: A deterministic selection contract and contrasting ambiguous/inherited cases exist.
- C2: Nominal HIR and public identity/descriptor contracts cover operator declarations and applications.
- C3: Union/collection matching and builtin interactions have static evidence.

## Resolution

Partially resolved. Accepted contracts are integrated; the remaining policies are not selected.
