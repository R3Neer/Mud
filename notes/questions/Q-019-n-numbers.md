---
id: Q-019
title: Numbers
priority: P1
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-028
  - D-030
  - D-034
  - D-040
  - D-060
  - D-067
  - D-080
affects: []
superseded-by: []
---

# Q-019 — Numbers

## Content

Premise status: **partially decided** by [[notes/decisions/ADR-028-system-of-quantities-and-units|D-028]], [[notes/decisions/ADR-030-explicit-quantitative-conversion-using-to|D-030]], [[notes/decisions/ADR-034-num-exactly-and-rum-binary64|D-034]], [[notes/decisions/ADR-040-semantics-remaining-basic-numeracy|D-040]], [[notes/decisions/ADR-060-additive-deltas-and-nat-normalisation|D-060]], [[notes/decisions/ADR-067-short-names-for-numeric-types|D-067]] and [[notes/decisions/ADR-080-algebra-higher-and-updates-de-collection|D-080]].

`Nat`, `Int`, `Num`, `Rum` and `Money` are basic numeric representations. `Num` is exact rational; `Rum` is `binary64`; they are not implicitly mixed. `Money` uses exact decimal scale two, has no literal suffix and applies global round-to-nearest, ties-to-even. Ordinary exact widening follows `Nat → Int → Num`. Pure natural subtraction saturates at zero; additive effects sum signed deltas before one normalisation. D-080 lifts arithmetic over collections when at least one operand has upper bound one and makes `empty` absorbing. The following remain to be fixed:

- Representation limits and overflow for `Nat`, `Int` and `Money`.
- The complete inference matrix for `Money` against other representations and magnitudes.
- Arithmetic failures not expressly covered by D-034.
