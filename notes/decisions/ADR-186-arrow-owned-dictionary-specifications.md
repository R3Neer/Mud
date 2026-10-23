---
id: D-186
title: Arrow-owned dictionary specifications
status: current
date: 2026-10-23
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/07-lexicon.md
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/10-names-and-anchors.md
  - specification/11-type-system.md
  - specification/17-dictionaries.md
  - specification/21-expressions.md
  - specification/grammar/
  - specification/syntax/
  - specification/types/
  - notes/examples/duelo-spellcasting
---

# ADR-186 — Arrow-owned dictionary specifications

## Context and authority correction

D-183 recorded first/all body constructors as accepted syntax although the
author's proposal left their spelling open. That attribution was incorrect.
The author rejected that spelling and accepted intrinsic bracket specifications
immediately after arrows, also resolving exact-association count ownership.
The accepted exterior-contribution aggregation remains unchanged.

## Decision

`A ->[2 ordered] B` has two associations in observable association order.
`A ->[2] B[3]` stores three Bs in each of two associations. Type-adjacent
specifications always describe their input/output value collections; grouping
a complete dictionary before a suffix forms an exterior collection of dictionaries.

`A -->[ordered unique] B[*]` selects the first matching branch and normalizes
aggregate result uniqueness. An unmarked branch definition selects all matches.
Intrinsic functional specifications accept ordered and unique/unique by, never
cardinality, mut or ordered by. Output collections can independently require
their own cardinality/order/uniqueness. No number counts source branches.

Arrows remain right-associative. Modifiers belong to their particular arrow:
`A --> B -->[ordered] C` prioritizes the B stage; `A -->[ordered] (B --> C)`
prioritizes the A stage. `(A -->[ordered] B[3])[4 ordered]` is an ordered
collection of four policies. Repeated suffixes remain nested collection layers.

There are no first/all body constructors. Ordinary branch lists, parenthesized
anonymous branch expressions and unconditional-body sugar remain available.
`first` is ordinary; `all` retains domain/enumeration syntax. Copying a checked
policy never silently changes its established behavior.

Partially amends D-085, D-086, D-169, D-172, D-180 and D-183. Correct their
effective text and existing normative/mechanical/example surfaces together.

## Validation

Check exact association counts, input/output counts, nested/mixed arrows,
exterior policy collections, keyed uniqueness, rejected functional cardinalities
and mutability, and rejected first/all constructors. Evidence remains bounded;
no source compiler, runtime scheduler or Unity implementation is introduced.
