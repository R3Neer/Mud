---
id: D-011
title: "Derivatives do not add behaviour of domain"
status: current
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

# ADR-011 — Derivatives do not add behaviour of domain

## Context

A generator, an IR or a plugin may accidentally become a
second source of rules if they fill in gaps in `.mud` or enter
validations and their own effects.

## Decisión

Derivatives interpret, preserve, consult or give concrete form to the semantics from
the source, but they do not include behaviour of domain. Any necessary distinction
For the code to run correctly, it must come from the source and from the specification.

## Consequences

D-051 defines the contract AST’s rebuildable, graph and IR. D-052 defines the
pipeline boundary, materialisers, editor and conformance.

