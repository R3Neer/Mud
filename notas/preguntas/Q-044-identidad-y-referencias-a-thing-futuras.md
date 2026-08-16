---
id: Q-044
title: Identidad y referencias a thing futuras
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-07-28
decisions:
  - D-054
affects: []
superseded-by: []
---

# Q-044 — Identidad y referencias a `thing` futuras

## Contenido

Estado: **cerrada**.

¿Qué designa el nombre activado por `create A`?

Decisión vigente: [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

`A` posee una única definición canónica de primer nivel y es resoluble antes de estar activa. `create A` solo solicita su activación. Tras `destroy A`, una ejecución posterior reactiva la misma identidad; nunca fabrica un segundo `A` ni modifica sus antecesoras.

Las operaciones que requieran presencia activa deben comprobarla. El nacimiento y la memoria de las vinculaciones `on` continúan coordinados con Q-005.

## Criterio de cierre

- C1: La resolución aceptada cubre todo el alcance formulado por la pregunta y los artefactos afectados reflejan esa respuesta.

## Evidencia de cierre

- C1: `D-054`.
