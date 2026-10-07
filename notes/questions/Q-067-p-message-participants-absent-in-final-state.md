---
id: Q-067
title: `message` participants absent in final state
priority: P1
opened: 2026-08-28
resolved: true
closed: 2026-10-07
decisions:
  - D-133
  - D-096
affects:
  - message, lifecycle, host boundary
superseded-by: []
---

# Q-067 — Message payload and participant lifetime

## Resolution

Message payloads are frozen in their causal birth view, with canonical participant descriptors even after inactivity/recreation. Shared normal messages publish after validated consolidation with a scope-aware Ticket; final confirmation/disposal determines Kept/Dropped without filtering by payload equality. Sub/private messages, tests and imagine publish none.

## Closure criterion

- C1: Define payload and binding lifetime when final state changes or a participant disappears.
- C2: Define provisional delivery, scope rollback, terminal ticket observation and confirmed-world isolation.

## Closure evidence

- C1: D-133 and specification/08-concrete-grammar define frozen causal values, canonical bindings and distinct equal-valued occurrences; message conformance traces cover changes and disappearance.
- C2: D-133, specification/04-mathematical-model and specification/28-effects define Waiting/Kept/Dropped, validated barriers and protected/invocation/outer scopes; specification/effects/message-delivery-cases.json contrasts recovery, child completion, imagination and subscription.
