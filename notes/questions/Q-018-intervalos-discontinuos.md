---
id: Q-018
title: Discontinuous intervals
priority: P1
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-049
  - D-059
  - D-082
  - D-088
affects: []
superseded-by: []
---

# Q-018 — Discontinuous intervals

## Content

Status: **partially decided** by [[notes/decisions/ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]], [[notes/decisions/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]], [[notes/decisions/ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]] and [[notes/decisions/ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]].

Intervals are normalised by content. For linear intervals, inverted effective endpoints produce `empty` and imply neither descending traversal nor a cycle. `cycle` is a later modifier exclusive to a point domain `[a..b)`, not part of the interval expression. The consolidated syntax and keys for discontinuous intervals remain open. D-088 closes explicit descending traversal: it is expressed with `by` and a negative difference, never by inverting endpoints.
