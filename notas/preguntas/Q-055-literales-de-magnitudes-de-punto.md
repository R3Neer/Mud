---
id: Q-055
title: Literales de magnitudes de punto
status: cerrada
priority: P2
opened:
closed: 2026-07-29
decisions:
  - D-061
  - D-062
affects:
  - especificacion/06-lexico.md
  - especificacion/07-gramatica-concreta.md
superseded-by: []
---

# Q-055 — Literales de magnitudes de punto

## Pregunta

¿La propiedad `format` de una magnitud de punto define también la forma de sus literales fuente y, si es así, cómo se resuelven la inversión, la precisión omitida, las colisiones y el dominio?

## Contexto

D-061 definió la representación de magnitudes de punto y la extracción de sus componentes, pero dejó sin cerrar si una representación como `12:30:00` podía volver a convertirse en un valor fuente mediante `POINT_LITERAL`.

## Ya decidido

D-061 fija:

- la sintaxis de plantilla usada por `format`;
- el significado de los componentes contextuales;
- la representación numérica de cada hueco;
- la extracción de componentes respecto del origen canónico.

## Resolución

[[notas/decisiones/ADR-062-literales-canonicos-de-magnitudes-de-punto|D-062]] cierra la pregunta:

- un tipo de punto con `format` admite como literal únicamente su representación canónica exacta;
- el tipo esperado debe seleccionar unívocamente la magnitud;
- el formato debe ser estáticamente invertible;
- toda precisión inferior no representada toma valor cero;
- sin `format` se usa una cantidad ordinaria con una unidad compatible;
- el valor reconstruido debe pertenecer al dominio declarado;
- un dominio cíclico no normaliza literales fuera de rango.

## Criterio de cierre

Cumplido por D-062 y su incorporación al léxico y la gramática concreta.
