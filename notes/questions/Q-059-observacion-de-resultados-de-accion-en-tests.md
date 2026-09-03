---
id: Q-059
title: Observing action results in tests
priority: P1
opened: 2026-07-29
resolved: false
closed:
decisions:
  - D-055
  - D-061
affects: []
superseded-by: []
---

# Q-059 — Observing action results in tests

## Content

Status: **open** from [[notes/decisions/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]] and [[notes/decisions/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].

How does a test check that a requested action produced `accepted`, `rejected` or `failed` without confusing those results with the test's own `passed`, `failed` and `error` states?

The following must be decided:

- Whether an action request inside `then` may bind its result to a local name.
- Whether a `rejected` action is by default a scenario error or an observable result.
- How the external `reason` already defined for `rejected` and `failed`, together with its trace, is linked without turning diagnostics into ordinary world values.
