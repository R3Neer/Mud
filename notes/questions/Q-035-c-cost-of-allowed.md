---
id: Q-035
title: Cost of `allowed`
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-043
affects: []
superseded-by: []
---

# Q-035 — Cost of `allowed`

## Content

Memoisation, speculative depth, cycles and resource limits without changing semantic truth.

Status: **partially decided** by [[notes/decisions/ADR-043-query-especulativa-allowed|D-043]].

The admissibility graph is acyclic, and a resource limit may not be silently turned into false. Memoisation, budgets and diagnostics remain to be defined.

## Additional product questions
