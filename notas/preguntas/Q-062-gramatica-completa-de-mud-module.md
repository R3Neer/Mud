---
id: Q-062
title: Gramática completa de `mud.module`
priority: P1
opened: 2026-08-28
resolved: false
closed:
decisions:
  - D-096
affects:
  - gramática de módulo, texto fuente, tooling
superseded-by: []
---

# Q-062 — Gramática completa de `mud.module`

## Contenido

Fijar la sintaxis completa del archivo `mud.module` sin reabrir lo ya decidido por D-096: el archivo se llama `mud.module`, delimita el módulo por ancestro más cercano y `uses` es la construcción que declara dependencias de contrato. Quedan por fijar la repetición y agrupación de entradas `uses`, sus separadores/terminadores, la estructura completa del archivo y cualquier propiedad adicional, sin duplicar el MudPath derivado del directorio.
