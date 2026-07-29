---
id: Q-012
title: Valores given nombrados
status: cerrada
priority: P1
opened:
closed:
decisions:
  - D-036
affects: []
superseded-by: []
---

# Q-012 — Valores `given` nombrados

## Contenido

Estado: **cerrada** mediante [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|D-036]].

Los argumentos `given` son siempre posicionales y pueden llevar la etiqueta opcional `nombre =` para mejorar la lectura. Se pueden mezclar argumentos etiquetados y no etiquetados en cualquier posición; una etiqueta debe coincidir con el `given` declarado en esa misma posición y nunca permite reordenar.
