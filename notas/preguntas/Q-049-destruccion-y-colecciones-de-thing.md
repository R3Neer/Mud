---
id: Q-049
title: Destrucción y colecciones de thing
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-08-03
decisions:
  - D-021
  - D-077
affects: []
superseded-by: []
---

# Q-049 — Destrucción y colecciones de `thing`

## Resolución

[[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]] conserva propiedades completas cuando se destruye una dependencia estructural. [[notas/decisiones/ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]] resuelve las identidades contenidas: la retirada solo se confirma si todas las cardinalidades y dominios finales son válidos; una relación inmutable conserva pertenencia latente y una relación `mut` la elimina permanentemente. `create` restaura únicamente la primera y vuelve a validar la transición.

No existe una colección efectiva cardinalmente degradada: un incumplimiento produce `failed` y rollback.

## Criterio de cierre

- C1: La resolución aceptada cubre todo el alcance formulado por la pregunta y los artefactos afectados reflejan esa respuesta.

## Evidencia de cierre

- C1: `D-021`, `D-077`.
