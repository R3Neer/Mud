---
id: Q-068
title: Identity and structural equality of anonymous types
priority: P1
opened: 2026-08-28
resolved: true
closed: 2026-10-06
decisions:
  - D-096
  - D-115
affects:
  - anonymous types, reflection, look, message
superseded-by: []
---

# Q-068 — Identity and structural equality of anonymous types

## Resolution

Literal products use normalized structural identity. Look results and message payload types are static and nominal per declaration; := preserves that identity and no runtime types are generated. Occurrence identity remains separate from payload equality.

## Closure criterion

- C1: The complete choice described above is explicit and its affected developed surfaces agree.

## Closure evidence

- C1: D-115, its integration review and accompanying grammar/AST or semantic examples state the applicable contracts and delimit their conformance scope.
