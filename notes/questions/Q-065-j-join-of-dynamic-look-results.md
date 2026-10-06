---
id: Q-065
title: Join of dynamic `look` results
priority: P1
opened: 2026-08-28
resolved: true
closed: 2026-10-06
decisions:
  - D-096
  - D-115
affects:
  - look, callables, typing
superseded-by: []
---

# Q-065 — Join of dynamic `look` results

## Resolution

With several incomparable minimal common result supertypes, retain the normalized union of original alternatives. Unique informative common joins retain their existing rule; textual priority and intersections are excluded.

## Closure criterion

- C1: The complete choice described above is explicit and its affected developed surfaces agree.

## Closure evidence

- C1: D-115, its integration review and accompanying grammar/AST or semantic examples state the applicable contracts and delimit their conformance scope.
