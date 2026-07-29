---
id: D-010
title: "Finitud y terminación exigidas por `eventually`"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-026"
  - "Q-027"
  - "Q-028"
  - "Q-029"
  - "Q-030"
  - "Q-031"
affects:
  - "capítulos de alcanzabilidad, finitud y terminación"
---

# ADR-010 — Finitud y terminación exigidas por `eventually`

## Contexto

Una búsqueda de alcanzabilidad sin un espacio enumerable y transiciones
terminantes puede no responder o depender de un límite técnico presentado
erróneamente como significado del lenguaje.

## Decisión

`eventually` solo es admisible cuando el análisis puede justificar un espacio
de búsqueda finito y enumerable y la terminación de cada transición explorada.
Un presupuesto técnico puede limitar recursos, pero no redefine la verdad de la
proposición.

## Consecuencias

D-044 desarrolla la alcanzabilidad existencial y su admisibilidad conservadora.
