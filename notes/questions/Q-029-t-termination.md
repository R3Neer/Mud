---
id: Q-029
title: Termination
priority: P2
opened: 2026-07-29
resolved: true
closed: 2026-10-14
decisions:
  - D-167
  - D-168
  - D-155
affects:
  - specification/11-type-system.md
  - specification/types
superseded-by: []
---

# Q-029 — Termination

## Resolution

D-167/D-168 define the admitted body classes, finite natural/lexicographic/phase
search, actual Rum order and exact affine scalar synthesis. Every continuing
recursive edge must strictly descend; dependent type/purity/acyclicity contracts
remain mandatory. No arbitrary stronger implementation may expand admission.
Source-body certification is distinct from causal stabilization/completion
(Q-020/Q-072), native waits and eventually profiles (Q-030). Those independent
questions are not closed or replaced by body termination.

## Closure criterion

- C1: Specify the certified body classes and exact common ranking/proof/completion procedure.
- C2: Provide contrasting recursive, affine, numeric and failure evidence without waiving independent cycle bans.

## Closure evidence

- C1: MUD-TYPE-044/MUD-TERM-001 through MUD-TERM-003, termination-certification and its common finite-static-certification dependency.
- C2: test_static_certification_witnesses.py, contextual call witnesses and source cases for lexicographic reset, phases, affine synthesis, rational halving, represented Rum descent/stall and action/domain cycles.
