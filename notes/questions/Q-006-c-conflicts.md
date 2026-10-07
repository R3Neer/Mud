---
id: Q-006
title: Conflicts
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-10-06
decisions:
  - D-023
  - D-039
  - D-046
  - D-060
  - D-080
  - D-098
  - D-100
  - D-105
  - D-117
  - D-123
affects: []
superseded-by: []
---

# Q-006 — Conflicts

## Resolution

MUD-EFFECT-005 and MUD-EFFECT-006 in [[specification/15-fields-and-mutability]] define the minimum constant-path analysis and the residual symbolic/uniqueness boundary, including mandatory static stored-cardinality preservation. The residual-symbolic-key-overlap and static-cardinality cases supply contrasting instances.

The required analysis is sound and conservative, not a complete solver for arbitrary symbolic predicates. Operational engine and general termination design retain their own questions.

## Closure criterion

- C1: The remaining formal proof/minimum-analysis boundary is specified with objective obligations and contrasting conformance evidence.

## Closure evidence

- C1: MUD-EFFECT-005 and MUD-EFFECT-006 in [[specification/15-fields-and-mutability]] define the minimum constant-path analysis and the residual symbolic/uniqueness boundary, including mandatory static stored-cardinality preservation. The residual-symbolic-key-overlap and static-cardinality cases supply contrasting instances. [[notes/decisions/ADR-123-static-capabilities-and-conflict-proof-boundaries|D-123]] records the integration.
