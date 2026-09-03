---
id: D-006
title: "Purity Boolean rules and write boundary"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "capítulos de reglas, acciones y API pública"
---

# ADR-006 — Purity Boolean rules and write boundary

## Context

One query amending the world returns depending on the evaluation order
the response received. Allow external writes outside of operations
The lack of identifiable markers also makes it impossible to validate and reverse a mutation such as unit.

## Decisión

Boolean rules are pure. External modifications to the world is
They make requests via actions, which form part of their write API.

Reactive rules and `always` take part in the causal resolution in accordance with
their own contracts; they do not turn a query Boolean in an operation with
effects.

## Consequences

D-041 specifies the three types of ruler and D-042 carries out the following activities, such as
atomic causal transactions.

## Verification

The static analysis Rejects effects on Boolean rules and any boundary
an external write operation that does not invoke a action Agreed.
