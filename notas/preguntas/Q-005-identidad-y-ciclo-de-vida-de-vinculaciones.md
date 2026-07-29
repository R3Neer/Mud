---
id: Q-005
title: Identidad y ciclo de vida de vinculaciones
status: parcialmente-decidida
priority: P0
opened:
closed:
decisions:
  - D-041
  - D-045
  - D-058
affects: []
superseded-by: []
---

# Q-005 — Identidad y ciclo de vida de vinculaciones

## Contenido

¿Cómo se identifica canónicamente una vinculación `on`, cuándo se elimina su memoria y qué ocurre si una vinculación equivalente desaparece y reaparece?

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola|D-045]] y [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]].

La memoria temporal pertenece a la vinculación; estas se fijan al inicio de cada onda y sus altas o bajas surten efecto en la siguiente. Una vinculación presente en la primera instantánea materializada por `start with` usa un anterior virtual falso para ramas booleanas y la propia instantánea para `changes` y `old`; una nacida después usa su primera onda activa para establecer toda la línea base sin disparar. Falta definir su identidad canónica y la política de eliminación o conservación de memoria cuando desaparece.
