---
id: Q-021
title: Static conflict analysis
priority: P1
opened: 2026-07-29
resolved: false
closed:
decisions:
  - D-023
  - D-026
  - D-031
  - D-046
  - D-054
affects: []
superseded-by: []
---

# Q-021 — Static conflict analysis

## Content

Which conflicts can be proven at compile time, and which only in a concrete resolution?

D-023 and [[notes/decisions/ADR-046-algebra-and-conflicts-of-effects|D-046]] establish the initial criterion: a conflict the compiler can prove is rejected statically; a coincidence it cannot decide is checked at runtime, and the transaction is rolled back if it occurs. D-054 removes matching activations of one `thing` or rule from this category: they are idempotent because their definitions are unique. D-031 makes the alias case inapplicable.

D-026 strengthens the cardinality case: the compiler must prove local and consolidated preservation; if it cannot, it conservatively rejects the programme instead of deferring the case to runtime.
