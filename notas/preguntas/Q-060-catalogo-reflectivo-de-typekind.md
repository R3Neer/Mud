---
id: Q-060
title: Catálogo reflectivo de TypeKind
priority: P1
opened: 2026-08-16
resolved: false
closed:
decisions:
  - D-087
affects:
  - especificacion/08-sintaxis-abstracta.md
superseded-by: []
---

# Q-060 — Catálogo reflectivo de `TypeKind`

## Pregunta

¿Qué miembros públicos contiene `TypeKind`, qué estabilidad garantiza MUD a ese catálogo reflectivo y cómo se relaciona con las formas internas normalizadas del sistema de tipos?

## Contexto

D-087 hace observable `Type~kind`, pero deja deliberadamente el catálogo concreto de `TypeKind` para la especificación del sistema de tipos. Sin una pregunta activa, esa parte de la API reflectiva puede cerrarse accidentalmente al formalizar tipos internos.

## Ya decidido

- Todo valor expone `~type: Type`.
- `Type` expone `~kind`.
- El catálogo de `TypeKind` es parte de la API reflectiva y no debe confundirse automáticamente con constructores internos del compilador.

## Pendiente

- C1: enumerar las categorías públicas mínimas de MUD 1.0.
- C2: decidir qué cambios del catálogo son compatibles entre versiones.
- C3: definir la relación entre una categoría pública y las formas internas normalizadas que pueda usar el compilador.

## Criterio de cierre

- C1: existe un catálogo normativo completo para MUD 1.0.
- C2: la especificación declara su estabilidad observable.
- C3: cada forma interna relevante puede proyectarse de manera determinista a un miembro público de `TypeKind` sin exponer accidentalmente detalles de implementación.

## Resolución

Pendiente.
