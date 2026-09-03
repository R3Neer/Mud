---
id: D-009
title: "`allowed` as a baseless rumour"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-007"
  - "Q-035"
affects:
  - "admissibility and speculative query chapter"
---

# ADR-009 — `allowed` as a baseless rumour

## Context

Check only the preconditions for a action may declare a
request whose resolution 'complete' would end in conflict, invariant
unfulfilled or failure.

## Decision

`allowed` executes the protocol of the action on a copy
disposable. Not confirmed state nor does it publish outputs. Errors are not converted
as falsehoods: they are spread as errors of the query.

## Consequences

D-043 develops the semantics in full, together with his comments.

