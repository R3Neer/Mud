---
id: Q-050
title: Pruning in remaining Boolean operators
priority: P1
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-150
  - D-142
  - D-022
affects: []
superseded-by: []
---

# Q-050 — Pruning in remaining Boolean operators

## Question

Which boundaries propagate structural deletion across speculative queries, reachability and internal failure/recovery?

## Already decided

Canonical equality/inequality/xor, demand sharing and per-member no-filter closure are specified by D-142 and MUD-TYPE-024. Deleted call arguments are not evaluated. Empty-source quantifier/selection/count/min/max results retain their ordinary contracts. D-150 fixes transparent := Boolean bindings across locals/fields/components/metadata, = capture, preservation of actually read prefix work and faults, erased initial eventually goals, ordinary imagine capture and no mandatory sensitivity warnings.

## Pending

- Complete the compositional demand/short-circuit contract when an erased derived read or initial eventually goal carries independent potentially faulting prefix computations, including enclosing operators that eliminate residual erased fragments and derived domain/cardinality transforms. The accepted actual-read examples must hold, but do not determine every enclosing execution order.

## Closure criteria

- C1: Specify the remaining boundary interactions and contrasting conformance cases.
- C2: Specify whether syntax-sensitive diagnostics are mandatory or explicitly decline them.

## Resolution

Partially resolved by [[../decisions/ADR-142-canonical-pruning-and-empty-filter-closures]] and [[../decisions/ADR-150-transparent-derived-boolean-pruning-boundaries]]. C2 is satisfied: sensitivity warnings are not required. C1 retains the explicitly delimited compositional demand cases.
