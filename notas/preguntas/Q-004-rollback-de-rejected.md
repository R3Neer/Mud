---
id: Q-004
title: Rollback de rejected
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-07-28
decisions:
  - D-042
affects: []
superseded-by: []
---

# Q-004 — Rollback de `rejected`

## Contenido

Estado: **cerrada** mediante [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]].

Todo resultado distinto de `accepted`, incluido un `after` falso, restaura exactamente el estado estable anterior y no publica mensajes ni efectos externos.

## Criterio de cierre

- C1: La resolución aceptada cubre todo el alcance formulado por la pregunta y los artefactos afectados reflejan esa respuesta.

## Evidencia de cierre

- C1: `D-042`.
