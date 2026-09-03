---
id: D-010
title: "Finiteness y termination required by `eventually`"
status: current
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

# ADR-010 — Finiteness y termination required by `eventually`

## Context

A search for reachability without countable space and transitions
Certain factors may not be addressed or may depend on a technical constraint that has arisen
mistakenly taken to be the meaning of language.

## Decisión

`eventually` It is only permissible when the analysis can justify a space
finite and countable search space and the termination of each transition explored.
A technical budget may limit resources, but it does not redefine the truth of the
proposition.

## Consequences

D-044 develops the reachability existential and its admissibility conservative.

