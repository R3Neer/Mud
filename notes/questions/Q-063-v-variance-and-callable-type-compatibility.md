---
id: Q-063
title: Variance and callable type compatibility
priority: P1
opened: 2026-08-28
resolved: true
closed: 2026-10-06
decisions:
  - D-096
  - D-114
affects:
  - callable typing, subtyping, narrowing
superseded-by: []
---

# Q-063 — Variance and callable type compatibility

## Resolution

D-114 defines read-only input contravariance, output covariance, writable-place invariance, unions and preservation of domains/cardinalities/defaults and capabilities. Outer-root permission remains independent.

## Closure criterion

- C1: The complete choice described above is explicit and its affected developed surfaces agree.

## Closure evidence

- C1: D-114, its integration review and accompanying grammar/AST or semantic examples state the applicable contracts and delimit their conformance scope.
