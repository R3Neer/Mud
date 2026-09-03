---
id: D-071
title: "Local bindings in Boolean blocks"
status: current
date: 2026-08-02
supersedes: []
superseded-by: []
questions: []
affects:
  - "Boolean rules, when, if, after, always, tests, grammar, CST, AST and local name resolution"
---
# ADR-071 — Local bindings in Boolean blocks

- Amended by: [[ADR-101-bloques-de-valor-variables-locales-almacenadas-and-extremos-por-testigos|D-101]].
- Extends: [[ADR-066-static-values-and-local-bindings-in-then|D-066]]
- Amends: [[ADR-041-contracts-under-the-three-types-of-rules|D-041]], [[ADR-055-declarative-and-diagnostic-tests-otherwise|D-055]] and [[ADR-058-temporal-triggers-changes-and-reactive-old|D-058]]
- Subsequently amended by: [[ADR-079-diagnostic-exterior-de-rules-always|D-079]]
- Amended by: [[ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]]

## Context

MUD conditions may need readable intermediate calculations. Repeating them inside a Boolean expression harms readability, while turning them into fields would introduce state that does not belong to the world.

MUD already has immutable local bindings via `:=` in `then` blocks. The same vocabulary must extend to conditions without making it ambiguous which Boolean value decides the clause.

## Decision

### Boolean block

A Boolean block contains, in this order:

1. Zero or more local bindings `name [derived-form] := expression`, with an optional static type and derived coercions over domain, cardinality, uniqueness or order.
2. Exactly one final expression.

The final expression must satisfy the owning construct's contract: it elaborates to `Bool` in Boolean rules, guards, invariants and postconditions; in `when`, it elaborates to an activator admitted by D-058. An expression without declaration form must be the last expression in the block; a second non-declarative expression is invalid.

```mud
if {
    cost := amount * price
    available := kingdom.money
    available >= cost
}
```

Boolean blocks are admitted in Boolean rule bodies, `when` and `if` clauses, `always` rule bodies, action `after` postconditions and test assertions where their concrete form permits it. The braced-less form with one expression remains valid and normalises to a block with no locals.

### Evaluation and scope

Local bindings are pure, immutable and evaluated sequentially once per clause evaluation, against the same snapshot observed by the condition. They create no persistent state and survive no other evaluation.

Each name is visible from the following declaration through the final Boolean expression and its associated `otherwise`, if any. It is not visible in `then`, another clause or outside the block. D-066's prohibitions remain: no forward references, cycles, redeclaration or shadowing.

In a `when`, a local used by `changes` or `old` is evaluated from its defining expression in each required snapshot; the binding itself stores no value between waves.

### Test `after`

A test's `after` block is a non-empty sequence of assertions, not one condition. It may begin with zero or more common local bindings, followed by one or more assertions. Locals are visible in every assertion and its `otherwise`.

```mud
after {
    expected := before + amount
    kingdom.soldiers == expected
    kingdom.treasury >= 0
}
```

No new local declaration may be interleaved after the first assertion. A test's `then` retains the effect blocks and local bindings defined by D-066.

### Abstract representation

D-088 generalises the common representation. The surface AST normalises every condition to `ExpressionBlock(locals, result)`. In these contexts the owner requires `result` to satisfy the corresponding Boolean or temporal contract. The `otherwise` diagnostic belongs to the owning construct and may resolve local names. A test `after` uses its own block with common locals and a non-empty sequence of `TestAssertion` nodes.

## Consequences

- Intermediate calculations are not duplicated or added to the store.
- The final expression unambiguously identifies the condition's result.
- One model serves rules, guards, postconditions and tests.
- Visibility in `otherwise` enables informative diagnostics without creating anchors for locals.

## Verification

1. Block without locals equivalent to the short form.
2. One or more locals before the final expression.
3. Rejection of a block without a final expression or with two non-declarative expressions.
4. Sequential use of an earlier local.
5. Rejection of forward reference, cycle, redeclaration and shadowing.
6. Visibility in `otherwise` and no visibility in `then`.
7. Temporal re-evaluation of locals used by `changes` or `old`.
8. Common locals in test `after` with one or more assertions.
9. Rejection of a local after the first test assertion.

## Amendment by D-088

The structure generalises to `ExpressionBlock(locals, result)`. Conditions retain their Boolean/temporal contracts; `select`, `exists`, `forall`, `count`, `min` and `max` may write a short expression or `{ locals*; result }` after `:`, with the same rules for purity, sequencing, scope and the absence of forward references, cycles, redeclaration and shadowing.
