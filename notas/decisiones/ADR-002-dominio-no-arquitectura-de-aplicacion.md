---
id: D-002
title: "MUD describes domain, not application architecture"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "especificacion/01-alcance-y-conformidad.md"
  - "frontera entre lenguaje y materializadores"
---

# ADR-002 — MUD describes domain, not application architecture

## Context

MUD needs to represent rules, state and causality without going into the details of
a specific interface, database or framework in semantics from the
language.

## Decisión

The MUD describes the domain and its observable behaviour. It does not prescribe the
the overall architecture of the application that hosts it, its user interface, its
network protocol, its database or the framework used by a
materialización.

The specification it can put in place the structures needed to carry out
MUD in accordance with the rules, such as identity, atomicity, order, logical time or chance
reproducible. That technological neutrality does not imply neutrality with regard to the
model its own semantic meaning.

## Consequences

- Technical adaptors remain outside the semantics from domain.
- One materialisation you can change the technology without redefining the world.
- D-052 explores the boundary between compilers and materialisers.

