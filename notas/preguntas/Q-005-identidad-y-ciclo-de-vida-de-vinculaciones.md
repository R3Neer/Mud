---
id: Q-005
title: Identidad y ciclo de vida de vinculaciones
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-041
  - D-045
  - D-058
  - D-099
affects: []
superseded-by: []
---

# Q-005 — Identidad y ciclo de vida de vinculaciones

## Contenido

¿Cómo se identifica canónicamente una vinculación `on`, cuándo se elimina su memoria y qué ocurre si una vinculación equivalente desaparece y reaparece?

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola|D-045]], [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]] y [[notas/decisiones/ADR-099-materializaciones-frescas-tras-destroy-create|D-099]].

La memoria temporal pertenece a la vinculación; estas se fijan al inicio de cada onda y sus altas o bajas surten efecto en la siguiente. Una vinculación presente en la primera instantánea materializada por `start with` usa un anterior virtual falso para ramas booleanas y la propia instantánea para `changes` y `old`; una nacida después usa su primera onda activa para establecer toda la línea base sin disparar.

D-099 fija un caso de eliminación: `destroy` explícito de una rule descarta la memoria temporal de esa activación y un `create` posterior establece una línea base nueva sin disparar por la mera reactivación. Sigue faltando definir la identidad canónica de una vinculación y la política de memoria cuando desaparece por cambios de participantes o cuando la rule queda meramente suspendida por una dependencia, sin `destroy` explícito.
