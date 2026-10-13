---
id: Q-050
title: Pruning in remaining Boolean operators
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-10-13
decisions:
  - D-152
  - D-150
  - D-142
  - D-022
affects: []
superseded-by: []
---

# Q-050 — Pruning in remaining Boolean operators

## Resolution

Canonical pruning, transparent derived Boolean reads, ordinary capture/recovery, prefix-preserving ordered demand, erased initial eventually goals and domain/collection value boundaries are fixed. Static query obligations remain mandatory; no causal search algorithm or mandatory sensitivity warnings are introduced.

## Closure criterion

- C1: Specify remaining boundary interactions and contrasting conformance cases.
- C2: Specify whether syntax-sensitive diagnostics are mandatory or explicitly decline them.

## Closure evidence

- C1: [[../decisions/ADR-152-ordered-demand-and-value-boundaries-for-pruning|D-152]], MUD-TYPE-024/032 in [[../../specification/21-expressions]] and ordered-demand, fault, equality, query and value-boundary certificates in specification/types/test_pruning_witnesses.py, with declarative cases in specification/types/typing-cases.yaml.
- C2: [[../decisions/ADR-150-transparent-derived-boolean-pruning-boundaries|D-150]] and MUD-TYPE-032 explicitly decline mandatory pruning-sensitivity warnings.
