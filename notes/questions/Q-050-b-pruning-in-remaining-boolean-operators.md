---
id: Q-050
title: Pruning in remaining Boolean operators
priority: P1
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-142
  - D-022
affects: []
superseded-by: []
---

# Q-050 — Pruning in remaining Boolean operators

## Question

Which boundaries propagate structural deletion across speculative queries, reachability and internal failure/recovery?

## Already decided

Canonical equality/inequality/xor, demand sharing and per-member no-filter closure are specified by D-142 and MUD-TYPE-024. Deleted call arguments are not evaluated. Empty-source quantifier/selection/count/min/max results retain their ordinary contracts.

## Pending

- Pruning boundaries for imagine/eventually, internal faults/recovery and intermediate bindings must be delimited without treating erased as a stored Bool.
- Any required diagnostics for syntax-sensitive pruning remain to be specified.

## Closure criteria

- C1: Specify the remaining boundary interactions and contrasting conformance cases.
- C2: Specify whether syntax-sensitive diagnostics are mandatory or explicitly decline them.

## Resolution

Partially resolved by [[../decisions/ADR-142-canonical-pruning-and-empty-filter-closures]]. No accepted core case remains pending.
