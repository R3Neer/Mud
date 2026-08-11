---
id: Q-043
title: Ciclos de especialización
status: cerrada
priority: P0
opened: false
closed: 2026-07-27
decisions:
  - D-015
affects: []
superseded-by: []
---

# Q-043 — Ciclos de especialización

## Contenido

Estado: **cerrada**.

¿Debe rechazarse cualquier ciclo no trivial de especialización directa?

Decisión: [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]].

Todo ciclo de especialización directa es inválido. La relación semántica `is` es un orden parcial.
