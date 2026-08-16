---
id: Q-012
title: Valores given nombrados
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

# Q-012 — Valores `given` nombrados

## Contenido

Estado: **cerrada** de nuevo mediante [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]], que modifica [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|D-036]].

Los argumentos `given` admiten vinculación posicional y nominal real. Puede aparecer un prefijo posicional seguido por nombres, pero ninguna posición después del primer nombre. Posicionalmente solo se omite un sufijo predeterminado; los nombres pueden omitir predeterminados intermedios y reordenar argumentos. El compilador sugiere restaurar el orden de declaración. Todo `given` tiene nombre obligatorio, es inmutable y su predeterminado, si existe, es una expresión estática cerrada independiente de participantes, otros `given`, valores locales y estado del mundo.

## Criterio de cierre

- C1: La resolución aceptada cubre todo el alcance formulado por la pregunta y los artefactos afectados reflejan esa respuesta.

## Evidencia de cierre

- C1: `D-036`, `D-063`.
