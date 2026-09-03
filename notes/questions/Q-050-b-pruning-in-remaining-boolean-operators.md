---
id: Q-050
title: Pruning in remaining Boolean operators
priority: P1
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-022
affects: []
superseded-by: []
---

# Q-050 — Pruning in remaining Boolean operators

## Content

Premise status: **decided** by [[notes/decisions/ADR-022-structural-deletion-of-inactive-boolean-rules|D-022]].

Calls to inactive Boolean rules are pruned after canonical desugaring to `not`, `and` and `or`. Elaboration of `!=`, `xor`, Boolean quantifiers and interactions with `allowed`, `eventually` and internal failures remains to be fixed.
