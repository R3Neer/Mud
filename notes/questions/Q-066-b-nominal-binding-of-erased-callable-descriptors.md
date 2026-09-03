---
id: Q-066
title: Nominal binding of erased callable descriptors
priority: P1
opened: 2026-08-28
resolved: false
closed:
decisions:
  - D-096
affects:
  - callables, resolution, binding
superseded-by: []
---

# Q-066 — Nominal binding of erased callable descriptors

## Content

Define how `for` and `given` role names are recovered or required when invoking a callable descriptor whose static type has erased part of the concrete declaration's nominal identity.
