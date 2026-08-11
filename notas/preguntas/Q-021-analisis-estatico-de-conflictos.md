---
id: Q-021
title: Análisis estático de conflictos
status: abierta
priority: P1
opened: true
closed:
decisions:
  - D-023
  - D-026
  - D-031
  - D-046
  - D-054
affects: []
superseded-by: []
---

# Q-021 — Análisis estático de conflictos

## Contenido

Qué conflictos pueden probarse en compilación y cuáles solo en una resolución concreta.

D-023 y [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]] establecen el criterio inicial: un conflicto que el compilador pueda demostrar se rechaza estáticamente; la coincidencia que no pueda decidir se valida en runtime y revierte la transacción si llega a ocurrir. D-054 retira de esta categoría las activaciones coincidentes de una misma `thing` o regla: son idempotentes porque sus definiciones son únicas. D-031 hace inaplicable el caso de aliases.

D-026 endurece el caso de cardinalidad: el compilador debe demostrar la preservación local y consolidada; si no puede, rechaza conservadoramente el programa en vez de diferir el caso al runtime.
