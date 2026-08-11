---
id: Q-011
title: Vinculación nombrada de participantes
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-07-30
decisions:
  - D-036
  - D-063
affects: []
superseded-by: []
---

# Q-011 — Vinculación nombrada de participantes

## Contenido

Estado: **cerrada** mediante [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|D-036]], modificada por [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]].

Una llamada puede usar un receptor posicional o un receptor nombrado entre paréntesis. La forma nombrada debe ser exacta, exhaustiva y no mezclable con posiciones: no admite roles ausentes, repetidos ni desconocidos. Puede reordenar roles, pero el compilador sugiere el orden de declaración. Los roles `for` pueden contener cualquier tipo de valor; una colección ocupa una sola posición y no se expande. Una `thing` se vincula por identidad, un valor inmutable por valor y un rol exteriormente mutable por lugar almacenado. Los argumentos posteriores corresponden exclusivamente a `given`.
