---
id: D-074
title: "Nominal unions and type narrowing"
status: current
date: 2026-08-03
supersedes: []
superseded-by: []
questions:
  - "Q-047"
affects:
  - "grammar, AST, type system, aliases, expressions and diagnostics"
---
# ADR-074 — Nominal unions and type narrowing

- Amended by: [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]], [[ADR-086-exact-nominal-identity-external-arrows-and-algebra-de-diccionarios|D-086]] and [[notes/decisions/ADR-084-specialisation-de-aliases-inherited-members-and-derived-views|D-084]]
- Adjusted to the phase boundary of [[ADR-093-surface-ast-nominal-hir-and-later-semantic-phase|D-093]].

## Context

MUD needs to express that a value may belong to several alternatives without losing its chosen nominal identity. The same need occurs in fields, participants, `given` values, local bindings and aliases.

## Decision

`|` forms a type union in every type position:

```mud
value: Nat | Text
alias Result := Nat | Text
```

An alternative may declare its own domain. Collection specification may appear only once, at the end, and applies to the complete union:

```mud
values: Nat in 0..10 | Int in -10..-1 [1..*]
```

Parentheses may group alternatives, but canonical form removes them when they do not change association. There are no per-alternative cardinalities.

The union is associative, commutative and idempotent with respect to identical alternatives. It does not remove a nominal alternative merely because its domain is contained in another's: `Nat | Int` retains both.

### Alternative selection

An expression is implicitly incorporated when it has one compatible alternative. If a literal or contextually constructible expression satisfies several, it is ambiguous:

```mud
value: Nat | Int = 2        # invalid
value: Nat | Int = 2 to Int # valid
```

This is especially important for distinct aliases with the same representation. A union value retains the nominal alternative through which it entered. A union of `thing` types retains the original identity and is compatible with `Thing` exactly when all its alternatives are.

`Thing` remains universal only for `thing` declarations; the existence of `|` does not include aliases, families, magnitudes or other nominal types. To combine different categories, write an explicit union.

### Operations and narrowing

Without further information, only operations with a result compatible with every possible alternative are admitted. `is` is extended to test nominal membership of an alternative, and `is not` is added as a canonical compound operator with the same precedence:

```mud
rule IsPositive given value: Nat | Text {
    value is Nat and value > 0
}
```

A true condition narrows the environment for the part whose evaluation depends on it: the right operand of `and`, the final expression of a Boolean block and the `then` governed by an action or rule's `if`. `is not A` removes alternatives or portions satisfying `A`; with overlapping types it does not necessarily select a complete alternative.

`is` observes nominal type, not mathematical inclusion of the content. A value `2 to Int` does not satisfy `is Nat` merely because it is non-negative.

### Structural aliases

A structural component may have a union type. Anonymous structural bodies may not be unioned after `}`. The forms must be named and then united:

```mud
alias Coordinate := GridCoordinate | NumericCoordinate
```

Simple alias definition retains `:=`; `:` remains value annotation.

### Defaults

A union that cannot select one unique nominal default requires an explicit initialiser in every context that must materialise a value. The textual order of alternatives never selects the default.

## Consequences

- Elaboration determines normalised nominal alternatives and the alternative selected by each incorporation; later representations must retain or reconstruct them.
- Boolean analysis needs flow-sensitive refined environments.
- D-017 must distinguish valid types from types materialisable without an initialiser.
- `|` is disambiguated by syntactic context between type unions and its value-level uses.

## Verification

1. Unions in every type position.
2. Local domains and one outer collection specification.
3. Normalisation without redundant parentheses.
4. Ambiguity of literals and aliases with the same representation.
5. Narrowing through `is` and `is not`.
6. Overlap through multiple specialisation.
7. Rejection of unioned anonymous structural bodies.

## Clarification by D-084

The union `A | B` expresses alternatives. It does not resolve multiple specialisation `alias C as A, B`: that requires every `C` value to satisfy both ancestors simultaneously and therefore requires one compatible effective representation obtained by intersection.
