---
id: D-185
title: Functional operator fields and global signature coherence
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

# ADR-185 — Functional operator fields and global signature coherence

## Decision

The author accepts alias operators implemented as pure functional fields,
with bare symbol names and --> signatures. At least one operand is the owner
alias, in either position. Explicit named/curried inputs obey ordinary functional
rules. Operator fields are type-owned capabilities, not additional instance
payload components. The existing operand-header syntax is retained as sugar for
that same definition; canonical new examples use the symbol-named form.

Operator references such as (+) are functional families; a declaration descriptor
remains a noncallable descriptor. Symbol projection from a type/value yields its
unbound accessible family, not implicit receiver partial application. Supported
symbols remain the closed existing alias-overloadable set; composition is builtin.

Across the complete linked program, the same symbol/arity/ordered full operand
contracts cannot have distinct explicit definitions, even under different owners.
Names/results do not distinguish signatures. An explicit definition supersedes
an implicit compiler-origin definition of exactly that signature. Repeated
identical semantic origins deduplicate; incompatible implicit generations collide.
Inheritance diamonds retain one origin. Distinct signatures still use ordinary
specificity and ambiguity rules. Do not synthesize inverse signatures or infer
commutativity from symbols/metadata. Runtime overload dispatch is not introduced.

Partially amends D-146/D-149/D-153/D-156. Existing anchors retain their original
owner and complete operand contract encoding; global coherence does not rename
them. Static integration does not specify the causal algorithm.

## Verification

Integrate current normative surfaces, nominal HIR/Surface AST contracts and
bounded positive/negative corpus witnesses. Repository checks do not implement
a compiler/runtime or certify unresolved host/causal protocols.
