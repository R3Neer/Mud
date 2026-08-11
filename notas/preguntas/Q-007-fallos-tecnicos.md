---
id: Q-007
title: Fallos técnicos
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-042
  - D-043
  - D-048
  - D-061
affects: []
superseded-by: []
---

# Q-007 — Fallos técnicos

## Contenido

¿Qué estructura tiene un error técnico y cómo se distingue de `failed` semántico, de un límite de recursos y de un defecto del runtime?

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-043-consulta-especulativa-allowed|D-043]], [[notas/decisiones/ADR-048-azar-reproducible-y-fallos|D-048]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].

Un fallo semántico revierte la acción y se propaga en `allowed`; no equivale a rechazo ni falsedad. Todo resultado externo distinto de `accepted` exige `reason: Text`, por lo que tanto los rechazos como los fallos normativos aportan un diagnóstico humano. Un límite de recursos o defecto interno debe distinguirse de ellos. Falta fijar la estructura y el orden canónicos al agregar varias causas, el contrato adicional de códigos y trazas para CLI, plugin y materializaciones y la tabla de errores en expresiones ordinarias.
