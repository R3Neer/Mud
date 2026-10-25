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

- Amended by: [[ADR-185-functional-operator-fields-and-global-signature-coherence|D-185]].
- Amended by: [[ADR-187-order-sensitive-collection-arithmetic-and-read-only-views|D-187]].

## Decision

Discover visible declarations from both operand aliases and their admissible ancestors. Deduplicate the same originating declaration, including diamonds. Distinct explicit origins with identical symbol, arity and normalized ordered operand contracts are a linked-program error, regardless of owner, use, result, argument names or equal bodies. An explicit definition takes precedence over an implicit generation of the same signature; equivalent generations from one semantic origin deduplicate, while incompatible implicit generations are invalid.

For each effective static operand alternative, retain applicable complete signatures under ordinary compatibility and contextual literal rules. Do not unwrap aliases, erase dimensions or search conversions. Numeric representation widening and builtin dimension-preserving magnitude arithmetic retain their existing contracts. Magnitude representations remain Nat, Int, Num, Rum or Money; arbitrary payload magnitudes and generalized dimensional vectors are not introduced.

Select the unique signature whose operand contracts are included in every other applicable signature, with at least one strict inclusion against each distinct competitor. Expected results do not select a signature. Incomparable applicable signatures are ambiguous, without left-owner, import-order, runtime-subtype or body preference. Inheritance retains original owner, signature, body and result; it does not rebind an operation to a descendant or synthesize its extra components.

Check every pair of remaining static union alternatives after flow narrowing. Each pair must select uniquely; result contracts join normally. Runtime identification of an already checked union alternative is not new runtime overload discovery.

Resolve explicit signatures on complete operands first, then an applicable builtin contract, then permitted arithmetic lifting. An ambiguous explicit match is an error, not a reason to fall back. Execution failure or destination/result failure does not retry a different operation. Custom +, -, *, / and % lift with complete static member-pair coverage: two semantically ordered values pair positions, otherwise use every occurrence pair, recursively at explicit nested layers. No reduction or matrix multiplication is inferred. The retained actual order selects traversal, not a new overload. A direct collection-argument overload takes priority over member lifting. Set-algebra symbols retain their outer collection contracts without new automatic member lifting.

## Public identity and reflection

An operator's identity includes its original alias owner, symbol, arity and ordered normalized operand contracts, preserving nominal identities. Parameter names, result and body do not distinguish signatures. The accepted simple anchor shape is `alias::path.Vector2::operator::*(path.Vector2, Num)`. Inherited declarations retain it. [[ADR-153-operator-descriptors-metadata-and-textual-anchor-policy|D-153]] requires self-contained complete textual encoding; its exact grammar for complex contracts, binders and escaping is specified by D-156. This shape is not a complete wire grammar.

Alias~operators exposes own and inherited operator declaration descriptors, unique by origin. Alias~declaredOperators exposes only own declarations. General signatures remain in the catalogue even if more specific ones exist. Descriptor queries cover owner, anchor, symbol, ordered operand descriptors containing source names and effective types, result and metadata under ordinary visibility. D-153 fixes the metadata source attachment forms; operand names remain descriptive. Descriptor TypeKind is DeclarationDescriptor. Operator references are separate functional values/families and do not make declaration descriptors callable. User metadata has no algebraic or overload-selection privileges.

Nominal resolution retains source ownership, operand scopes and type-reference provenance. Signature-dependent selection and anchors are computed after typing and are not fabricated as nominal HIR fields. The full reflective property/type schema and encoding follow the complete D-156 contract; metadata attachment spelling is fixed by D-153.

## Verification and provenance

Extends [[ADR-146-alias-operator-signatures-and-derived-updates|D-146]]. Chapter 21 supplies applicability, specificity, alternative coverage and fallback rules; chapter 10 supplies public identity boundaries. Finite supplied-candidate witnesses distinguish dominance, crossed ambiguity, origin deduplication, union narrowing and whole-operand priority. They do not implement Mud parsing, lookup, compilation or execution. Q-075 is completed by D-156 and its identity/schema evidence.

Complete identity/schema specification and evidence: [[ADR-156-canonical-operator-contract-encoding-and-reflection-schema|D-156]].
