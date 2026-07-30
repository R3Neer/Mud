---
id: Q-057
title: Capacidad interior dentro de valores de alias
status: cerrada
priority: P2
opened:
closed: 2026-07-30
decisions:
  - "D-031"
affects:
  - "aliases estructurales, capacidades y gramática concreta"
superseded-by: []
---

# Q-057 — Capacidad interior dentro de valores de alias

## Pregunta

Si una representación de alias contiene una colección de `thing`, decidir si puede declarar capacidad interior `[mut]` aunque el valor de alias sea inmutable, qué autoridad concede y cómo se conserva la distinción entre modificar un miembro alcanzado y reemplazar la colección contenida.

## Resolución

Sí. Un componente de alias no admite `mut` exterior, pero su especificación de colección puede declarar `[mut]`. Esa capacidad permite modificar las `thing` contenidas directamente sin volver reemplazable la colección ni actualizable el componente. No se propaga implícitamente a través de aliases o contenedores anidados.

La decisión queda incorporada en [[notas/decisiones/ADR-031-aliases-nominales-e-inmutables|D-031]] y en la gramática concreta.
