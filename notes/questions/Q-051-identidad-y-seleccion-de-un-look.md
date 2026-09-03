---
id: Q-051
title: Identity and selection of a `look`
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-08-28
decisions:
  - D-027
  - D-061
  - D-096
affects: []
superseded-by: []
---

# Q-051 — Identity and selection of a `look`

Status: **resolved** by [[notes/decisions/ADR-096-modulos-callables-look-message-y-activacion|D-096]].

A `look` is a pure callable with `for` participants and `given` parameters. A call returns exactly one anonymous result object, not a special sequence of rows. Its read view comes from the call context: stable state from the host, a rule snapshot or the private delta visible from a `then`.

Remaining open issues are no longer about basic `look` identity or selection: dynamic-result joins remain in Q-065, and anonymous-type identity in Q-068.

## Closure criterion

- C1: Define how a `look`'s participants and parameters are supplied.
- C2: Define the conceptual cardinality of a call's result.
- C3: Define the read view used by the query.

## Closure evidence

- C1: D-096 defines `look` as a pure callable with `for` and `given`.
- C2: D-096 defines a call as exactly one anonymous result object; multiplicity is expressed in its fields.
- C3: D-096 defines the caller's inherited view: stable from the host, a rule snapshot or the private delta visible from `then`.
