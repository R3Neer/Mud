---
id: Q-028
title: Finiteness
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-044
  - D-047
  - D-081
  - D-088
affects: []
superseded-by: []
---

# Q-028 — Finiteness

## Content

Analysis limits, conservative approximations and messages when finiteness cannot be proven.

Status: **partially decided** by [[notes/decisions/ADR-044-reachability-eventually|D-044]], [[notes/decisions/ADR-047-quantifiers-and-finite-iteration|D-047]], [[notes/decisions/ADR-081-collection-filtering-take-and-indexing|D-081]] and [[notes/decisions/ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]].

Failure to prove finiteness or enumerability statically rejects a use that requires it; it does not produce a negative runtime answer. The same obligation applies to filters and `take`. D-088 retains this requirement for `for each`, selection and quantifiers/aggregators, and limits traversable cyclic domains to one fundamental period. The analysis and its diagnostics remain to be defined.
