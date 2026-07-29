---
id: D-011
title: "Los derivados no añaden comportamiento de dominio"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-009"
  - "Q-037"
  - "Q-038"
affects:
  - "arquitectura de AST, IR, grafo, materializadores y editor"
---

# ADR-011 — Los derivados no añaden comportamiento de dominio

## Contexto

Un generador, un IR o un plugin pueden convertirse accidentalmente en una
segunda fuente de reglas si completan silencios de `.mud` o introducen
validaciones y efectos propios.

## Decisión

Los derivados interpretan, conservan, consultan o materializan la semántica de
la fuente, pero no añaden comportamiento de dominio. Toda distinción necesaria
para una ejecución conforme debe proceder de la fuente y de la especificación.

## Consecuencias

D-051 define el contrato reconstruible de AST, grafo e IR. D-052 define la
frontera del pipeline, materializadores, editor y conformidad.
