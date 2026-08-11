---
id: Q-052
title: Entrega de message
status: parcialmente-decidida
priority: P1
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-027
affects: []
superseded-by: []
---

# Q-052 — Entrega de `message`

## Contenido

Estado de la premisa: **decidida** mediante [[notas/decisiones/ADR-027-salidas-look-y-message|D-027]].

Un `message` detecta un hecho durante la resolución de una acción y evalúa sus campos públicos después de estabilizarla. Falta definir multiplicidad, deduplicación, orden, momento de evaluación de `if`, participantes destruidos y el destino de detecciones pertenecientes a acciones `rejected` o `failed`.
