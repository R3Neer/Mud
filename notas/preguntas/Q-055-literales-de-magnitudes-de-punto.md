---
id: Q-055
title: Literales de magnitudes de punto
priority: P2
opened: 2026-07-29
resolved: true
closed: 2026-08-16
decisions:
  - D-061
  - D-062
  - D-089
affects:
  - especificacion/06-lexico.md
  - especificacion/07-gramatica-concreta.md
  - especificacion/gramatica/mud-lexico.ebnf
superseded-by: []
---

# Q-055 — Literales de magnitudes de punto

## Pregunta

¿Cómo puede `~format` definir simultáneamente la representación canónica y una forma literal fuente directa sin exigir que el scanner inicial conozca ya el tipo esperado y la declaración de magnitud resuelta?

## Resolución

D-062 conserva la forma fuente directa, la canonicalidad, la inversión y el dominio. D-089 hace que el scanner base ignore `~format`; cuando una posición posee un único tipo de punto esperado, el clasificador contextual lee el span fuente original y puede producir `POINT_LITERAL` con prioridad sobre la tokenización ordinaria del mismo span. Sin tipo esperado único esa alternativa no existe.

La inversión estática incluye la capacidad de reconocer de forma determinista el final de la representación completa. Por ello no se necesita un delimitador nuevo y tampoco existe dependencia circular del scanner base.

## Criterio de cierre

- C1: el scanner inicial puede ejecutarse sin consultar declaraciones de magnitud.
- C2: una secuencia fuente se reclasifica reproduciblemente cuando el tipo esperado identifica una única magnitud de punto.
- C3: las colisiones con una interpretación ordinaria tienen una prioridad explícita.
- C4: los artefactos léxicos distinguen scanner base y clasificación contextual.

## Evidencia de cierre

- C1: `D-089` y `MUD-LEX-012`.
- C2: `D-062`, `D-089` y `MUD-LEX-013`.
- C3: `D-089` y `MUD-LEX-014`.
- C4: `especificacion/06-lexico.md` y `especificacion/gramatica/mud-lexico.ebnf`.
