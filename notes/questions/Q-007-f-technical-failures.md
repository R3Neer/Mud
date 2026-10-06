---
id: Q-007
title: Technical failures
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-042
  - D-043
  - D-048
  - D-061
  - D-118
affects: []
superseded-by: []
---

# Q-007 — Technical failures

## Resolution

ActionReply, mandatory origins/reasons, Refusal subtypes, final-expression BoolCheck, Error inheritance/cause and multiplicity-preserving Error channels are specified. Always falsity is refusal; otherwise selects errors only.

## Pending

Finish the exhaustive expression/adapter error catalogue and the external codes/trace contract; distinguish implementation resource exhaustion, cancellation and runtime defects from modeled recoverable Error. These are not closed by choosing the value representation.

## Closure criterion

- C1: The pending conditions are defined with objective verification evidence.
