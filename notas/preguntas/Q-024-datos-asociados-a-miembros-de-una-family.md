---
id: Q-024
title: Datos asociados a miembros de una family
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-07-28
decisions:
  - D-038
affects: []
superseded-by: []
---

# Q-024 — Datos asociados a miembros de una `family`

## Contenido

Estado: **cerrada** mediante [[notas/decisiones/ADR-038-familias-cerradas-de-valores|D-038]].

Una `family` puede declarar directamente un esquema uniforme de datos inmutables, almacenados o calculados, antes de sus miembros. Cada miembro puede sustituir valores almacenados en un subbloque; los omitidos proceden primero del predeterminado explícito del dato y después del predeterminado de su tipo. Los datos calculados se evalúan estáticamente para cada miembro, tienen tipo opcional si puede inferirse de forma unívoca, admiten dependencias acíclicas con otros datos asociados y no pueden sustituirse en el miembro. Los datos no alteran la identidad ni la igualdad nominal del miembro.
