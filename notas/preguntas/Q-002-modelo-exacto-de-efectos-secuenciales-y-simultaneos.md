---
id: Q-002
title: Modelo exacto de efectos secuenciales y simultáneos
status: parcialmente-decidida
priority: P0
opened:
closed:
decisions:
  - D-023
  - D-042
  - D-046
  - D-060
affects: []
superseded-by: []
---

# Q-002 — Modelo exacto de efectos secuenciales y simultáneos

## Contenido

¿Qué estado lee cada instrucción de un `then` elemental y cada hoja de una acción compuesta? ¿Cómo se combinan efectos de una misma raíz?

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]], [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]] y [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]].

Cada `then` se interpreta secuencialmente sobre un delta privado derivado de la instantánea común y no observa deltas parciales ajenos. En `Nat`, una lectura privada proyecta a cero la suma del valor inicial y el delta local acumulado sin recortar el delta. Las hojas de una acción compuesta leen el mismo estado inicial y forman una raíz simultánea. Falta una semántica operacional para las lecturas intermedias de las demás familias de efectos y todas sus combinaciones.
