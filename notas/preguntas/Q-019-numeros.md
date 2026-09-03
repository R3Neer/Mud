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

Premise status: **partially decided** by [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]], [[notas/decisiones/ADR-034-number-exacto-y-rumber-binary64|D-034]], [[notas/decisiones/ADR-040-semantica-numerica-basica-restante|D-040]], [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]], [[notas/decisiones/ADR-067-nombres-breves-de-tipos-numericos|D-067]] and [[notas/decisiones/ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|D-080]].

`Nat`, `Int`, `Num`, `Rum` and `Money` are basic numeric representations. `Num` is exact rational; `Rum` is `binary64`; they are not implicitly mixed. `Money` uses exact decimal scale two, has no literal suffix and applies global round-to-nearest, ties-to-even. Ordinary exact widening follows `Nat → Int → Num`. Pure natural subtraction saturates at zero; additive effects sum signed deltas before one normalisation. D-080 lifts arithmetic over collections when at least one operand has upper bound one and makes `empty` absorbing. The following remain to be fixed:

- Representation limits and overflow for `Nat`, `Int` and `Money`.
- The complete inference matrix for `Money` against other representations and magnitudes.
- Arithmetic failures not expressly covered by D-034.
