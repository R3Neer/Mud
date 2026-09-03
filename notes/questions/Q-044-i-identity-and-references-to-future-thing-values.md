---
id: Q-044
title: Identity and references to future `thing` values
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-07-28
decisions:
  - D-054
affects: []
superseded-by: []
---

# Q-044 — Identity and references to future `thing` values

## Content

Status: **closed**.

What does the name activated by `create A` designate?

Current decision: [[notes/decisions/ADR-054-canonical-definitions-and-initial-activation|D-054]].

`A` has one canonical top-level definition and is resolvable before it is active. `create A` only requests its activation. After `destroy A`, a later execution reactivates the same identity; it never fabricates a second `A` or changes its ancestors.

Operations requiring active presence must check it. The birth and memory of `on` bindings remain coordinated with Q-005.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-054`.
