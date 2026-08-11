---
id: Q-050
title: Borrado en operadores booleanos restantes
priority: P1
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-022
affects: []
superseded-by: []
---

# Q-050 — Borrado en operadores booleanos restantes

## Contenido

Estado de la premisa: **decidida** mediante [[notas/decisiones/ADR-022-borrado-de-reglas-booleanas-inactivas|D-022]].

Las llamadas a reglas booleanas inactivas se podan después de un desazucarado canónico a `not`, `and` y `or`. Falta fijar la elaboración de `!=`, `xor`, cuantificadores booleanos y las interacciones con `allowed`, `eventually` y fallos internos.
