---
id: D-145
title: Nested collection suffixes and empty shape
status: current
date: 2026-10-08
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/11-type-system.md
  - specification/21-expressions.md
  - specification/grammar/
  - specification/syntax/
  - specification/types/
---

# ADR-145 — Nested collection suffixes and empty shape

## Context

The author accepts repeated direct collection suffixes and ultimately rejects collapsing singleton-empty containers. This records the final choice; earlier conversational normalization proposals are not accepted semantics.

## Decision

Int [3] [2] means (Int [3]) [2]: apply suffixes left to right, inner to outer. Each layer retains cardinality, order, uniqueness and capability. Parentheses remain available; any number of layers is syntactically admitted. Variable inner sizes do not guarantee rectangularity. Generic argument, dictionary and domain boundaries remain unchanged.

Empty and [] denote zero outer members. [empty] equals [[]], contains one empty collection member and differs from empty. Preserve all layers, including [x] when x is empty. No flattening or singleton-empty normalization applies. Bare-star effective-limit and contextual admission rules remain unchanged.

Surface AST preserves layers through NestedCollectionType wrapping TypeExpr. Nominal HIR retains references without shape/type conclusions.

## Alternatives and consequences

Reject outer-first suffix application and empty-collapse equality. Zero-row and one-empty-row matrices remain distinguishable.

## Verification

MUD-TYPE-027, repeated/grouped token fixtures and matrix/empty cases cover independent layers. No chapter is promoted.
