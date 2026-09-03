---
id: Q-067
title: `message` participants absent in final state
priority: P1
opened: 2026-08-28
resolved: false
closed:
decisions:
  - D-096
affects:
  - message, lifecycle, host boundary
superseded-by: []
---

# Q-067 — `message` participants absent in final state

## Content

Decide the external projection of a committed occurrence when one of its `on` bindings ceases to exist or be active before the final stable state, while preserving internal causal identity.
