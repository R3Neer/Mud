---
id: Q-001
title: Gramática y saltos de línea
status: cerrada
priority: P0
opened: false
closed: 2026-07-28
decisions:
  - D-050
  - D-056
  - D-057
affects: []
superseded-by: []
---

# Q-001 — Gramática y saltos de línea

## Contenido

Estado: **cerrada** mediante [[notas/decisiones/ADR-050-comentarios-terminadores-y-separadores-numericos|D-050]], [[notas/decisiones/ADR-056-char-texto-y-orden-unicode|D-056]] y [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|D-057]].

Una instrucción termina mediante `;` o salto de línea. El salto continúa cuando el prefijo todavía no puede formar una unidad sintáctica completa pero admite una continuación válida; la sangría no interviene.

La sintaxis completa vive en `especificacion/gramatica/`; [[especificacion/07-gramatica-concreta]] fija precedencia, prefijos abiertos y distinciones contextuales. La recuperación de errores puede variar entre implementaciones, pero nunca amplía el lenguaje aceptado.
