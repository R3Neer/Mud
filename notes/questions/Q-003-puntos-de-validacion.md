---
id: Q-003
title: Validation points
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-026
  - D-037
affects: []
superseded-by: []
---

# Q-003 — Validation points

## Content

At exactly what point are domains, cardinalities and `always` validated: after each write, when the root closes, when each wave closes, or at several of these points?

The answer affects which tentative states are observable to later rules.

Status: **partially decided** by [[notes/decisions/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]] and [[notes/decisions/ADR-037-campos-y-dominios-declarativos|D-037]].

Final cardinality is proven statically for each `then` and for every possible concurrent consolidation. Intermediate states inside a `then`'s private delta may violate it. Domains are preserved during initialisation, materialisation, specialisation, writes, roots, waves and publishable states. A unified operational formulation, the exact treatment of suspended references and the checking points for `always` rules remain open.
