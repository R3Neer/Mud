---
id: Q-049
title: Destrucción y colecciones de thing
status: parcialmente-decidida
priority: P0
opened:
closed:
decisions:
  - D-021
affects: []
superseded-by: []
---

# Q-049 — Destrucción y colecciones de `thing`

## Contenido

Estado: **parcialmente cerrada** mediante [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]].

La destrucción no poda ni reescribe colecciones almacenadas. Si el tipo declarado de una propiedad queda inactivo, la propiedad completa se suspende y conserva orden, multiplicidad, claves, cardinalidad y carga para una recreación posterior. No necesita mutabilidad exterior ni valores de reparación.

Permanece abierta la observación de una identidad inactiva dentro de una colección cuyo tipo declarado continúa efectivo por ser más general. También falta coordinar esta observación con iteraciones, diccionarios, `old` y serialización.
