---
id: D-180
title: Uniform dictionary cardinality inference
status: current
date: 2026-10-16
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/11-type-system.md
  - specification/15-fields-and-mutability.md
  - specification/16-collections.md
  - specification/17-dictionaries.md
  - specification/21-expressions.md
  - specification/syntax/cst-to-surface-ast.md
  - specification/syntax/mud-surface-ast.asdl
  - specification/syntax/cases/cst-ast.yaml
  - specification/types/README.md
  - specification/types/typing-cases.yaml
  - notes/examples/duelo-spellcasting
---

# ADR-180 — Uniform dictionary cardinality inference

## Context

The author accepts reuse of ordinary omitted-cardinality rules for exact and
functional dictionaries. A dictionary is one exterior value; its arrow-owned
specification counts associations or application results instead. Those counts
must not be confused. Omission must not silently demand one association or a
total policy when an immutable definition supplies inference evidence.

## Decision

Written cardinalities remain contracts. Without one, an immutable stored exact
dictionary infers its association bounds from its initializer; a literal with
two distinct keys infers [2], and a contextually typed empty map infers [0].
A mutable stored exact dictionary instead defaults to [1]. A derived dictionary
retains expression-inferred bounds. Type-only positions, including signature
slots and alias representations, default to [1] when no defining-value
inference applies. A receiving contract is not widened from a caller's value.

An immutable functional definition with omitted application cardinality infers
bounds from its complete body, branch-selection mode and admitted input/view
contracts. An uncovered case contributes zero. Ordered selection remains
FirstMatch; an unannotated partial FirstMatch can therefore infer [0..1]. An
AllMatches body can infer several results. Positive written or expected minima
require proved coverage and enough admitted results; omission does not create
an implicit exhaustivity requirement. Type-only functional contracts default
to [1]. No body or input type is invented to solve missing evidence.

Inference uses the normative supported proofs and conservative bounds; it is
not a count of the current call or first world view. Static literal counts are
exact when proved; other expressions retain sound intervals. Calculated
policies can change results across reads without changing their fixed static
contract. Written modifiers without a cardinality preserve omission; they do
not create a [1] requirement. No constructor, arrow grouping, inner value
shape, mutation permission, evaluation demand or dictionary query rule changes.
Functional dictionaries remain nonmutable.

Schema defaults are initial values, not a reason to omit a contract that must
admit other supplied values or inherited defaults. Use explicit bounds there.
The author also requests removal of redundant cardinalities in internal example
calculations; public/domain bounds and required stored mutable bounds remain.

Partially amends [[ADR-019-mutability-orthogonal-to-collection-and-members|D-019]],
[[ADR-039-collections-and-dictionaries|D-039]],
[[ADR-080-higher-order-collection-algebra-and-updates|D-080]],
[[ADR-085-functional-dictionaries-metadata-and-structured-activation|D-085]],
[[ADR-086-exact-nominal-identity-external-arrows-and-dictionary-algebra|D-086]]
and [[ADR-169-explicit-values-selectors-and-foreach-comprehensions|D-169]].

## Alternatives and consequences

A universal [*] exact default was rejected in favour of the ordinary owner
matrix. Implicit totality for functional definitions was rejected in favour of
body inference: authors write a positive bound to preserve that guarantee.
Removing a branch may widen inferred absence; an explicit positive contract
instead diagnoses lost coverage. Mutable maps commonly need [*], as ordinary
mutable collections do. Partial policies need no redundant [?] annotation.

## Verification

Integrate prose, AST omission/projection, declarative corpus and bounded
cardinality witnesses. Preserve the existing source-only boundary: supplied
finite certificates are not a compiler, general coverage solver or runtime.
