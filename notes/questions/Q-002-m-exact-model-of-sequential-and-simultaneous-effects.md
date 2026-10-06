---
id: Q-002
title: Exact model of sequential and simultaneous effects
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-111
  - D-110
  - D-023
  - D-042
  - D-046
  - D-060
  - D-096
  - D-117
affects: []
superseded-by: []
---

# Q-002 — Exact model of sequential and simultaneous effects

## Resolution

Sequential private projections, branch normalization, replacement before change, semantic alias/dictionary destinations, deletion precedence, joint uniqueness and materialisation-generation writes are fixed by D-117. Runtime schema edits remain excluded.

## Pending

Write the complete operational judgments for every surviving effect family in the planned effects/root/wave chapters, including activation admission under Q-046. Static conflict analysis is specified in [[specification/10-type-system]] and [[specification/14-fields-and-mutability]]; its accepted contract is not a pending decision. These pending formalizations do not reopen the accepted composition policies.

## Closure criterion

- C1: The pending conditions are defined with objective verification evidence.
