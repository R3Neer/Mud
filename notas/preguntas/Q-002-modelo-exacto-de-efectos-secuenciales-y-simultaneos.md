---
id: Q-002
title: Modelo exacto de efectos secuenciales y simultáneos
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-023
  - D-042
  - D-046
  - D-060
  - D-096
affects: []
superseded-by: []
---

# Q-002 — Modelo exacto de efectos secuenciales y simultáneos

## Contenido

¿Cómo se formalizan operacionalmente las lecturas y consolidaciones de todas las familias de efectos dentro de un `then` secuencial y entre deltas independientes de una misma resolución?

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]], [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]], [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]] y [[notas/decisiones/ADR-096-modulos-callables-look-message-y-activacion|D-096]].

D-096 fija que no existen actions elementales/compuestas: cada `then` se interpreta secuencialmente sobre su delta privado y una llamada interna observa el delta en su posición textual, aporta sus efectos a la misma resolución y deja esos efectos visibles a las sentencias posteriores. Ningún bloque observa deltas parciales de otros bloques independientes. En `Nat`, una lectura privada proyecta a cero la suma del valor inicial y el delta local acumulado sin recortar el delta.

Permanece abierta la semántica operacional completa de las lecturas intermedias para las demás familias de efectos y de su consolidación cuando varios deltas independientes concurren en una misma resolución.
