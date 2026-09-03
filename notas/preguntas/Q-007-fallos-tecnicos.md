---
id: Q-007
title: Technical failures
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

# Q-007 — Technical failures

## Content

What structure does a technical error have, and how is it distinguished from semantic `failed`, a resource limit and a runtime defect?

Status: **partially decided** by [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-043-consulta-especulativa-allowed|D-043]], [[notas/decisiones/ADR-048-azar-reproducible-y-fallos|D-048]] and [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].

A semantic failure rolls back the action and propagates through `allowed`; it is neither rejection nor falsity. Every external result other than `accepted` requires `reason: Text`, so both rejections and normative failures provide a human-readable diagnostic. A resource limit or internal defect must be distinguished from these. The canonical structure and ordering when several causes are added, the additional code and trace contract for CLI, plugin and materialisations, and the error table for ordinary expressions remain to be fixed.
