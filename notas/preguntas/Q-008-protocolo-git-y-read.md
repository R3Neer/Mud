---
id: Q-008
title: Protocolo Git y READ
status: parcialmente-decidida
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-053
affects: []
superseded-by: []
---

# Q-008 — Protocolo Git y `READ`

## Contenido

¿Qué operaciones producen commit? Propuesta: consultas `READ` no; CREATE, UPDATE, RETIRE y migraciones sí.

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-053-operador-semantico-y-flujo-de-autoria|D-053]].

Las consultas `READ` puras no producen commit y todo cambio confirmado se limita al plan sin descartar trabajo ajeno. Falta fijar el formato estable del mensaje, el aislamiento técnico y qué derivados se versionan.
