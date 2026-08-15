---
id: Q-029
title: Terminación
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-047
  - D-088
affects: []
superseded-by: []
---

# Q-029 — Terminación

## Contenido

Qué clases de acciones y reglas puede certificar el compilador.

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita|D-047]] y [[notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]. Una iteración exhaustiva solo es válida sobre una fuente cuya finitud y enumerabilidad puedan demostrarse; una progresión posee paso fijo por ejecución y los dominios cíclicos se limitan a un periodo fundamental. Permanece abierta la certificación general de terminación de actions, reglas y composiciones más amplias.
