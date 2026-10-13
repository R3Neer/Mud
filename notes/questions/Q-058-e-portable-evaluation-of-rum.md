---
id: Q-058
title: Portable evaluation of Rum
priority: P2
opened: 2026-07-29
resolved: true
closed: 2026-10-13
decisions:
  - D-160
  - D-034
affects:
  - specification/11-type-system.md
  - specification/21-expressions.md
superseded-by: []
---

# Q-058 — Portable evaluation of Rum

## Resolution

D-160 fixes exact decimal decoding and single nearest-even conversion; all finite binary64/subnormal values, gradual underflow and canonical positive zero; per-site arithmetic precision and truncating mathematical quotient for remainder; value/fault/demand-preserving constant evaluation and contraction; canonical semantic words and existing-signature derived magnitude inference. Nonfinite results and zero divisors remain errors. Physical IR schema and foreign ABI stay with Q-009/Q-069/Q-070 rather than numeric semantics.

## Closure criterion

- C1: Literal conversion, operations, subnormal/overflow/zero cases and canonical numeric representation are specified and evidenced.
- C2: Constant evaluation/contraction and derived magnitude representation boundaries are specified and evidenced.

## Closure evidence

- C1: D-160, MUD-TYPE-038 in specification/11-type-system.md, Rum declarative cases and test_rum_witnesses.py exact-rational certificates for normal/subnormal/tie/overflow/remainder boundaries.
- C2: MUD-TYPE-038 and MUD-TYPE-037, source-site rounding and contraction certificate, explicit mixed-representation rejection cases and unchanged source/nominal models.
