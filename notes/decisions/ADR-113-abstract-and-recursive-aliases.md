---
id: D-113
title: Abstract and recursive aliases
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - Q-056
affects:
  - Language contracts and their developed normative surfaces
---

# ADR-113 — Abstract and recursive aliases

- Formalised by: [[ADR-122-finite-type-graphs-and-proof-obligations|D-122]].

## Context

Abstract Error and Refusal values need extensible immutable records and productive recursive cause/trace components. This amends D-031, D-032 and D-084; it does not permit a cycle in nominal specialisation.

## Decision

`abstract alias Name { ... }` and `abstract alias Name as Base` declare nominal abstract aliases. Abstract aliases can type values and be ancestors but cannot be constructed or cast into as a new exact value. Concrete specialisations provide the exact nominal identity. An abstract modifier does not introduce world identity, lifecycle or mutable storage. The modifier is admissible only for structural aliases or descendants with a structural effective representation.

Representation recursion may be direct or indirect through stored components, collections and dictionaries. Every actual alias value is a finite immutable tree; it has no cyclic reference identity. A recursive reference in a type is not an instruction to unfold that type infinitely. Unguarded representation-alias cycles such as A := B, B := A are invalid. Nominal ancestor cycles remain invalid.

Normalisation builds a finite graph keyed by resolved nominal type and normalized constructor/domain/collection specification. Named recursion is represented by graph references. Effective inherited members are collected by declaration origin, refinements are intersected under existing substitutability rules, and competing independent definitions are resolved as required by D-084. Transparent representation edges must reach a productive constructor; they cannot constitute their own value.

For unrestricted structural constructors, productivity is the least fixed point starting from known inhabited nonrecursive leaves. A product is productive when all required components are; a union when at least one alternative is; a collection/dictionary admitting zero occurrences can terminate at empty, while positive minimum requires productive elements/keys/values. An abstract alias is inhabited through productive concrete descendants, not by directly instantiating the base. Any explicit default must itself be a finite valid value. Reject a strongly connected mandatory component cycle with no productive exit.

Compatibility of normalized finite type graphs uses memoized pairs, nominal ancestry and the declared representation/domain/capability rules; encountering a recursive pair is not itself a proof of compatibility or productivity. Domain-dependent obligations require their ordinary proof or explicit restriction rather than an invented type default. A finite representation for each value does not imply a finite value space: canonical enumeration requires a proof of a finite, effectively enumerable domain. Recursive unbounded trees are not enumerable merely because each individual tree is finite.

## Examples

```mud
abstract alias Problem { reason: Text; cause: Problem [0..1] = empty }
alias Missing as Problem { key: Text }
alias Tree { children: Tree [*] = empty }
alias Impossible { next: Impossible } # invalid: no finite value
alias A := B
alias B := A # invalid: transparent cycle
```

## Integration review

Grammar and Surface AST retain the abstract flag; the CST transformation records it without deciding productivity. Lexicon includes abstract before alias. The nominal HIR's existing alias symbols and Specializes/RefersTo edges suffice: recursive representation edges are type elaboration data, not new nominal ancestry. Chapter 10 develops the static contract; the complete alias declaration chapter remains to be developed.

## Verification

Check concrete construction through abstract ancestors, direct and mutual productive recursion, rejection of mandatory/transparent cycles, finite normalization and the distinction between finite values and finite enumeration.
