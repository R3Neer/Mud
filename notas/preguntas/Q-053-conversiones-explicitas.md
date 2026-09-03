---
id: Q-053
title: Explicit conversions
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-07-29
decisions:
  - D-030
  - D-032
  - D-037
  - D-042
  - D-059
  - D-061
affects: []
superseded-by: []
---

# Q-053 — Explicit conversions

## Content

Status: **closed** by [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]], [[notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal|D-032]], [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]], [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]] and [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].

`as` is reserved for specialisation. `to` converts compatible quantitative values or changes nominal type between structurally compatible representations; `in` changes the expression unit of linear and point magnitudes. On a point it transforms the complete coordinate and avoids its `format`; extracting parts uses `unit from container in point`. A `given` outside its domain produces `rejected`, while tentative state with an out-of-domain field produces `failed`. Normalising an inverted interval to `empty` is not itself a violation.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-030`, `D-032`, `D-037`, `D-042`, `D-059`, `D-061`.
