---
id: Q-046
title: Ineffective creation inside a root
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-023
  - D-031
  - D-054
  - D-096
affects: []
superseded-by: []
---

# Q-046 — Ineffective creation inside a root

## Content

Status: **partially decided** by [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]] and [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

If a rule contains `create A` while canonical identity `A` is already active, the complete rule does not execute and publishes none of its effects.

The following remain to be decided:

- Which result an action requested in the same case receives: `rejected`, `failed` or another result.
- Whether a rule with several creations requires all identities to be absent.
- How creations with mixed availability combine within a `then` sequence, including those contributed transitively by internal calls.

D-054 requires one complete top-level definition for every `thing` and rule. Several concurrent activations of one absent identity consolidate idempotently; there are no bodies or fragments left to merge. D-031 removes aliases from the `create` and `destroy` system. Activation and destruction requested by different `then` blocks leave the identity destroyed when the wave closes.

This blocks the complete operational semantics of `create`, effect sets and atomicity.
