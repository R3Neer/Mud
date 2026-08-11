---
id: Q-053
title: Conversiones explícitas
status: cerrada
priority: P1
opened: false
closed: 2026-07-29
decisions:
  - D-030
  - D-032
  - D-037
  - D-042
  - D-059
  - D-061
affects: []
superseded-by: []
---

# Q-053 — Conversiones explícitas

## Contenido

Estado: **cerrada** mediante [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]], [[notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal|D-032]], [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]], [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].

`as` queda reservado para especialización. `to` convierte valores cuantitativos compatibles o cambia el tipo nominal entre representaciones estructuralmente compatibles; `in` cambia la unidad de expresión de magnitudes lineales y de punto. En un punto transforma la coordenada completa y evita su `format`; la extracción de partes usa `unidad from contenedor in punto`. Un `given` fuera de dominio produce `rejected`, mientras un estado tentativo con un campo fuera de dominio produce `failed`. La normalización de un intervalo invertido a `empty` no es por sí misma una violación.
