---
id: Q-032
title: Aleatoriedad reproducible
status: parcialmente-decidida
priority: P2
opened:
closed:
decisions:
  - D-048
affects: []
superseded-by: []
---

# Q-032 — Aleatoriedad reproducible

## Contenido

Subsemillas, cachés, identidad de puntos aleatorios y exposición de campos estocásticos.

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-048-azar-reproducible-y-fallos|D-048]].

Todo punto aleatorio tiene identidad semántica, deriva de una semilla y un campo calculado mantiene su muestra dentro de una instantánea. Falta el algoritmo de subsemillas, cachés, reintentos y exposición.
