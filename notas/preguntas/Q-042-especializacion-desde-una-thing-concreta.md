---
id: Q-042
title: Specialisation from a concrete `thing`
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-07-27
decisions:
  - D-015
affects: []
superseded-by: []
---

# Q-042 — Specialisation from a concrete `thing`

## Content

Status: **closed**.

When a concrete `thing` $B$ specialises from another concrete `thing` $A$, does it inherit only $A$'s declarations, constraints and defaults, or does it also copy or observe its current mutable state?

Decision: [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]].

Schema and effective defaults are inherited, never active state. Each concrete `thing` has independent state, and its first activation initialises it from defaults before applying its explicit assignments.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-015`.
