---
id: Q-054
title: Catálogo y resolución léxica de unidades y prefijos
priority: P2
opened: 2026-07-29
resolved: true
closed: 2026-08-16
decisions:
  - D-076
  - D-089
affects:
  - especificacion/06-lexico.md
  - especificacion/gramatica/mud-lexico.ebnf
superseded-by: []
---

# Q-054 — Catálogo y resolución léxica de unidades y prefijos

## Pregunta

¿Cómo se reconocen las formas de unidad configuradas por declaraciones del propio programa sin hacer depender el scanner inicial de una magnitud ya parseada y resuelta, y qué colisiones léxicas son admisibles?

## Resolución

D-076 fija catálogo, formas habilitadas, prefijos y adyacencia. D-089 separa el scanner base del clasificador contextual: `UNIT_FORM` se crea únicamente sobre el texto fuente cuando el catálogo semántico ya está resuelto. El tipo esperado restringe candidatos; sin él se exige unicidad global, las coincidencias de distinta longitud usan la forma completa más larga y un mismo span con varios candidatos sigue siendo ambiguo. `MUD-LEX-016` permite espacios en `~name`, `~plural` y `~abbreviation` cuando actúan como forma fuente, exige al menos un carácter alfabético y excluye cualquier palabra clave de MUD; `MUD-LEX-017` comprueba colisiones dentro de una magnitud después de expandir todas las combinaciones de prefijos permitidas.

## Criterio de cierre

- C1: el pipeline separa de forma explícita el reconocimiento inicial de la resolución contextual de formas de unidad.
- C2: toda forma fuente de unidad tiene una regla determinista de delimitación y desambiguación.
- C3: la norma exige conformidad para colisiones, contexto esperado y adyacencia.

## Evidencia de cierre

- C1: `D-089`, `MUD-LEX-012` y `MUD-LEX-013`.
- C2: `D-089`, `MUD-LEX-015`, `MUD-LEX-016` y `MUD-LEX-017`.
- C3: verificación de D-089 y reglas `MUD-LEX-015` a `MUD-LEX-017`, además de la adyacencia de D-076/06-léxico.
