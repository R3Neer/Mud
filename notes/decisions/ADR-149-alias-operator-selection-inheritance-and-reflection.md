---
id: D-149
title: Alias operator selection, inheritance and reflection
status: current
date: 2026-10-08
supersedes: []
superseded-by: []
questions:
  - Q-075
affects:
  - specification/10-names-and-anchors.md
  - specification/11-type-system.md
  - specification/21-expressions.md
  - specification/names/mud-nominal-hir.asdl
  - specification/types
---

# ADR-149 — Alias operator selection, inheritance and reflection

## Decision

Discover visible declarations from both operand aliases and their admissible ancestors. Deduplicate the same originating declaration, including diamonds; distinct declarations remain distinct even with equal bodies. Duplicate normalized ordered operand signatures inside one declaring alias are declaration errors, independent of use, result and argument names.

For each effective static operand alternative, retain applicable complete signatures under ordinary compatibility and contextual literal rules. Do not unwrap aliases, erase dimensions or search conversions. Numeric representation widening and builtin dimension-preserving magnitude arithmetic retain their existing contracts. Magnitude representations remain Nat, Int, Num, Rum or Money; arbitrary payload magnitudes and generalized dimensional vectors are not introduced.

Select the unique signature whose operand contracts are included in every other applicable signature, with at least one strict inclusion against each distinct competitor. Expected results do not select a signature. Equal or incomparable distinct signatures are ambiguous, without left-owner, import-order, runtime-subtype or body preference. Inheritance retains original owner, signature, body and result; it does not rebind an operation to a descendant or synthesize its extra components.

Check every pair of remaining static union alternatives after flow narrowing. Each pair must select uniquely; result contracts join normally. Runtime identification of an already checked union alternative is not new runtime overload discovery.

Resolve explicit signatures on complete operands first, then an applicable builtin contract, then permitted arithmetic lifting. An ambiguous explicit match is an error, not a reason to fall back. Execution failure or destination/result failure does not retry a different operation. Custom +, -, *, / and % lift under existing collection limits: at least one static upper cardinality is at most one; every possible member pair is admitted. No implicit zip, reduction or unrestricted Cartesian product is introduced. A direct collection-argument overload takes priority over member lifting. Set-algebra symbols retain their outer collection contracts without new automatic member lifting.

## Public identity and reflection

An operator's identity includes its original alias owner, symbol, arity and ordered normalized operand contracts, preserving nominal identities. Parameter names, result and body do not distinguish signatures. The accepted simple anchor shape is `alias::path.Vector2::operator::*(path.Vector2, Num)`. Inherited declarations retain it. Canonical serialization of complex contracts, generic binders and escaping remains Q-075; this shape is not a complete wire grammar.

Alias~operators exposes own and inherited operator declaration descriptors, unique by origin. Alias~declaredOperators exposes only own declarations. General signatures remain in the catalogue even if more specific ones exist. Descriptor queries cover owner, anchor, symbol, operands, result and metadata under ordinary visibility. TypeKind is DeclarationDescriptor unless a more specific established category applies; no OperatorCallable type or first-class operator invocation is introduced. User metadata has no algebraic or overload-selection privileges.

Nominal resolution retains source ownership, operand scopes and type-reference provenance. Signature-dependent selection and anchors are computed after typing and are not fabricated as nominal HIR fields. The public descriptor/metadata spelling and full encoding require their remaining Q-075 contract before publication.

## Verification and provenance

Extends [[ADR-146-alias-operator-signatures-and-derived-updates|D-146]]. Chapter 21 supplies applicability, specificity, alternative coverage and fallback rules; chapter 10 supplies public identity boundaries. Finite supplied-candidate witnesses distinguish dominance, crossed ambiguity, origin deduplication, union narrowing and whole-operand priority. They do not implement Mud parsing, lookup, compilation or execution. Q-075 remains partial for the exact encoding/reflective schema.
