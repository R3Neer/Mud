---
id: Q-047
title: Selection of defaults by type
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-10-06
decisions:
  - D-017
  - D-026
  - D-031
  - D-068
  - D-069
  - D-074
  - D-112
affects: []
superseded-by: []
---

# Q-047 — Selection of defaults by type

## Resolution

Explicit storage initialisation removes type-default selection. Inherited initialisation, complete alias construction, family completeness and intrinsic metadata defaults have distinct contracts in D-112.

## Closure criterion

- C1: The complete choice described above is explicit and its affected developed surfaces agree.

## Closure evidence

- C1: D-112, its integration review and accompanying grammar/AST or semantic examples state the applicable contracts and delimit their conformance scope.
