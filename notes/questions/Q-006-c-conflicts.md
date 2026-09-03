---
id: Q-006
title: Conflicts
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-023
  - D-039
  - D-046
  - D-060
  - D-080
  - D-098
  - D-100
affects: []
superseded-by: []
---

# Q-006 — Conflicts

## Question

What is the complete compatibility matrix for assignments, increments, multiplications and concurrent structural operations?

## Already decided

The question is **partially decided** by [[notes/decisions/ADR-023-consolidation-of-concurrent-structural-effects|D-023]], [[notes/decisions/ADR-039-collections-and-dictionaries|D-039]], [[notes/decisions/ADR-046-algebra-and-conflicts-of-effects|D-046]], [[notes/decisions/ADR-060-additive-deltas-and-nat-normalisation|D-060]], [[notes/decisions/ADR-080-higher-order-collection-algebra-and-updates|D-080]], [[notes/decisions/ADR-098-assignable-paths-and-write-back-of-immutable-aliases|D-098]] and [[notes/decisions/ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].

Equal and unequal assignments; concurrent arithmetic `(Δ, P, Q)` with an additive block before the multiplicative one; the structural core `create → add → remove → destroy`; composition of `add` and `remove` on one presence; homogeneous updates `|=`, `&=`, `^=` and `--=`; idempotent consolidation of multiple additions of one value to a `unique` collection; reproducible provenance tie-breaking for concurrent insertions; and sequential reconstruction/write-back semantics for stored aliases are fixed. In `Nat`, additive deltas are summed as signed integers and only then normalised to zero.

## Outstanding

The families for which no algebraic combination or canonical composition yet exists remain to be completed, including remaining dictionary cases, properties, structural cardinality limits, and partially overlapping destinations or write-backs. The minimum required precision of static analysis distinguishing inevitable, possible and impossible conflict also remains to be fixed.

## Closure criterion

- C1. A complete classification exists for remaining concurrent dictionary combinations that can coincide on one semantic destination.
- C2. A complete classification exists for operations on properties and structural cardinality limits lacking an algebraic combination or canonical composition.
- C3. A complete rule exists for partially overlapping destinations and write-backs, including the condition distinguishing valid composition from conflict.
- C4. The minimum required precision of static analysis distinguishing inevitable, possible and impossible conflict is fixed.

## Resolution

Pending satisfaction of C1–C4.
