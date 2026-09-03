---
id: D-102
title: "Complete form of computed family data"
status: current
date: 2026-08-29
supersedes: []
superseded-by: []
questions:
  - "Q-061"
affects:
  - "family, computed data, derived form, grammar, CST and superficial AST"
---
# ADR-102 — Complete form of computed family data

- Resolves: [[notes/questions/Q-061-f-declarable-form-of-computed-family-data|Q-061]].
- Modifies: [[ADR-038-close-knit-families-with-strong-values|D-038]] and [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]].
- Applies the derived form from [[ADR-037-fields-and-declarative-domains|D-037]] to computed `family` data.

## Context

Computed `family` data was already represented in EBNF and the AST with `derived-value-shape`, while D-038 retained a narrower exception that only intended to admit an optional type and excluded domain and collection form. Q-061 isolated that divergence.

## Decision

Computed `family` data uses the same complete declarable form as a computed field:

```text
nombre [forma-derivada] := value-body
```

`derived-form` is the ordinary `derived-value-shape`: it may fix a `type-expression`, declare a domain with an optional collection form, or declare a collection form directly. If it does not fix a type, the type must be inferred uniquely.

Computed data remains immutable, has no storage of its own, does not admit outer `mut`, has no stored default, and cannot be the target of a member assignment. The derived form describes and, where appropriate, coerces the produced value; it does not turn the data into a writable slot.

Explicit type, domain, cardinality, `unique` and order reuse exactly the general semantics of D-037's computed fields. A derived form cannot manufacture inner `[mut]` capability or any other authority absent from the source value.

The RHS admits the short expression or the `ValueBlock` already defined for computed `family` data; this decision does not modify its purity contract or its static per-member evaluation.

## Ejemplos

```mud
family Tier {
    score: Nat := baseScore
    normalized in 0..100 := rawScore
    tags: Text [* unique ordered] := inheritedTags

    Low,
    High
}
```

All three declarations are computed and immutable. The written forms constrain or normalise the result according to the ordinary `derived-value-shape` contract.

## Rejected alternatives

### Limit computed `family` data to `[: type]`

Rejected. It would introduce an exception without a mutability or storage difference to justify it and lose the declarative coercions available in other computed fields.

## Consequences

- Q-061 is closed.
- The current EBNF needs no change: it already uses `[ derived-value-shape ]`.
- `CalculatedFamilyDataDecl` definitively retains `derived_value_shape? shape`; it is no longer a provisional representation.
- The grammar, CST and AST for `family` are aligned with the general computed-field form.

## Verification

1. Computed `family` data accepts an explicit type, domain or collection form through `derived-value-shape`.
2. The form continues to reject outer `mut` and creates no storage.
3. The EBNF and `CalculatedFamilyDataDecl` retain the complete derived form.
4. Q-061 disappears from normative surfaces as an active question.
