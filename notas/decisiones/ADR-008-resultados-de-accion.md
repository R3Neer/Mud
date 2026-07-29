---
id: D-008
title: "Resultados `accepted`, `rejected` y `failed`"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-007"
affects:
  - "capítulos de acciones, resultados y diagnósticos"
---

# ADR-008 — Resultados `accepted`, `rejected` y `failed`

## Contexto

Una solicitud inadmisible y un fallo de resolución no expresan la misma
situación. Confundirlos impide distinguir una negativa normal del dominio de un
problema que invalida la ejecución tentativa.

## Decisión

Una acción produce exclusivamente:

- `accepted`, cuando confirma su transición;
- `rejected`, cuando la solicitud no se admite sin constituir un fallo técnico
  o semántico de la resolución;
- `failed`, cuando la resolución no puede producir un estado confirmable.

Los resultados no aceptados no publican cambios parciales.

## Consecuencias

D-042 define el protocolo completo de las acciones. D-061 exige una razón
`Text` para todo resultado no aceptado.
