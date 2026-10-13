---
id: Q-079
title: Quantifier predicate demand
priority: P1
opened: 2026-10-14
resolved: true
closed: 2026-10-14
decisions:
  - D-164
affects:
  - specification/21-expressions.md
  - specification/22-quantifiers-and-iteration.md
superseded-by: []
---

# Q-079 — Quantifier predicate demand

## Resolution

The author accepts ordered exists/forall short circuit, complete common-view
unordered evaluation and min/max search from their respective semantic ends.
Count needs all predicate outcomes. Source production/validation and all static
checks remain required; demanded faults remain faults, skipped predicate work
does not occur. Min/max retain the previously fixed ordered-witness Bool-filter
contract rather than a general numeric aggregation body.

## Closure criterion

- C1: Define exists/forall demand with ordered and unordered sources, preserving errors/dependencies.
- C2: Define count and extremum search, empty results and source-production boundaries.

## Closure evidence

- C1: D-164 and MUD-ITER-004 in chapter 22, ordered/unordered declarative cases and test_quantifier_demand_witnesses.py supplied demand certificates.
- C2: Chapter 22's result/direction rules, empty and reverse-search certificates, unchanged source/step checking obligations.
