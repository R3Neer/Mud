---
id: D-169
title: "Explicit value declarations, exhaustive selector shorthand and foreach comprehensions"
status: current
date: 2026-10-14
supersedes: []
superseded-by: []
questions: []
affects:
  - "[[specification/07-lexicon]]"
  - "[[specification/08-concrete-grammar]]"
  - "[[specification/09-abstract-syntax]]"
  - "[[specification/10-names-and-anchors]]"
  - "[[specification/11-type-system]]"
  - "[[specification/15-fields-and-mutability]]"
  - "[[specification/16-collections]]"
  - "[[specification/17-dictionaries]]"
  - "[[specification/21-expressions]]"
  - "[[specification/22-quantifiers-and-iteration]]"
---

# ADR-169 — Explicit value declarations, exhaustive selector shorthand and foreach comprehensions

## Context

The author accepts explicit let/mut markers to distinguish declarations from
assignment while keeping stored = captures separate from live := derivations.
Functional policies need concise selectors and exhaustive treatment; collection
transformations should not require a hand-written private accumulator.

## Decision

Ordinary immutable stored/derived value declarations require let. Mutable stored
declarations require mut. Stored annotations may be omitted or constrain inference
by type/domain/shape. Bare : _ annotations remain valid with a semantics-preserving
simplification suggestion; partial holes remain useful. Stored alias components also require let, including components without a
default, as clarified by D-170. Family stored data, parameters, metadata, type
definitions, units and overrides keep their distinct contracts.
Stored domain-only annotations constrain admission and never filter their values.

Functional selectors retain complete Bool predicates and add ordinary-value
equality, abbreviated comparisons, nominal type tests, interval/domain membership,
selector negation and logical combinations. Bool operands remain predicates;
explicit == compares Bool/interval values. value becomes an implicit ordinary
immutable input variable; .member abbreviates its member access. Exact dictionaries
do not inject it. No as input binding, structural patterns or additional guard
syntax is accepted. D-172 extends each result scope with its own direct selector-preamble bindings
and requires demand-preserving per-application reuse of unchanged derivations.
All policies require proven input coverage or a fallback;
explicit empty output handles a case and does not invoke fallback.

foreach replaces the separated traversal spelling everywhere. foreach with :
executes the existing short/braced body; foreach with --> produces one complete
body result per accepted occurrence. It is pure, finite, snapshot-based and uses
the existing optional by/if headers and positional patterns. Multiplicity/order
are retained; output uniqueness needs proof and collection results stay nested.

This partially amends D-066, D-071, D-085, D-088, D-101, D-112, D-124 and D-137.
Concrete collection-library APIs and an alternative modifier-only dictionary
annotation are not selected by this decision. Input inference still needs unique
evidence; Person --> _ [ordered] retains explicit branch-selection grouping.

## Verification

Review declaration owners, selector interpretation/coverage, source scopes,
grammar/CST/AST/HIR, examples and finite contracts together. Validators and bounded
token/semantic witnesses do not constitute a complete MUD compiler or runtime.
