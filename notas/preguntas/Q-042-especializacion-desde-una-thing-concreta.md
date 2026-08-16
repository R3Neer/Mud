---
id: Q-042
title: Especialización desde una thing concreta
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-07-27
decisions:
  - D-015
affects: []
superseded-by: []
---

# Q-042 — Especialización desde una `thing` concreta

## Contenido

Estado: **cerrada**.

Cuando una `thing` concreta $B$ se especializa a partir de otra `thing` concreta $A$, ¿hereda solo las declaraciones, restricciones y valores predeterminados de $A$, o copia u observa también su estado mutable actual?

Decisión: [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]].

Se heredan esquema y predeterminados efectivos, nunca estado activo. Cada `thing` concreta posee estado independiente y su primera activación inicializa desde predeterminados antes de aplicar sus asignaciones explícitas.

## Criterio de cierre

- C1: La resolución aceptada cubre todo el alcance formulado por la pregunta y los artefactos afectados reflejan esa respuesta.

## Evidencia de cierre

- C1: `D-015`.
