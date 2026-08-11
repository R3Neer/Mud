---
id: Q-045
title: Contenido declarativo de create
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-07-28
decisions:
  - D-054
affects: []
superseded-by: []
---

# Q-045 — Contenido declarativo de `create`

## Contenido

Estado: **cerrada**.

¿Dónde se define el contenido declarativo de una identidad activada mediante `create`?

Decisión vigente: [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

```mud
abstract thing B as A {
    # Única definición canónica.
}

create B
```

`create` no admite bloque, categoría, antecesoras ni contenido declarativo. La definición canónica contiene todas las propiedades, restricciones, predeterminados y antecesoras. La activación solo las incorpora a la proyección efectiva.
