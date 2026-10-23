---
id: D-184
title: Structural traits and capability views
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
  - specification/13-aliases.md
  - specification/17-dictionaries.md
  - specification/21-expressions.md
  - specification/types/
  - specification/grammar/
  - specification/syntax/
  - specification/names/
  - notes/examples/duelo-spellcasting
---

# ADR-184 — Structural traits and capability views

## Decision

The author accepts trait declarations as structural minimum requirements,
separate from nominal aliases and thing identity. Traits can type values and
heterogeneous collections and bound ordinary static generics. Stored, calculated
and inherited accessible fields can supply read capabilities; extra fields are
allowed. Typed mutability requirements require existing authority and invariant
stored writable contracts. Private schema cannot be laundered through a view.

Omitted domain/order/uniqueness/authority does not add a guarantee beyond the
written type/ordinary cardinality. Bare ordered requires an observable sequence;
by criteria retain existing inclusion rules. An operator field has its bare
symbol name. A bare + requirement asks for some admitted accessible capability,
not T+T->T; typed signatures can require particular relations.

is Trait checks proven structural satisfaction and may discriminate a finite
known set of nominal alternatives. iis Trait is invalid. Trait === compares
normalized requirement contracts, ignoring declaration names/order but retaining
all requirements. Satisfaction adds no nominal inheritance. TypeKind.Trait and
DeclarationKind.Trait are fixed catalogue additions, not user-extensible kinds.

No extra intersection/exclusion type language or union construction over Type
values is introduced; those ideas are discarded. Ordinary | remains available.
Partially amends D-074/D-135/D-157/D-178. Canonical rules are in
specification/types/structural-traits.md.

## Verification

Integrate current normative surfaces, nominal HIR/Surface AST contracts and
bounded positive/negative corpus witnesses. Repository checks do not implement
a compiler/runtime or certify unresolved host/causal protocols.
