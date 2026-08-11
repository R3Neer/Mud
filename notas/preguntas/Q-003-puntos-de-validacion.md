---
id: Q-003
title: Puntos de validación
status: parcialmente-decidida
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-026
  - D-037
affects: []
superseded-by: []
---

# Q-003 — Puntos de validación

## Contenido

¿En qué momento exacto se validan dominios, cardinalidades y `always`: tras cada escritura, al cerrar la raíz, al cerrar cada onda o en varios de esos puntos?

La respuesta afecta qué estados tentativos son observables para reglas posteriores.

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]] y [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]].

La cardinalidad final se demuestra estáticamente para cada `then` y para toda consolidación concurrente posible. Los estados intermedios dentro del delta privado de un `then` pueden incumplirla. Los dominios se preservan en inicialización, materialización, especialización, escrituras, raíces, ondas y estados publicables. Siguen abiertos la formulación operacional unificada, el tratamiento exacto de referencias suspendidas y los puntos de comprobación de reglas `always`.
