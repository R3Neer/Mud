---
id: Q-004
title: Rollback of rejected
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-07-28
decisions:
  - D-042
affects: []
superseded-by: []
---

# Q-004 — Rollback of `rejected`

## Content

Status: **closed** by [[notes/decisions/ADR-042-acciones-raiz-y-resultados|D-042]].

Every result other than `accepted`, including a false `after`, restores exactly the preceding stable state and publishes neither messages nor external effects.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-042`.
