---
id: Q-057
title: Capacidad interior dentro de valores de alias
status: abierta
priority: P2
opened:
closed:
decisions: []
affects: []
superseded-by: []
---

# Q-057 — Capacidad interior dentro de valores de alias

## Contenido

Si una representación de alias contiene una colección de `thing`, decidir si puede declarar capacidad interior `[mut]` aunque el valor de alias sea inmutable, qué autoridad concede y cómo se conserva la distinción entre modificar un miembro alcanzado y reemplazar la colección contenida.
