---
id: Q-049
title: Destruction and `thing` collections
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-08-03
decisions:
  - D-021
  - D-077
affects: []
superseded-by: []
---

# Q-049 — Destruction and `thing` collections

## Resolution

[[notes/decisions/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]] retains complete properties when a structural dependency is destroyed. [[notes/decisions/ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]] resolves contained identities: removal is committed only if all final cardinalities and domains are valid; an immutable relationship retains latent membership, while a `mut` relationship removes it permanently. `create` restores only the former and validates the transition again.

There is no effectively cardinality-degraded collection: a violation produces `failed` and rollback.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-021`, `D-077`.
