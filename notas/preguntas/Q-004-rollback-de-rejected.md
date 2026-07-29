---
id: Q-004
title: Rollback de rejected
status: cerrada
priority: P0
opened:
closed:
decisions:
  - D-042
affects: []
superseded-by: []
---

# Q-004 — Rollback de `rejected`

## Contenido

Estado: **cerrada** mediante [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]].

Todo resultado distinto de `accepted`, incluido un `after` falso, restaura exactamente el estado estable anterior y no publica mensajes ni efectos externos.
