---
id: Q-051
title: Identidad y selección de un look
priority: P1
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-027
  - D-061
affects: []
superseded-by: []
---

# Q-051 — Identidad y selección de un `look`

## Contenido

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-027-salidas-look-y-message|D-027]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].

Un `look` es una consulta pública pura cuyos campos se evalúan sobre un único estado estable. Una magnitud usada directamente selecciona su unidad con `in`; omitirla usa la unidad raíz o combinación canónica y emite un aviso. Un punto directo publica su coordenada, mientras que su formato se publica construyendo `Text`. Falta definir la sintaxis de solicitud, el tratamiento de participantes inactivos, la posible multiplicidad de filas y la serialización recursiva de aliases, colecciones y magnitudes anidadas.
