---
id: Q-048
title: Destruction with active descendants
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-07-27
decisions:
  - D-021
affects: []
superseded-by: []
---

# Q-048 — Destruction with active descendants

## Content

Status: **closed**.

Decision: [[notes/decisions/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]].

Declared edges are retained in storage. The effective projection crosses inactive ancestors and connects each active descendant to its nearest active ancestors. The descendant retains its own properties, temporarily loses what it inherited from the destroyed node and recovers the original structure when that node is recreated.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-021`.
