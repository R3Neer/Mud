---
id: D-013
title: "Complete formalisation before continuing with implementation"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "especificacion/README.md"
  - "planificación de implementación"
---

# ADR-013 — Complete formalisation before continuing with implementation

## Context

Early implementation would, by necessity, resolve any ambiguities that still
open and could turn accidental code choices into semantics from
MUD.

## Decisión

The specification The MUD 1.0 formalisation must be completed before proceeding with the
implementation of the language. Prototypes or editorial tools do not
can be used to quietly resolve regulatory issues.

The criteria for completeness and the order of the chapters are set out in
[[especificacion/README|the specification formally]].

## Consequences

- Decisions are first elevated to a revisable rule.
- Subsequent implementation is assessed by conformance under that regulation.
- Gaps identified by tooling are recorded as questions or decisions,
  not as an implicit behaviour.
