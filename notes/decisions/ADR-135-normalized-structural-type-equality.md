---
id: D-135
title: Normalized structural type equality
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions: []
affects:
  - "[[specification/10-type-system]]"
  - "[[specification/19-expressions]]"
  - "[[specification/06-lexicon]]"
  - "[[specification/07-concrete-grammar]]"
  - "[[specification/08-abstract-syntax]]"
---

# ADR-135 — Normalized structural type equality

## Context

The author accepted exact structural type comparison while retaining nominal value identity and the distinct explicit-conversion relation. Clarifications select normalized symbolic contracts rather than general semantic equivalence; calculated bodies are excluded when their effective contracts coincide.

## Decision

=== and !== compare Type operands and produce Bool. Compare the complete normalized effective contract after generic substitution, erasing only alias nominal identities. Thing/family identities and exact arguments remain opaque, including phantom family distinctions. Include names/order, member kind, complete types, symbolic domains, shapes, capabilities, criteria, products, dictionaries and normalized unions. Ignore metadata, presentation, documentation, defaults and calculation bodies except through their influence on an inferred effective contract. Current runtime population equality is not type-contract equality. Recursive comparison requires a finite closed labelled-bisimulation certificate. ==, is, iis and conversion compatibility remain distinct.

## Verification

Grammar and AST preserve complete type operands and dedicated nonchainable operators. Conformance includes aliases with equal schemas and different defaults/calculations, member-kind and shape differences, symbolic-domain differences, recursive graphs, opaque families/things and applied-family source anchors. Bounded witnesses validate supplied normalized graphs without claiming a MUD parser or arbitrary predicate equivalence solver.
