---
id: Q-003
title: Validation points
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-10-06
decisions:
  - D-026
  - D-037
  - D-118
affects: []
superseded-by: []
---

# Q-003 — Validation points

## Resolution

Domains are checked at initialization/write and consolidated boundaries. Cardinality must be proven for complete private then results and possible consolidations, while intermediate private states may violate it. Always is checked after each consolidated root and each consolidated wave, before a later wave can repair a violation; false yields AlwaysRefusal. Suspended hard dependencies waive the inactive rule and must be revalidated on restored effective activation.

## Closure criterion

- C1: The complete choice described above is explicit and its affected developed surfaces agree.

## Closure evidence

- C1: D-118, its integration review and accompanying grammar/AST or semantic examples state the applicable contracts and delimit their conformance scope.
