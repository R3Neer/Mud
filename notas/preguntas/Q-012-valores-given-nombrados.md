---
id: Q-012
title: Named `given` values
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-07-30
decisions:
  - D-036
  - D-063
affects: []
superseded-by: []
---

# Q-012 — Named `given` values

## Content

Status: **closed** again by [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]], which amends [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|D-036]].

`given` arguments support positional binding and genuine named binding. A positional prefix may be followed by names, but no positional argument may follow the first name. Positionally, only a defaulted suffix may be omitted; names may omit intermediate defaults and reorder arguments. The compiler suggests restoring declaration order. Every `given` has a mandatory name, is immutable and, when present, its default is a closed static expression independent of participants, other `given` values, local values and world state.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-036`, `D-063`.
