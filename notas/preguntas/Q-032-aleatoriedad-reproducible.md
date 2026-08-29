---
id: Q-032
title: Aleatoriedad reproducible
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-048
  - D-081
  - D-100
affects: []
superseded-by: []
---

# Q-032 — Aleatoriedad reproducible

## Pregunta

¿Qué reglas de caché, reintento y exposición completan el contrato de los puntos aleatorios reproducibles?

## Ya decidido

La pregunta está **parcialmente decidida** mediante [[notas/decisiones/ADR-048-azar-reproducible-y-fallos|D-048]], [[notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]] y [[notas/decisiones/ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].

Todo punto aleatorio posee identidad semántica estable y deriva su elección de una semilla reproducible. Un campo calculado mantiene su muestra dentro de una instantánea. `take` sobre una fuente no ordenada con elección real es también un punto aleatorio, uniforme y sin reemplazo. Los puntos de consolidación aleatoria no pueden depender del consumo secuencial accidental de un PRNG global: la elección debe derivarse de la semilla y de la identidad semántica del punto, de modo que puntos independientes no se desplacen mecánicamente por el orden de consumo. El algoritmo concreto de derivación o subsemillas es un detalle de implementación mientras conserve estas propiedades.

## Pendiente

Queda fijar las reglas de caché y reintentos y la exposición de campos o resultados estocásticos.

## Criterio de cierre

- C1. Están fijadas las reglas de caché y reintentos de puntos aleatorios.
- C2. Está fijada la exposición observable de campos y resultados estocásticos.

## Resolución

Pendiente de satisfacer C1-C2.
