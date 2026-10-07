---
id: Q-046
title: Ineffective creation inside a root
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-10-07
decisions:
  - D-023
  - D-031
  - D-054
  - D-096
  - D-125
affects: []
superseded-by: []
---

# Q-046 — Ineffective creation inside a root

## Resolution

Resolved by [[notes/decisions/ADR-125-instruction-local-lifecycle-no-ops|D-125]] and integrated into the developed normative surfaces below. Complete operational trace formalisation remains separate work; the choices identified by this question are fixed.

## Closure criterion

- C1: Instruction-local behaviour is specified for both redundant creation and redundant destruction, without suppressing surrounding work.
- C2: Mixed-availability sequences and internal calls use the current private view, retaining effective-transition validation and concurrent consolidation.

## Closure evidence

- C1: MUD-LIFE-001 in [[specification/04-mathematical-model]] and the lifecycle effect contract in [[specification/08-concrete-grammar]] specify successful no-ops; D-125 contrasting cases cover redundant create/destroy and continued Bob creation.
- C2: D-125 contrasting cases cover repeated create, repeated destroy and destroy/create; MUD-LIFE-001 applies preceding effects/internal calls and preserves validation and concurrent composition.
