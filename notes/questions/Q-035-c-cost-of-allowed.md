---
id: Q-035
title: Cost of `imagine`
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-110
  - D-043
  - D-119
affects: []
superseded-by: []
---

# Q-035 — Cost of `imagine`

## Resolution

Imagine returns ActionReply through the full isolated invocation protocol, always discards its state, and cannot classify resource exhaustion as a modeled refusal.

## Pending

Define memoization validity, retry/cache isolation, speculative resource budgets and diagnostics. Result type and discard are settled.

## Closure criterion

- C1: The pending conditions are defined with objective verification evidence.
