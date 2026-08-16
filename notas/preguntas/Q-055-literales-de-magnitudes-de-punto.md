---
id: Q-055
title: Literales de magnitudes de punto
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-061
  - D-062
affects:
  - especificacion/06-lexico.md
  - especificacion/07-gramatica-concreta.md
  - especificacion/gramatica/mud-lexico.ebnf
superseded-by: []
---

# Q-055 — Literales de magnitudes de punto

## Pregunta

¿Cómo puede `~format` definir simultáneamente la representación canónica y una forma literal fuente directa sin exigir que el scanner inicial conozca ya el tipo esperado y la declaración de magnitud resuelta?

## Ya decidido

D-062 fija que:

- una magnitud de punto con `~format` admite como literal su representación canónica exacta;
- el tipo esperado debe seleccionar unívocamente la magnitud;
- el formato debe ser estáticamente invertible;
- la precisión inferior omitida toma valor cero;
- sin `~format` se usa una cantidad ordinaria con unidad compatible;
- el valor reconstruido debe pertenecer al dominio declarado;
- un dominio cíclico no normaliza literales fuente fuera de rango.

También está aceptado que `~format` **sí** define sintaxis fuente directa: no se sustituirá por un literal textual delimitado obligatorio.

## Pendiente

- C1: separar el scanner inicial de la clasificación contextual del literal de punto.
- C2: definir cómo se conserva y delimita la secuencia fuente candidata hasta que exista un único tipo esperado.
- C3: hacer determinista la prioridad entre una coincidencia de `~format` y las tokenizaciones ordinarias de la misma secuencia.
- C4: incorporar la arquitectura resultante a léxico, gramática/CST y conformidad sin introducir dependencia circular.

## Criterio de cierre

- C1: el scanner inicial puede ejecutarse sin consultar declaraciones de magnitud.
- C2: una secuencia fuente puede reinterpretarse de forma reproducible cuando el tipo esperado identifica una única magnitud de punto.
- C3: las colisiones con números, palabras, operadores y puntuación tienen una regla explícita.
- C4: los artefactos mecánicos y casos de conformidad representan la misma frontera.

## Resolución

D-062 resolvió canonicalidad, inversión, precisión y dominio. Queda pendiente formalizar la arquitectura léxica contextual que permite usar directamente la salida de `~format` como literal fuente.
