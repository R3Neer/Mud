---
id: D-003
title: "MUD es un lenguaje declarativo formal"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "especificacion/01-alcance-y-conformidad.md"
  - "interacción del operador semántico"
---

# ADR-003 — MUD es un lenguaje declarativo formal

## Contexto

La interacción principal puede comenzar en lenguaje natural, pero usar esa
conversación como representación persistente introduciría ambigüedad y
significado invisible.

## Decisión

MUD es un lenguaje declarativo formal, no un lenguaje natural controlado. La
persona o una herramienta pueden expresar una intención en lenguaje natural,
pero el resultado duradero debe convertirse en operaciones comprobables y en
fuente `.mud` conforme.

## Consecuencias

- El lenguaje natural es una interfaz de autoría, no la fuente del mundo.
- El operador no puede inventar silenciosamente reglas ausentes.
- D-053 define el flujo de interpretación, impacto, validación y commit.
