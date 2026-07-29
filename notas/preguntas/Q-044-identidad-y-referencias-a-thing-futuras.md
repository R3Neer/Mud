---
id: Q-044
title: Identidad y referencias a thing futuras
status: cerrada
priority: P0
opened:
closed:
decisions:
  - D-054
affects: []
superseded-by: []
---

# Q-044 — Identidad y referencias a `thing` futuras

## Contenido

Estado: **cerrada**.

¿Qué designa el nombre activado por `create A`?

Decisión vigente: [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

`A` posee una única definición canónica de primer nivel y es resoluble antes de estar activa. `create A` solo solicita su activación. Tras `destroy A`, una ejecución posterior reactiva la misma identidad; nunca fabrica un segundo `A` ni modifica sus antecesoras.

Las operaciones que requieran presencia activa deben comprobarla. El nacimiento y la memoria de las vinculaciones `on` continúan coordinados con Q-005.
