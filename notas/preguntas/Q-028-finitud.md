---
id: Q-028
title: Finitud
status: parcialmente-decidida
priority: P2
opened:
closed:
decisions:
  - D-044
  - D-047
  - D-081
affects: []
superseded-by: []
---

# Q-028 — Finitud

## Contenido

Límites del análisis, aproximaciones conservadoras y mensajes cuando no puede demostrarse.

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-044-alcanzabilidad-eventually|D-044]], [[notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita|D-047]] y [[notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]].

La incapacidad de demostrar finitud o enumerabilidad rechaza estáticamente el uso que las exige; no produce una respuesta negativa en runtime. La misma obligación se aplica a filtros y `take`. Falta definir el análisis y sus diagnósticos.
