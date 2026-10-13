---
id: Q-078
title: Unitless point construction
priority: P1
opened: 2026-10-14
resolved: true
closed: 2026-10-14
decisions:
  - D-163
affects:
  - specification/11-type-system.md
  - specification/21-expressions.md
  - specification/19-magnitudes.md
superseded-by: []
---

# Q-078 — Unitless point construction

## Resolution

The author accepts a point over a unitless magnitude. Without ~format, its bare
numeric literal uses unique expected point context; an already typed number uses
explicit to. Preserve nominality, representation/domain checks and literal
rejection before cycle correction. No units or extraction syntax are invented.

## Closure criterion

- C1: Literal/expression construction and nominal/domain boundaries are specified.
- C2: Missing unit operations and cyclic-literal behavior are distinguished with conformance cases.

## Closure evidence

- C1: D-163, MUD-TYPE-041 and chapter 19's point-coordinate rules, with unitless point cases in specification/types/typing-cases.yaml.
- C2: Unitless presentation rejection and out-of-domain cycle literal cases; D-062/D-083 reconciled without adding grammar or HIR forms.
