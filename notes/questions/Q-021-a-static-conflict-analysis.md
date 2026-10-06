---
id: Q-021
title: Static conflict analysis
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-10-06
decisions:
  - D-023
  - D-026
  - D-031
  - D-046
  - D-054
  - D-123
affects: []
superseded-by: []
---

# Q-021 — Static conflict analysis

## Resolution

MUD-EFFECT-005 and MUD-EFFECT-006 in [[specification/14-fields-and-mutability]] distinguish proved static conflicts, residual runtime overlap and conservatively rejected unknown stored cardinality. Finite proof-boundary witnesses are checked by validate_type_spec.py and its regression tests.

The required analysis is sound and conservative, not a complete solver for arbitrary symbolic predicates. Operational engine and general termination design retain their own questions.

## Closure criterion

- C1: The remaining formal proof/minimum-analysis boundary is specified with objective obligations and contrasting conformance evidence.

## Closure evidence

- C1: MUD-EFFECT-005 and MUD-EFFECT-006 in [[specification/14-fields-and-mutability]] distinguish proved static conflicts, residual runtime overlap and conservatively rejected unknown stored cardinality. Finite proof-boundary witnesses are checked by validate_type_spec.py and its regression tests. [[notes/decisions/ADR-123-static-capabilities-and-conflict-proof-boundaries|D-123]] records the integration.
