---
id: Q-052
title: Entrega de message
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-08-28
decisions:
  - D-027
  - D-096
affects: []
superseded-by: []
---

# Q-052 — Entrega de `message`

Estado: **resuelta** mediante [[notas/decisiones/ADR-096-modulos-callables-look-message-y-activacion|D-096]].

D-096 fija la multiplicidad por ocurrencias causales, la ausencia de deduplicación por payload, el orden causal por ondas, la evaluación causal de `when`/`if`, la propagación a la onda siguiente y la cancelación de entrega exterior cuando la resolución revierte. MUD y el host observan la misma identidad de ocurrencia, con proyección causal interna y proyección final exterior.

El único borde material no resuelto de la antigua pregunta se separa en Q-067: qué proyección exterior corresponde cuando un participante deja de existir antes del estado final.

## Criterio de cierre

- C1: fijar multiplicidad, deduplicación y orden causal de ocurrencias.
- C2: fijar el momento de evaluación de `when`, `if` y payload.
- C3: fijar el comportamiento exterior ante commit y rollback.

## Evidencia de cierre

- C1: D-096 modela ocurrencias causales con identidad propia, conserva multiplicidad y las propaga por ondas sin deduplicación por payload.
- C2: D-096 evalúa `when` e `if` en la vista causal y distingue proyección causal interna de proyección final exterior.
- C3: D-096 entrega al host solo después de commit y cancela toda entrega exterior si la resolución revierte; el borde de participantes inexistentes se separa en Q-067.
