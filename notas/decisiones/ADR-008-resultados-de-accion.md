---
id: D-008
title: "Results `accepted`, `rejected` y `failed`"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-007"
affects:
  - "capítulos de acciones, resultados y diagnósticos"
---

# ADR-008 — Results `accepted`, `rejected` y `failed`

## Context

One request unacceptable and a failure from resolution do not express the same thing
situation. Confusing the two makes it difficult to distinguish a normal refusal from the domain of a
a problem that prevents the attempted execution from taking place.

## Decisión

One action produces exclusively:

- `accepted`, when he confirms his transition;
- `rejected`, when the request is not permitted without constituting a technical failure
  or semantic aspect of the resolution;
- `failed`, when the resolution cannot produce a state verifiable.

Rejected results do not publish partial changes.

## Consequences

D-042 defines the complete protocol for the actions. D-061 requires a reason
`Text` for everything result Not accepted.

