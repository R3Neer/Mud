---
id: D-066
title: "Static values and local bindings in `then`"
status: current
date: 2026-07-30
supersedes: []
superseded-by: []
questions: []
affects:
  - "stored and computed fields, families, defaults, actions, tests, effect blocks, AST and IR"
---
# ADR-066 — Static values and local bindings in `then`

- Amended by: [[ADR-101-bloques-de-valor-variables-locales-almacenadas-and-extremos-por-testigos|D-101]].
- Extended by: [[ADR-071-local-bindings-in-boolean-blocks|D-071]]
- Amends: [[notes/decisions/ADR-023-consolidation-of-concurrent-structural-effects|D-023]], [[notes/decisions/ADR-037-fields-and-declarative-domains|D-037]], [[notes/decisions/ADR-038-close-knit-families-with-strong-values|D-038]], [[notes/decisions/ADR-042-shares-root-and-results|D-042]], [[notes/decisions/ADR-051-graph-future-semantics-and-reconstructable-information|D-051]] and [[notes/decisions/ADR-057-concrete-grammar-precedence-and-continuation|D-057]]
- Extends: [[notes/decisions/ADR-063-signatures-given-and-joint-on-bindings|D-063]]
- Affected documents: stored and computed fields, families, defaults, actions, tests, effect blocks, AST and IR

## Context

MUD uses `=` for stored or default values and `:=` for computed values. It was unclear whether a value written with `=` could be an expression, and how to name intermediate calculations in a `then` without turning them into world state.

A restriction to literal tokens would be too narrow. Expressions such as `1..2 | 3..4` are constant even when they combine literals and operators. Conversely, allowing `=` to read changing state would confuse “starts as” with “is calculated as”.

## Decision

### Closed static expression

A closed static expression is pure, deterministic and non-stochastic; can be fully evaluated at compile time; and does not consult state fields, participants, `given`, local values or world activity. It may use literals, `family` members, nominal anchors denoting statically known values, constructors and operations between constants. When a context supplies an expected type, it is elaborated against that type. Permitted nominal references do not read mutable payload or current activity of a `thing`.

### Use of `=`

The explicit value of a stored field, component, stored `family` datum or member assignment must be statically evaluable. It may be a short expression or `ValueBlock`, provided the complete body meets this contract. A `given` default remains specifically a closed static expression and does not accept `ValueBlock`.

```mud
lives: Nat = 3
king: Person = Arthur
allowed: Int Interval = 1..2 | 3..4
duration: Time = 1 hour + 30 minutes
```

The interval union produces one normalised discontinuous interval value; it is not a special exception. If `victories` is state, `initialScore: Nat = victories * 3` is invalid; the computed form is `score := victories * 3`. `=` introduces materialisable storage or a default, whereas `:=` declares a computed dependency. The distinction does not depend on how simple the expression looks.

```mud
initialScore: Nat = victories * 3   # invalid when victories is state
score := victories * 3
```

### Computed and stored locals

An executable block may declare a computed local with `x [derived-form] := value-body`, an immutable stored local with `x: X = value-body`, or a mutable stored local with `mut x: X = value-body`.

The computed form is pure and not assignable, retaining the applicable inference and coercion rules. Stored forms create execution-frame slots; only `mut` may be reassigned. An initializer is evaluated when execution reaches its declaration and may read the runtime projection visible there. None of these locals creates a field, public anchor or persistent state.

`value-body` may be a short expression or `ValueBlock`. `ExpressionBlock`, shared behaviour preambles and `TestAfterBlock` retain only the pure computed form with an ordinary expression RHS; nesting cannot provide storage or mutability.

A mutable local may satisfy a `for mut` participant. The call keeps a temporary binding to the slot and ordinary rollback reverts its changes. Other locals may satisfy only read-only participants or compatible `given` parameters.

### Sequencing, evaluation and scope

The declaration is evaluated exactly once when execution reaches its textual position, reading the private sequential projection produced by earlier instructions in the same `then`. Its value is fixed; later effects do not re-evaluate it even if they change fields used by the expression.

The name is visible from the instruction after its declaration to the end of its block; not before the declaration; usable by later local bindings; and unable to shadow or redeclare another visible name. Forward references and cycles are forbidden.

```mud
then {
    tax := basePrice / 10
    finalPrice := basePrice + tax
    account.balance -= finalPrice
}
```

This is invalid because `tax` is referenced before its declaration:

```mud
then {
    finalPrice := basePrice + tax
    tax := basePrice / 10
    account.balance -= finalPrice
}
```

Each `for each` block creates a new local scope per iteration. Locals do not survive into the next iteration. A `LocalForEach` in a `ValueBlock` may modify mutable slots in the enclosing `ValueBlock`; an executable traversal may additionally write authorised world locations.

A `then` still requires at least one effect or action call. A block consisting only of local bindings changes no world state and is invalid as an action body or reactive consequence.

## Consequences

- Persistent stored values and defaults under the static `=` contract accept more than literals but never depend on runtime state; stored locals in executable blocks follow their own runtime contract.
- Constant discontinuous intervals are assigned directly and normalised at compile time.
- Repeated calculations in a `then` can be named without extending the store.
- Local resolution is strictly textual and needs no fixed point.
- Traces may show a computed local's value, but it receives no anchor and is not published as state.

## Verification

1. Literal, nominal constructor and constant operation with `=`.
2. Union, intersection, difference and symmetric difference of constant intervals.
3. Rejection of state, participant, `given`, local or random reads in a static expression.
4. Local value with inferred and annotated type.
5. Rejection of ambiguous inference.
6. Local read of a preceding sequential effect.
7. Preservation of a local value across later effects.
8. Dependency on an earlier local.
9. Rejection of forward reference, cycle, redeclaration and shadowing.
10. Scope by block and iteration.
11. Acceptance of `in`, cardinality, `unique` and ordering as derived coercions, and rejection of `[mut]` as fabricated authority.
12. Rejection of a `then` without an observable effect.
