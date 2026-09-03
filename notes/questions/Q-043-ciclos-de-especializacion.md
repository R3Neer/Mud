---
id: Q-043
title: Specialisation cycles
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-07-27
decisions:
  - D-015
affects: []
superseded-by: []
---

# Q-043 — Specialisation cycles

## Content

Status: **closed**.

Should every non-trivial cycle of direct specialisation be rejected?

Decision: [[notes/decisions/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]].

Every direct-specialisation cycle is invalid. The semantic relation `is` is a partial order.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-015`.
