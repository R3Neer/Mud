---
id: Q-006
title: Conflictos
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-023
  - D-039
  - D-046
  - D-060
  - D-080
  - D-098
  - D-100
affects: []
superseded-by: []
---

# Q-006 — Conflictos

## Pregunta

¿Cuál es la matriz completa de compatibilidad entre asignaciones, incrementos, multiplicaciones y operaciones estructurales concurrentes?

## Ya decidido

La pregunta está **parcialmente decidida** mediante [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]], [[notas/decisiones/ADR-039-colecciones-y-diccionarios|D-039]], [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]], [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]], [[notas/decisiones/ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|D-080]], [[notas/decisiones/ADR-098-rutas-asignables-y-write-back-de-aliases|D-098]] y [[notas/decisiones/ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].

Ya están fijadas las asignaciones iguales o distintas; la forma aritmética concurrente `(Δ, P, Q)` con bloque aditivo previo al multiplicativo; el núcleo estructural `create → add → remove → destroy`; la composición de `add` y `remove` sobre una misma presencia; las actualizaciones homogéneas `|=`, `&=`, `^=` y `--=` ya decididas; la consolidación idempotente de varias adiciones del mismo valor a una colección `unique`; el desempate reproducible de procedencia para inserciones concurrentes; y la semántica secuencial de reconstrucción/write-back de aliases almacenados. En `Nat`, los deltas aditivos se suman como enteros firmados y solo después se normalizan a cero.

## Pendiente

Queda completar las familias para las que todavía no existe combinación algebraica ni composición canónica concreta, incluidos los casos restantes de diccionarios, propiedades, límites estructurales de cardinalidad y destinos o write-backs parcialmente solapados. También queda por fijar la precisión mínima obligatoria del análisis estático que distingue conflicto inevitable, posible e imposible.

## Criterio de cierre

- C1. Existe una clasificación completa para las combinaciones concurrentes restantes de diccionarios que puedan coincidir sobre un mismo destino semántico.
- C2. Existe una clasificación completa para operaciones sobre propiedades y límites estructurales de cardinalidad que todavía carezcan de combinación algebraica o composición canónica.
- C3. Existe una regla completa para destinos y write-backs parcialmente solapados, incluida la condición que distingue composición válida de conflicto.
- C4. Está fijada la precisión mínima obligatoria del análisis estático para distinguir conflicto inevitable, posible e imposible.

## Resolución

Pendiente de satisfacer C1-C4.
