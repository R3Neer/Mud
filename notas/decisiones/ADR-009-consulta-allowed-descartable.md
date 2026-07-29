---
id: D-009
title: "`allowed` como especulación descartable"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-007"
  - "Q-035"
affects:
  - "capítulo de admisibilidad y consultas especulativas"
---

# ADR-009 — `allowed` como especulación descartable

## Contexto

Comprobar solo las precondiciones de una acción puede declarar admisible una
solicitud cuya resolución completa terminaría en conflicto, invariante
incumplida o fallo.

## Decisión

`allowed` ejecuta especulativamente el protocolo de la acción sobre una copia
descartable. No confirma estado ni publica salidas. Los fallos no se convierten
en falsedad: se propagan como fallos de la consulta.

## Consecuencias

D-043 desarrolla la semántica completa y sus observaciones.
