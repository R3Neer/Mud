---
id: D-173
title: Sequence order and contextual value ordering
status: current
date: 2026-10-15
supersedes: []
superseded-by: []
questions: []
affects:
  - Ordinary collection ordering, lexical classification and typed key resolution
  - Grammar, CST, AST, nominal contracts and finite ordering witnesses
---

# ADR-173 — Sequence order and contextual value ordering

- Amended by: [[ADR-174-value-extrema-and-association-sequences|D-174]].

- Amended by: [[ADR-175-historical-order-and-local-collection-properties|D-175]].

- Amended by: [[ADR-183-functional-families-currification-and-input-syntax|D-183]].

## Decision

For ordinary collections, bare ordered establishes historical occurrence order
regardless of member comparability or a prior key order. Literal history is
written order. Copying and filtering retain occurrences; comprehension results
are new occurrences in production order. Sequential additions append new
occurrences and removal preserves surviving order. Existing causal-respecting
stable provenance governs concurrent insertion ties; physical arrival is not
a language order. This changes no consolidation algorithm.

Explicit ordered by selects a stable totally ordered key. In ordered by value,
an accessible member field/component/datum named value takes precedence. When
no such member exists, the single-component spelling denotes the complete
element and requires its established total comparator. A present but invalid
field is an error, not permission to fall back. The choice must be uniform over
the remaining static alternatives; a mixed union cannot choose per occurrence.
Longer paths starting with value remain ordinary member paths.

value is reserved for functional input references. Explicit member-name exceptions retain .value and intrinsic diagnostic/schema components, but ordinary locals/arguments cannot use or shadow value. Functional scopes retain cumulative inputs and no-shadowing under D-183. Their value field is accessed as value.value or
the existing .value abbreviation. The ordering spelling preserves a neutral
key-path Surface AST; the member-versus-whole choice belongs to elaboration.

This partially amends D-039, D-064, D-100, D-169 and D-172. Their remaining rules,
including key stability, comparison of family/alias values and FirstMatch
priority, remain applicable. D-174 defines exact-dictionary association sequences
and mathematical extrema with full demand absent explicit compatible key order.
First/last remain library conveniences rather than new core quantifiers. No forced whole-element spelling in the
presence of a value field is introduced by this decision.

## Consequences

Int [* ordered] can preserve [3,1,2]. Int [* ordered by value] establishes [1,2,3].
An ordered family's member comparison does not force collections of those
members into declaration order. Char collections can preserve arbitrary
sequences; String remains a distinct basic value. Collection uniqueness remains
an independent axis.

Syntax Highlight should expose the reserved functional-input token while retaining member-name contexts. Its package release is separate from this specification change.
Highlighting may recognise contextual source positions without proving the
cross-file/generic member binding. It must not claim semantic resolution or
classify every ordinary identifier named value as a keyword.

## Verification

Review lexical catalogue, neutral syntax projection, nominal input scopes,
collection normalization/algebra and preserved-order examples together.
Finite supplied-premise witnesses distinguish sequence versus explicit sort,
stable ties, field precedence, invalid keys and mixed union interpretations.
They do not implement a compiler, runtime or causal scheduler.
