---
id: Q-002
title: Exact model of sequential and simultaneous effects
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-10-07
decisions:
  - D-111
  - D-110
  - D-023
  - D-042
  - D-046
  - D-060
  - D-096
  - D-117
  - D-128
affects: []
superseded-by: []
---

# Q-002 — Exact model of sequential and simultaneous effects

## Resolution

[[specification/28-effects]] specifies private statement/effect judgments and the finite root/wave batch boundary for every surviving Surface AST effect family. The author confirms textual mixed-arithmetic sequencing and per-destination staged composition; [[notes/decisions/ADR-128-sequential-effects-and-staged-consolidation|D-128]] records both contrasting cases.

This closes the effect-family formalisation scope, not scheduler implementation, general termination, unresolved numeric operations, circular dynamic domains or native hosting. Those retain their own questions. The corpus is an editorial/reference witness checker, not a complete MUD interpreter.

## Closure criterion

- C1: Define sequential execution and branch normalisation for every surviving effect family, preserving private views, semantic destinations, generations and internal-call contributions.
- C2: Define finite root/wave composition, validation, recovery and rollback boundaries consistent with accepted conflict/cardinality and ownership policies.
- C3: Provide contrasting conformance evidence and mechanical inventory coverage without claiming unsupported engine implementation.

## Closure evidence

- C1: MUD-EFFECT-007 through MUD-EFFECT-011 and sections 1–7 of [[specification/28-effects]] define the judgments and all eight effect families. [[specification/effects/effect-cases.json]] maps every Surface AST effect constructor and all nine assignment operators.
- C2: MUD-EFFECT-012 and sections 8–9 define finite batch validation/checkpoints, occurrence recovery and tentative/outer confirmation. Dictionary joint-uniqueness fallback terminates by permanently rejecting a finite proposal set; chapter 15's static cardinality proof remains mandatory.
- C3: [[specification/effects/README]] distinguishes 21 bounded executable witnesses from reviewed declarative traces. validate_effect_spec.py checks inventory and finite expected results; test_validate_effect_spec.py checks branch permutations, textual-order differences, ledger preservation, rollback-related lifecycle identity and corrupted evidence rejection.
