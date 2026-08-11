---
id: Q-048
title: Destrucción con descendientes activos
status: cerrada
priority: P0
opened: false
closed: 2026-07-27
decisions:
  - D-021
affects: []
superseded-by: []
---

# Q-048 — Destrucción con descendientes activos

## Contenido

Estado: **cerrada**.

Decisión: [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]].

Las aristas declaradas se conservan en el almacenamiento. La proyección efectiva atraviesa antecesores inactivos y conecta cada descendiente activo con sus antecesores activos más próximos. El descendiente conserva sus propiedades propias, pierde temporalmente lo heredado desde el nodo destruido y recupera la estructura original al recrearlo.
