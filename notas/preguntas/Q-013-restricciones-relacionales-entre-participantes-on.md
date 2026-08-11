---
id: Q-013
title: Restricciones relacionales entre participantes on
status: cerrada
priority: P1
opened: false
closed: 2026-07-30
decisions:
  - D-036
  - D-063
affects: []
superseded-by: []
---

# Q-013 — Restricciones relacionales entre participantes `on`

## Contenido

Estado: **cerrada** de nuevo mediante [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]], que modifica [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|D-036]].

La cabecera puede construir participantes relacionados mediante `role [: Type] in expression`. La anotación refina nominalmente el elemento de la colección. Todos los nombres son visibles en la cabecera completa y sus tipos y restricciones se resuelven conjuntamente, por lo que se admiten referencias adelantadas y ciclos. El universo de cada rol son las `thing` concretas y activas de su tipo efectivo; las vinculaciones forman el join finito que satisface todas las restricciones en una misma instantánea. Los roles conservan orientación y no se impone desigualdad ni deduplicación simétrica. Las condiciones adicionales se expresan en `if`; `given` no está permitido en declaraciones `on`.
