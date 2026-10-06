---
id: Q-066
title: Nominal binding of erased callable descriptors
priority: P1
opened: 2026-08-28
resolved: true
closed: 2026-10-06
decisions:
  - D-096
  - D-114
affects:
  - callables, resolution, binding
superseded-by: []
---

# Q-066 — Nominal binding of erased callable descriptors

## Resolution

Named roles are available only through an unequivocal static contract shared by every possible alternative. Erased positional invocation and static narrowing are distinguished; runtime scanning is excluded.

## Closure criterion

- C1: The complete choice described above is explicit and its affected developed surfaces agree.

## Closure evidence

- C1: D-114, its integration review and accompanying grammar/AST or semantic examples state the applicable contracts and delimit their conformance scope.
