---
id: Q-006
title: Conflictos
status: parcialmente-decidida
priority: P0
opened:
closed:
decisions:
  - D-023
  - D-039
  - D-046
  - D-060
  - D-080
affects: []
superseded-by: []
---

# Q-006 — Conflictos

## Contenido

¿Cuál es la matriz completa de compatibilidad entre asignaciones, incrementos, multiplicaciones y operaciones estructurales concurrentes?

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]], [[notas/decisiones/ADR-039-colecciones-y-diccionarios|D-039]], [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]], [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]] y [[notas/decisiones/ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|D-080]].

Ya están fijadas asignaciones iguales o distintas, acumulaciones homogéneas, mezclas aritméticas incompatibles, el núcleo estructural, las actualizaciones homogéneas `|=`, `&=`, `^=` y `--=`, y la consolidación idempotente de varias adiciones del mismo valor a una colección `unique`. En `Nat`, los deltas aditivos se suman como enteros firmados y solo después se normalizan a cero. Falta completar la matriz para mezclas entre clases de efecto, adiciones y retiradas combinadas, inserciones distintas con orden por entrada, límites de cardinalidad, diccionarios, propiedades, ciclo de vida y destinos parcialmente solapados.
