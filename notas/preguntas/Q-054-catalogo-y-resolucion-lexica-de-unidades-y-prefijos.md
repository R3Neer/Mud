---
id: Q-054
title: Catálogo y resolución léxica de unidades y prefijos
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-076
affects:
  - especificacion/06-lexico.md
  - especificacion/gramatica/mud-lexico.ebnf
superseded-by: []
---

# Q-054 — Catálogo y resolución léxica de unidades y prefijos

## Pregunta

¿Cómo se reconocen las formas de unidad configuradas por declaraciones del propio programa sin hacer depender el scanner inicial de una magnitud ya parseada y resuelta, y qué colisiones léxicas son admisibles?

## Ya decidido

- D-076 exige identificador de unidad, catálogo SI, normalización de micro y resolución contextual entre identificador, `~name`, `~plural` y `~abbreviation`.
- La unidad puede escribirse adyacente a una cantidad y la forma canónica posterior inserta el espacio correspondiente.
- Las colisiones semánticas entre magnitudes pueden resolverse mediante tipo esperado o cualificación.

## Pendiente

- C1: fijar una arquitectura de reconocimiento que no exija conocer el catálogo semántico de unidades durante el scanner inicial.
- C2: fijar las condiciones de admisibilidad y desambiguación cuando una forma configurada colisiona con tokens o secuencias ordinarias del lenguaje.
- C3: añadir casos de conformidad que distingan colisión local, resolución contextual y forma léxicamente imposible.

## Criterio de cierre

- C1: el pipeline separa de forma explícita el reconocimiento inicial de la resolución contextual de formas de unidad.
- C2: toda forma fuente de unidad tiene una regla determinista de delimitación y desambiguación.
- C3: la suite de conformidad cubre las colisiones y el contexto esperado.

## Resolución

D-076 resolvió el catálogo, los nombres y la semántica contextual, pero no formalizó todavía el bootstrapping léxico ni todas las colisiones con el tokenizado general. La pregunta permanece parcialmente decidida.
