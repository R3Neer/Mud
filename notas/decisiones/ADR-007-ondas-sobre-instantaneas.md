---
id: D-007
title: "Resolución causal por ondas sobre instantáneas"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-005"
  - "Q-020"
affects:
  - "capítulos de resolución causal y ondas"
---

# ADR-007 — Resolución causal por ondas sobre instantáneas

## Contexto

Evaluar reacciones mientras se muta el mismo estado introduce resultados
dependientes del orden de recorrido y permite que una regla observe una
resolución parcial.

## Decisión

Las consecuencias causales se resuelven por ondas. Cada onda evalúa sus
condiciones sobre una instantánea definida y consolida sus efectos antes de
producir la instantánea observada por la onda siguiente.

Ningún estado parcial de una onda se publica como estado estable.

## Consecuencias

D-045 desarrolla vinculaciones, memoria reactiva y cola causal. D-046 y D-060
precisan la consolidación determinista de efectos.
