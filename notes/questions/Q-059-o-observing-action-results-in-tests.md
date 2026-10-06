---
id: Q-059
title: Observing action results in tests
priority: P1
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-055
  - D-061
  - D-119
affects: []
superseded-by: []
---

# Q-059 — Observing action results in tests

## Resolution

A real invocation binds ordinary ActionReply in an effect-block initializer. Explicit observation differs from a bare effect call propagating non-success; test executor labels remain separate.

## Pending

Formalize test assertion/aggregation and observation lifetimes after failed child-scope rollback, including Refusal versus computing Error in shared traces. No new external envelope or test-specific reply type is needed.

## Closure criterion

- C1: The pending conditions are defined with objective verification evidence.
