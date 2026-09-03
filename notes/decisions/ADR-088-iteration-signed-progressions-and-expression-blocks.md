---
id: D-088
title: "Iteration, signed progressions and expression blocks"
status: current
date: 2026-08-15
supersedes: []
superseded-by: []
questions:
  - "Q-018"
  - "Q-028"
  - "Q-029"
  - "Q-032"
affects:
  - "for each, filters, quantifiers, selection, stepped domains, intervals, magnitudes, expression blocks, name resolution, grammar, CST and AST"
---

# ADR-088 — Iteration, signed progressions and expression blocks

- Modified by: [[ADR-101-bloques-de-valor-variables-locales-almacenadas-and-extremos-por-testigos|D-101]].

- Modifies: [[ADR-047-quantifiers-and-finite-iteration|D-047]], [[ADR-057-concrete-grammar-precedence-and-continuation|D-057]], [[ADR-071-local-bindings-in-boolean-blocks|D-071]], [[ADR-075-enumerable-domains-all-and-derived-value-form|D-075]], [[ADR-081-filtering-take-and-indexing-de-collectiones|D-081]] and [[ADR-082-cycle-as-point-domain-modifier|D-082]].
- Retains: [[ADR-034-num-exactly-and-rum-binary64|D-034]], [[ADR-040-semantics-remaining-basic-numeracy|D-040]] and D-048's prohibition on randomness in filters of [[ADR-048-reproducible-randomness-and-errors|D-048]].
- Modified by: [[ADR-095-extremos-vacios-como-ausencia-ordinaria|D-095]] in the result form of `min` and `max` on absence.
- Modified by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]] in the identity and derivation of random points.
- Related questions: [[notes/questions/Q-018-i-discontinuous-intervals|Q-018]], [[notes/questions/Q-028-f-finiteness|Q-028]], [[notes/questions/Q-029-t-termination|Q-029]] and [[notes/questions/Q-032-a-reproducible-randomness|Q-032]].

## Context

MUD already has `for each`, quantifiers, pure selection and stepped domains, but the earlier rules mixed enumerability, progression by a difference and the structure of the body after `:`. D-075 also required a positive step, and D-047 did not precisely distinguish when an ordered iteration's filter can observe earlier effects.

## Enumerable sources and `for each`

`for each` accepts any source whose finiteness and enumerability can be demonstrated: collections, exact dictionaries, enumerable intervals, finite enumerable domains and any other value with a defined canonical enumeration. An interval remains an interval; being enumerable does not turn it into a collection.

```mud
action Accumulate for values: Int [* ordered], mut total: Int {
    then for each value in values :
        total += value
}
```

The source membership is captured when the loop starts. An empty interval produces zero iterations. An infinite interval cannot feed a construction requiring exhaustive enumeration.

## Separator `:` and bodies

When a construct uses `:` to separate a header from a subordinate body, braces belong to the following body and never replace the separator.

```mud
action AccumulateDoubled for values: Int [* ordered], mut total: Int {
    then for each value in values : {
        doubled := value * 2
        total += doubled
    }
}
```

The form without `:` is invalid. After `:`, the body may begin on the same line or after physical separation by terminators; the line break does not change the AST. Executable `for each` uses the `EffectBlock` contract. A `for each` written inside `ValueBlock` instead uses `LocalStatementBlock`, without outer effects and restricted to D-101's local statements.

Selection and `exists`, `forall`, `count`, `min` and `max` likewise retain their mandatory `:`. Their body may be a short expression or an expression block with zero or more local bindings followed by a single final expression.

## Expression block

The former `BooleanBlock` is generalised to `ExpressionBlock(locals, result)`. The structure does not determine the type of `result`; its owner does. Boolean rules, `if` guards, `always` rules, action `after` postconditions, selection, `exists`, `forall`, `count`, `min` and `max` apply a Boolean contract to `result`; `when` requires an admitted trigger. `min` and `max` use that result as a filter and return witnesses according to source order. Test `after` retains its own structure of several assertions.

Locals are pure, immutable and sequential, and do not admit forward references, cycles, redeclaration or shadowing.


## Iteration scopes and expression blocks

`source` and optional `by` are resolved in the outer environment before introducing the iteration binding. Therefore, the iterated variable—or the `(key, value)` pair—is not visible inside `source` or `by`.

In `for each`, the iteration binding is visible in the `if` filter and the corresponding subordinate body. If the filter uses an `ExpressionBlock`, its locals are visible only in later locals and the filter's final expression; they disappear before entering the executable `EffectBlock` or the `LocalStatementBlock` of a `LocalForEach`.

In selection and quantifiers, the introduced binding is visible in the locals and final expression of their `ExpressionBlock`, but not outside it. Each local becomes visible after its own declaration, so it may be used by later locals and the final result, never by its initialiser or earlier declarations.

## `for each` filter

The optional `if` appears after `by` and may be an expression or expression block. The predicate is pure and non-stochastic in accordance with D-048.

- With semantic order, each filter is evaluated immediately before its iteration and observes sequential effects produced by earlier iterations.
- Without semantic order, all filters observe the same initial snapshot and accepted iterations produce deltas consolidated as simultaneous.

Therefore, `for each ... if ...` is not universally defined as literal desugaring to a pre-materialised selection.

## `by` as progression

`by δ` takes an ordinary expression whose value is a signed difference compatible with the source. In runtime constructs it is evaluated exactly once before traversal begins and its value remains fixed during that execution.

Compatibility is determined by the advance operation and the admitted exact implicit conversions, not by nominal equality between the traversed type and the difference. A `Nat` interval may use an `Int` difference; an interval of `Num` may use compatible `Nat`, `Int` or `Num`; a magnitude may use another compatible unit. For point magnitudes, the step is a difference of the underlying linear magnitude, not another point.

A positive step is anchored at the lower bound; a negative one at the upper bound. If the initial bound is open, the step is applied once before checking the first candidate. After each emitted value the step is added and traversal ends before the first outside candidate. Reaching the opposite endpoint exactly is not required.

```mud
action Forward for mut total: Num {
    then for each value in [1..8] by 2 :
        total += value
}
# traversal: 1, 3, 5, 7

action Backward for mut total: Num {
    then for each value in [1..8] by -3 :
        total += value
}
# traversal: 8, 5, 2
```

Inverted endpoints continue to normalise to `empty`; they never express descending traversal.

## Zero step

If a runtime step is demonstrably zero, it is a static error. If this cannot be demonstrated and it eventually evaluates to zero, evaluation fails with `progression-step-zero`. Inside a real action that failure produces `failed` and rollback under the taxonomy of D-048 and D-061; in a pure context it propagates under the expression-failure contract without becoming `false`. In a stepped domain the step is static, so zero is always an elaboration error.

## Default steps

A source that already has its own enumeration—for example a collection, exact dictionary or finite nominal domain—does not need `by` to be traversed. Default steps apply only when enumeration is constructed as a progression. In a source whose enumeration is constructed as a progression, `by` may be omitted only when the traversed type defines a canonical successor difference. MUD fixes `Nat -> 1`, `Int -> 1` and `Money -> 0.01`; omitting `by` always selects that positive difference. Other exact-progression types require an explicit step unless a decision defines a canonical successor.

`Num` admits progression with an explicit exact step, but a general `Num` interval without a step is invalid. `Rum` retains D-034's prohibition: its intervals are never enumerable and do not admit `by` progression, either in iteration or stepped domains. An explicit collection of `Rum` values may be enumerated without `by` because its enumeration comes from the collection, not a numeric progression.

## Stepped domains

`interval by δ` defines a domain through the same exact progression. The step must be static, non-zero and compatible, and may be negative.

```text
[1..8] by 2   -> {1, 3, 5, 7}
[1..8] by -2  -> {2, 4, 6, 8}
(1..8] by 2   -> {3, 5, 7}
[1..8) by -2  -> {2, 4, 6}
```

The sign determines the anchor and may change the domain's members, but generation order is not part of the type. `all` materialises members in the type's canonical order.

Stepped domains may appear in any context admitting a domain: fields, components, participants, `given`, derived forms, public fields and other compatible owners.

## Discontinuous intervals and cyclic point domains

In a normalised form with several disjoint segments, the step restarts in each segment. A positive step traverses segments from lower to higher and anchors at the lower endpoint; a negative one traverses from higher to lower and anchors at the upper endpoint.

The consolidated syntax of discontinuous intervals remains open in Q-018. D-088 settles explicit descending traversal: it is expressed by a negative step, never by reversing endpoints.

A cyclic point domain may be enumerated with a compatible difference, but only for one fundamental period. It never wraps indefinitely.

## Other constructs with `by`

Progression `by` is also admitted in selection and in `exists`, `forall`, `count`, `min` and `max`, provided that the source offers progression by difference. If selection conceptually starts from a domain, its source must be written materialised as `all D`; traversals and quantifiers that do not produce a collection may consume the domain directly. `by` does not mean stride over an arbitrary collection. The absence semantics of `min` and `max` is D-095's: no candidate produces `empty` with cardinality `[0..1]`. A future source may define that capability explicitly; this decision introduces no general protocol. `ordered by path` retains different semantics.

## Randomness

D-088 does not permit randomness in an iteration filter. The semantic identity and reproducible derivation of random points are already fixed; the prohibition remains while Q-032 keeps open the per-occurrence caching and retry rules affecting the filter's observable stability.

## AST consequences

The Surface AST replaces `BooleanBlock` with `ExpressionBlock`. `ForEachEffect` retains `step?`, retains its optional filter as `ExpressionBlock?`, and normalises both the short effect and executable block to the same `EffectBlock` used by `then`. `SelectionExpr` and `QuantifierExpr` retain `step?` and their predicate/body as `ExpressionBlock`. `by -2` needs no special sign node.

## Diagnostics

The implementation must diagnose a missing `:`, zero step, incompatible difference, missing step when a progression has no default successor, an infinite/non-enumerable source, attempted progression over a `Rum` interval, `by` on a source without progression, a non-Boolean filter, randomness in a filter, and use of inverted endpoints as presumed descent.

## Verification

Verification covers enumerable sources of every admitted class, `:` with short and braced bodies, short filters and filters with locals, positive/negative/runtime steps, single step evaluation, static/runtime zero, open/closed bounds, empty/infinite intervals, signed stepped domains and `all`, `Num`, rejection of `Rum` progression, explicit `Rum` collections, selection and the five quantifiers with `by` and Boolean blocks, magnitudes with compatible units, and the distinction between ordered and unordered filters. Concrete verification of discontinuous intervals is completed when Q-018 closes its consolidated source form; their semantics are fixed by this decision. The requirement to traverse at most one fundamental period of a cyclic domain belongs to D-082's verification and does not depend on Q-018.

## Current amendment by D-096

Operations that produce a collection from a domain, including selection, require explicit `all D` materialisation. `for each` traversals and quantifiers may consume finite enumerable domains directly because they do not themselves materialise a collection. Actions, reactive rules and messages also admit preceding pure locals between metadata and behaviour clauses.
