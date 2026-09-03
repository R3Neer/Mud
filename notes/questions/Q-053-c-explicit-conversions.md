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

Status: **closed** by [[notes/decisions/ADR-030-explicit-quantitative-conversion-using-to|D-030]], [[notes/decisions/ADR-032-contextual-construction-and-nominal-casting-of-aliases|D-032]], [[notes/decisions/ADR-037-fields-and-declarative-domains|D-037]], [[notes/decisions/ADR-042-shares-root-and-results|D-042]], [[notes/decisions/ADR-059-magnitude-intervals-and-inverted-endpoints|D-059]] and [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]].

`as` is reserved for specialisation. `to` converts compatible quantitative values or changes nominal type between structurally compatible representations; `in` changes the expression unit of linear and point magnitudes. On a point it transforms the complete coordinate and avoids its `format`; extracting parts uses `unit from container in point`. A `given` outside its domain produces `rejected`, while tentative state with an out-of-domain field produces `failed`. Normalising an inverted interval to `empty` is not itself a violation.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-030`, `D-032`, `D-037`, `D-042`, `D-059`, `D-061`.
