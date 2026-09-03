---
id: Q-013
title: Relational constraints between `on` participants
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-07-30
decisions:
  - D-036
  - D-063
affects: []
superseded-by: []
---

# Q-013 — Relational constraints between `on` participants

## Content

Status: **closed** again by [[notes/decisions/ADR-063-signatures-given-and-joint-on-bindings|D-063]], which amends [[notes/decisions/ADR-036-participants-recipients-and-calls|D-036]].

The header may construct related participants through `role [: Type] in expression`. The annotation nominally refines the collection element. All names are visible throughout the complete header and their types and constraints are resolved jointly, so forward references and cycles are admitted. Each role's universe is the concrete active `thing` values of its effective type; bindings form the finite join satisfying every constraint in one snapshot. Roles retain orientation, and neither inequality nor symmetric deduplication is imposed. Additional conditions are expressed in `if`; `given` is not permitted in `on` declarations.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-036`, `D-063`.
