---
id: D-137
title: "Live locals, stored type inference and positional binding patterns"
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions: []
affects:
  - "[[specification/README]]"
  - "[[specification/06-lexicon]]"
  - "[[specification/07-concrete-grammar.md]]"
  - "[[specification/08-abstract-syntax.md]]"
  - "[[specification/09-names-and-anchors.md]]"
  - "[[specification/10-type-system.md]]"
  - "[[specification/14-fields-and-mutability.md]]"
  - "[[specification/19-expressions.md]]"
  - "[[specification/25-effects.md]]"
---

# ADR-137 — Live locals, stored type inference and positional binding patterns

## Context

Local := and derived fields need the same mental model. Capturing a computed local forever makes sequential private updates and shared preamble observations unexpectedly stale. Explicit stored inference and reusable patterns allow concise captures without name-dependent parsing or mutable destructuring.

## Decision

Stored = evaluates once at slot creation; derived := registers a live non-assignable derivation. Reads use their applicable current/temporal view, obey ordinary random-point identity and capability restrictions, and preserve a fixed static contract. Caching may not change observable values, faults or dependencies.

Action/subaction, reactive-rule and message/submessage shared preambles admit immutable stored and derived locals and positional patterns with value-body RHSs, including privately mutable ValueBlock computation. They admit no outer mut. Stored slots exist only within a concrete declaration instance. Expression/test preambles retain derived expression RHSs and admit pure derived positional patterns only.

Eligible stored annotations with their own initializer/default admit _ recursively in type positions, including mutable stored owners. Written structure, domains and collection modifiers remain normal stored admission constraints. Every hole must resolve uniquely and completely before execution; unknown, contradictory or ambiguous evidence is a compilation error marked at the hole. No nominal alias enumeration, arbitrary literal promotion, runtime type generation, Any fallback or union of guessed solutions is permitted. General type expressions/signatures and derived annotations do not admit holes.

Binding patterns recursively capture names, discard _ or open positional products. Local pattern declarations require a positional root and are immutable; standalone _ =/_ := and mut destructuring are invalid. Stored patterns evaluate once and introduce captures atomically; derived patterns are live projections. Named products cannot be opened. Iteration, selection and all quantifiers reuse the same pattern model; exact-dictionary pairs retain association semantics. Semantic for/on/given roles keep mandatory names. Discards introduce no LocalSymbol; named leaves retain ordinary lexical rules.

Tooling may suggest unused-name discard or removing a completely discarded pattern only when observable obligations and meaning are preserved. All tooling diagnostics are in English.

## Integration and provenance

Amends [[notes/decisions/ADR-023-consolidation-of-concurrent-structural-effects]], [[notes/decisions/ADR-066-static-values-and-local-bindings-in-then]], [[notes/decisions/ADR-071-local-bindings-in-boolean-blocks]], [[notes/decisions/ADR-096-modules-callables-look-message-and-activation]], [[notes/decisions/ADR-101-value-blocks-stored-local-variables-and-witness-extrema]], [[notes/decisions/ADR-109-foreign-language-blocks-and-value-exports]], [[notes/decisions/ADR-042-shares-root-and-results]], [[notes/decisions/ADR-047-quantifiers-and-finite-iteration]], [[notes/decisions/ADR-081-collection-filtering-take-and-indexing]], [[notes/decisions/ADR-088-iteration-signed-progressions-and-expression-blocks]]. The author's follow-up closes partial inference and mutable-hole choices, rejects standalone discard declarations, preserves expression-block purity and includes submessage preambles. Also amends [[ADR-119-invocation-owned-completion-and-imagine]] to retain real-action capture in stored initializers and prohibit it in live pure derivations. Compiler representation is designed within these accepted constraints.

## Alternatives

Freezing := locals would disagree with derived fields. Bare x = value as an implicit declaration hides misspellings and makes parsing depend on resolution. Mutable and named-product destructuring are not admitted. Restricting _ to a whole annotation would unnecessarily exclude statically unique component inference.

## Verification

Grammar/CST/AST inventories, nominal pattern scopes, static inference and sequential/temporal observation cases are reviewed together. Mechanical checks are specification validators and bounded witnesses, not an implemented MUD compiler.
