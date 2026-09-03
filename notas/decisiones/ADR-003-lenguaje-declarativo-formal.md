---
id: D-003
title: "MUD is a formal declarative language"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "especificacion/01-alcance-y-conformidad.md"
  - "interacción del operador semántico"
---

# ADR-003 — MUD is a formal declarative language

## Context

The main interaction may begin in natural language, but using that
Treating conversation as a persistent representation would introduce ambiguity and
hidden meaning.

## Decisión

MUD is a formal declarative language, not a controlled natural language. The
a person or a tool can express an intention in natural language,
but the result Sustainability must translate into verifiable actions and into
source `.mud` Agreed.

## Consequences

- Natural language is an authoring interface, not the source of the world.
- The operator cannot quietly make up rules that do not exist.
- D-053 defines the process of interpretation, impact, validation and commit.

