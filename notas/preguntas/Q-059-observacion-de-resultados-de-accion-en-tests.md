---
id: Q-059
title: Observación de resultados de acción en tests
priority: P1
opened: 2026-07-29
resolved: false
closed:
decisions:
  - D-055
  - D-061
affects: []
superseded-by: []
---

# Q-059 — Observación de resultados de acción en tests

## Contenido

Estado: **abierta** a partir de [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].

¿Cómo comprueba un test que una acción solicitada produjo `accepted`, `rejected` o `failed` sin confundir esos resultados con `passed`, `failed` y `error` del propio test?

Debe decidirse:

- Si una solicitud de acción dentro de `then` puede vincular su resultado a un nombre local.
- Si una acción `rejected` constituye por defecto un error del escenario o un resultado observable.
- Cómo se enlaza el `reason` externo ya definido para `rejected` y `failed`, junto con su traza, sin convertir diagnósticos en valores ordinarios del mundo.
