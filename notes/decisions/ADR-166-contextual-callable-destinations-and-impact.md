---
id: D-166
title: Contextual callable destinations and impact
status: current
date: 2026-10-14
supersedes: []
superseded-by: []
questions:
  - Q-023
affects:
  - specification/types/contextual-call-analysis.md
  - specification/10-names-and-anchors.md
  - specification/11-type-system.md
  - specification/15-fields-and-mutability.md
  - specification/18-domains-and-intervals.md
  - specification/21-expressions.md
  - specification/23-boolean-rules.md
  - specification/24-reactive-rules.md
  - specification/25-always-rules.md
  - specification/26-public-boundary.md
  - specification/28-effects.md
---

# ADR-166 — Contextual callable destinations and impact

## Accepted choices

The author accepts finite contexts distinguished by demonstrated nominal callable
input destinations, rather than one node merging every invocation of a declaration.
When only a signature is known, use the conservative compatible legally obtainable
catalogue; a manually closed source list is not mandatory. Every possible target
must satisfy the required acyclicity, authority, dependency and effect proofs.

Contexts do not specialize arbitrary runtime numeric data or world states. Known
Dispatch(A)/Dispatch(B) calls can remain separate. Open inputs may enlarge the
graph; narrowing can remove only proved impossible destinations. No trial execution,
reflection scan, metadata permission or new source syntax is introduced.

## Formalization and evidence

MUD-TYPE-043 and the contextual procedure specify the finite destination lattice,
transfers, exact no-growth completion, contextual SCC obligations, place substitution
and complete conservative summary joins. D-042's literal body is reconciled.
Q-023 closes with supplied finite graph/summary certificates and contrasting cases.
Pure recursion remains subject to its independent termination certificate; causal
cycles, foreign protocols and runtime completion are not closed by this graph.
