---
id: D-012
title: "Validation and atomic versioning of semantic changes"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-008"
  - "Q-015"
affects:
  - "gobierno/POLITICA-DE-COMMITS.md"
  - "flujo de autoría del operador semántico"
---

# ADR-012 — Validation and atomic versioning of semantic changes

## Context

A change to the source may affect several anchors and derivatives. Publish
Even just one part – confirming an invalid change or including someone else’s work – destroys the
correspondence between intention, model and history.

## Decisión

Every semantic change A valid test is prepared, analysed, applied, validated and versioned as
one unit atomic. A failure prior to confirmation, it does not publish a state
partial. The commit includes only the files relating to the change.

One query `READ` `pura` does not create a commit because it does not make any changes state.

## Consequences

D-053 improves the operator’s workflow. The policy the number of commits determines the
atomicity and the handling of previous changes to the repository.

