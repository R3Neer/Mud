---
id: Q-029
title: Termination
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-155
affects: []
superseded-by: []
---

# Q-029 — Termination

## Already decided

[[../decisions/ADR-155-uniform-normative-analysis-and-finiteness-diagnostics|D-155]] requires one normative certification procedure per language version, optionally supplied by a shared reference analyzer. Existing finite traversal and decreasing-measure obligations remain applicable. Tool resource interruption is not a negative proof or an invalid-program judgement.

## Pending

- Specify the classes of calculations/actions/rules the normative procedure certifies and its exact normalization, proof search and completion conditions.
- Coordinate body termination and deeper reachable-state analysis without making those methods a blanket prerequisite to independently fixed static construct contracts.
- Lexicographic descent has been discussed but not accepted; no corresponding mandatory rule is established.

## Closure criterion

- C1: Certified classes and the uniform procedure are specified with contrasting evidence and scope boundaries.
