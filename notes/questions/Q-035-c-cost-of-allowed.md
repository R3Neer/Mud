---
id: Q-035
title: Cost of `allowed`
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-110
  - D-043
affects: []
superseded-by: []
---

# Q-035 — Cost of `allowed`

## Content

Memoisation, speculative depth, cycles and resource limits without changing semantic truth.

Status: **partially decided** by [[notes/decisions/ADR-043-speculative-query-with-allowed|D-043]].

The admissibility graph is acyclic, and a resource limit may not be silently turned into false. Memoisation, budgets and diagnostics remain to be defined.

## Additional product questions

## Tentative journal boundary

D-110 fixes use of the complete speculative protocol with unconditional discard, including acceptance. `failed` still propagates, and world/queue/log/randomness isolation is mandatory. Memoisation, resource budgets and diagnostics remain pending; this question is not closed by choosing a journal implementation.
