---
id: Q-063
title: Variance and callable type compatibility
priority: P1
opened: 2026-08-28
resolved: false
closed:
decisions:
  - D-096
affects:
  - callable typing, subtyping, narrowing
superseded-by: []
---

# Q-063 — Variance and callable type compatibility

## Content

Formalise compatibility and variance of callable types in inputs, outputs, mutable locations and unions, while keeping an `action`'s outer capability separate from `subaction`.
