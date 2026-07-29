---
id: Q-047
title: Selección de predeterminados por tipo
status: parcialmente-decidida
priority: P0
opened:
closed:
decisions:
  - D-017
  - D-026
  - D-031
affects: []
superseded-by: []
---

# Q-047 — Selección de predeterminados por tipo

## Contenido

Estado de la premisa: **decidida** mediante [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|ADR-017]].

Todo tipo bien formado tiene un valor predeterminado perteneciente a su dominio. Los tipos básicos ya tienen selección concreta; en particular, `Char` usa `'\u{0}'` (`U+0000`). D-031 fija que un alias estructural compone el suyo usando, para cada componente, su predeterminado explícito o el de su tipo efectivo. Falta definir la función concreta para:

- Aliases no estructurales y colecciones con restricciones.
- Intervalos, selección del miembro predeterminado de una familia cerrada y refinamientos.
- Tipos cuyo dominio pueda depender del mundo activo.

Los componentes de un alias estructural pueden reemplazar explícitamente el predeterminado que obtendrían de su tipo. Falta decidir si otras clases de tipo derivado pueden reemplazar su predeterminado intrínseco.

Desde [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]], debe definirse además cómo obtiene predeterminado una colección de `thing` con mínimo positivo. El ancla exacta nunca es candidata; puede ser necesario exigir un descendiente estricto predeterminado o un inicializador explícito.
