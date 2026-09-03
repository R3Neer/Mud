---
id: Q-052
title: `message` delivery
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-08-28
decisions:
  - D-027
  - D-096
affects: []
superseded-by: []
---

# Q-052 — `message` delivery

Status: **resolved** by [[notes/decisions/ADR-096-modulos-callables-look-message-y-activacion|D-096]].

D-096 fixes multiplicity by causal occurrences, no payload-based deduplication, causal order by waves, causal evaluation of `when`/`if`, propagation to the next wave and cancellation of external delivery when the resolution rolls back. MUD and the host observe the same occurrence identity, with an internal causal projection and a final external projection.

The only material unresolved edge of the former question is separated into Q-067: which external projection applies when a participant ceases to exist before final state.

## Closure criterion

- C1: Fix multiplicity, deduplication and causal order of occurrences.
- C2: Fix when `when`, `if` and payload are evaluated.
- C3: Fix external behaviour on commit and rollback.

## Closure evidence

- C1: D-096 models causal occurrences with their own identity, retains multiplicity and propagates them across waves without payload deduplication.
- C2: D-096 evaluates `when` and `if` in the causal view and distinguishes internal causal from final external projection.
- C3: D-096 delivers to the host only after commit and cancels all external delivery if the resolution rolls back; the missing-participant edge is separated into Q-067.
