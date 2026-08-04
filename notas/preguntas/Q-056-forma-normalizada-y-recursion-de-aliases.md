---
id: Q-056
title: Forma normalizada y recursión de aliases
status: parcialmente-decidida
priority: P2
opened:
closed:
decisions:
  - D-084
affects: []
superseded-by: []
---

# Q-056 — Forma normalizada y recursión de aliases

## Decidido por D-084

- Especialización simple y múltiple de aliases.
- Intersección de representaciones nominales y dominios compatibles.
- Herencia de componentes y campos derivados.
- Deduplicación de diamantes por origen y conflictos entre nombres independientes.
- Sobrescritura exclusiva de predeterminados almacenados.
- Construcción contextual y acceso nominal a miembros.

## Pendiente

Definición inductiva completa de la forma estructural normalizada cuando existen aliases anidados o recursivos; admisión o rechazo de recursión directa e indirecta; condiciones de productividad; decidibilidad de compatibilidad, predeterminados y enumeración canónica de cada tipo componente.

## Criterio de cierre

Q-056 podrá cerrarse cuando la especificación defina una normalización canónica para aliases anidados, resuelva la recursión y establezca condiciones decidibles de compatibilidad, productividad, predeterminados y enumeración.
