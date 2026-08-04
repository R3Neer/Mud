---
id: Q-019
title: Números
status: parcialmente-decidida
priority: P1
opened:
closed:
decisions:
  - D-028
  - D-030
  - D-034
  - D-040
  - D-060
  - D-067
  - D-080
affects: []
superseded-by: []
---

# Q-019 — Números

## Contenido

Estado de la premisa: **parcialmente decidida** mediante [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]], [[notas/decisiones/ADR-034-number-exacto-y-rumber-binary64|D-034]], [[notas/decisiones/ADR-040-semantica-numerica-basica-restante|D-040]], [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]], [[notas/decisiones/ADR-067-nombres-breves-de-tipos-numericos|D-067]] y [[notas/decisiones/ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|D-080]].

`Nat`, `Int`, `Num`, `Rum` y `Money` son representaciones numéricas básicas. `Num` es racional exacto; `Rum` es `binary64`; no se mezclan implícitamente. `Money` usa decimal exacto de escala dos, no tiene sufijo literal y aplica el redondeo global al más cercano con empates al par. La ampliación exacta ordinaria sigue `Nat → Int → Num`. La resta pura de naturales satura en cero; los efectos aditivos suman deltas firmados antes de una única normalización. D-080 eleva la aritmética sobre colecciones cuando al menos un operando tiene límite superior uno y hace `empty` absorbente. Falta fijar:

- Los límites de representación y overflow de `Nat`, `Int` y `Money`.
- La matriz completa de inferencia de `Money` frente a otras representaciones y magnitudes.
- Los fallos aritméticos no cubiertos expresamente por D-034.
