---
id: Q-013
title: Restricciones relacionales entre participantes on
status: cerrada
priority: P1
opened:
closed:
decisions:
  - D-036
affects: []
superseded-by: []
---

# Q-013 — Restricciones relacionales entre participantes `on`

## Contenido

Estado: **cerrada** mediante [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|D-036]].

La cabecera puede construir participantes relacionados mediante `role: Type in previousRole.relation`. Las condiciones relacionales que no formen parte de esa vinculación estructural se expresan en `if`; `given` no está permitido en declaraciones `on`.
