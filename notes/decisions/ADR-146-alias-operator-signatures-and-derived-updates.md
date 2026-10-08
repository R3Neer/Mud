---
id: D-146
title: Alias operator signatures and derived updates
status: current
date: 2026-10-08
supersedes: []
superseded-by: []
questions:
  - Q-075
affects:
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/10-names-and-anchors.md
  - specification/11-type-system.md
  - specification/15-fields-and-mutability.md
  - specification/21-expressions.md
  - specification/28-effects.md
  - specification/grammar/
  - specification/syntax/
  - specification/names/
  - specification/types/
---

# ADR-146 — Alias operator signatures and derived updates

## Context

The author accepts alias-owned operators with explicit public signatures, no proof-generated inverse signatures and derived updates. This extends the existing operator, alias, construction and write-back contracts without selecting unresolved lookup/inheritance/descriptor rules.

## Decision

Declarations use `a * (factor: Num): Vector2 := value-body`. Bare operands have the enclosing applied alias type; explicit operands use `(name: type)`. At least one operand has the owner alias type, explicitly or by omission. Unary + and - and binary +, -, *, /, %, |, &, ^, -- are the closed overloadable set. Keep existing precedence/grouping. Logical, comparison, type/membership, conversion, contextual and assignment operations cannot be directly overloaded. Equality and ordering retain their existing representation/nominal contracts.

A declaration introduces only its written ordered signature. The inverse is explicitly declared and can delegate: `(factor: Num) * b: Vector2 := b * factor`. Same-type signatures already admit exchanged values without guaranteeing equal results. No algebraic metadata is special; no proof creates signatures or resolves ambiguity. Valid optimizations preserve ordinary result/error/observation contracts.

An explicit result contract prevails. Without one, a returned untyped tuple first attempts contextual construction of the owner alias. If it does not fit, consider distinct operand types that fit the complete component/cardinality/domain contract: one wins, multiple require an explicit type. With none, use ordinary structural inference. Already typed results retain their identity. No Self keyword or extra short-body form is introduced.

Existing +=, -=, *=, /=, |=, &=, ^=, --= derive from an admitted binary signature with the destination on the left and a storable result. Locate/evaluate the destination once and evaluate the operand once; a failed calculation writes no result. Incorporated operators preserve their established effect algebra. A user-overloaded update computes an absolute replacement, not a numeric/set contribution; concurrent replacements use existing agreement/conflict rules. %= is not introduced. Reconstructible alias paths preserve their ordinary write-back and authority rules.

Candidate discovery, inheritance/duplicate precedence and public operator identity/descriptor/metadata remain Q-075. No current decision automatically selects these policies.

## Alternatives and consequences

Reject automatically generated inverses, proof-dependent public admission, comparison overloads and inferred concurrent algebra. Explicit inverse delegation avoids duplicated calculations. Tuple contextual preference is local to operator result inference, not general nominal conversion.

## Verification

MUD-TYPE-028/029, grammar/CST/AST models, declared acceptance/rejection cases and reviewed result-priority cases cover the accepted contracts. Q-075 delimits the remaining selection/identity work. No chapter is promoted.
