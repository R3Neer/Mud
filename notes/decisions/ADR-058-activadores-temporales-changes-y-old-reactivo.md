---
id: D-058
title: "Temporal triggers, `changes` and reactive `old`"
status: current
date: 2026-07-29
supersedes: []
superseded-by: []
questions:
  - "Q-005"
affects:
  - "[[specification/07-concrete-grammar]], `specification/grammar/mud.ebnf`"
---
# ADR-058 — Temporal triggers, `changes` and reactive `old`

- Amends: [[notes/decisions/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notes/decisions/ADR-042-acciones-raiz-y-resultados|D-042]], [[notes/decisions/ADR-045-resolucion-causal-vinculaciones-y-cola|D-045]], [[notes/decisions/ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]], [[notes/decisions/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]] and [[notes/decisions/ADR-057-gramatica-concreta-y-continuacion|D-057]]
- Related questions: Q-005
- Extended by: [[notes/decisions/ADR-071-vinculaciones-locales-en-bloques-booleanos|D-071]]
- Affected documents: [[specification/07-concrete-grammar]], `specification/grammar/mud.ebnf`

## Context

D-041 distinguished two complete forms of `when`: `when e`, which detected `false → true`, and `when e changes`, which compared consecutive values. Although the prose described `changes` as postfix, the grammar permitted it only at the end of the entire clause. It could not express triggers such as:

```mud
when position changes or ready
when position changes and velocity changes
```

Treating `changes` as an ordinary `Bool` would not work either. If the value changes in two consecutive transitions, the pulse would be true in both, and a second outer `false → true` detection would miss the second one.

## Decision

### Triggers

The temporal semantics use the notation `Rise(e)`, `Temporal(e)` and `Changed(e)`. These forms distinguish temporal sources from ordinary `Bool` values, but do not prescribe concrete IR constructors: D-096 leaves the exact internal representation of causal matches and their composition open.

```text
TemporalSource
    = Rise(BoolExpression)
    | Temporal(BoolExpression)
    | Changed(Expression)
```

For a binding $b$, let $v_n(b,e)$ be the value of the pure expression $e$ in the initial snapshot $W_n$ of wave $n$.

A `when e` containing neither `old` nor `changes` is elaborated as a single `Rise(e)`:

$$
\operatorname{Rise}_n(b,e)
\iff
\neg v_{n-1}(b,e)\land v_n(b,e).
$$

Its inner Boolean operators therefore continue first to form a level condition. In particular, `when ready and authorized` detects that the complete conjunction changes from false to true.

A Boolean `when` expression using `old` forms a `Temporal` trigger: it is evaluated directly over the pair $(W_{n-1},W_n)$ and pulses on every transition for which it is true. It is not then subjected to another `false → true` detection.

`e changes` forms:

$$
\operatorname{Changed}_n(b,e)
\iff
v_{n-1}(b,e)\ne v_n(b,e),
$$

and requires the type of $e$ to have defined equality. It is temporal sugar equivalent to comparing the previous and current values:

```mud
e changes
old e != e
```

The equivalence is semantic; it does not require the compiler to discard the original form or its provenance in the AST.

### Composition

A trigger produces zero or more causal matches. The temporal forms `Rise`, `Temporal` and `Changed` describe when a binding contributes a match; when an ordinary `Bool` operand participates in a temporal composition, it is raised to `Rise` as before.

`and` performs a natural join of compatible matches from both operands and, if they share no bindings, their Cartesian product. `or` performs the union of matches. The identities of causal occurrences form part of a match, so two distinct occurrences are not deduplicated even when they have the same payload.

```mud
when position changes and velocity changes
```

requires compatible matches whose net differences correspond to the same step between snapshots. A parenthesised ordinary Boolean subexpression is raised as a unit: `(ready or authorized) and position changes` uses `Rise(ready or authorized)`, not two independent sources.

Triggers are initially combined only through `and` and `or`. `not`, `xor`, `=>`, `<=>`, `&`, `|` and `^` do not accept `Trigger` operands. This restriction does not prevent ordinary Boolean operators from being used within the Boolean expression of a `Rise` or `Temporal`. D-096 additionally introduces occurrences of `message`, firings of reactive rules and evaluations of `always` as declarative sources.

### Precedence of `changes`

`changes` is a postfix operator in the temporal layer. It has lower precedence than arithmetic operations, conversions and comparisons, but higher precedence than `and` and `or`:

```mud
when position + offset changes
when temperature > limit changes
when position changes or ready
```

These are grouped respectively as:

```text
(position + offset) changes
(temperature > limit) changes
(position changes) or ready
```

Parentheses alter the logical scope:

```mud
when (ready and authorized) changes
```

`changes` is valid only within the `when` of a reactive rule or a `message`. It does not produce a value that may be stored, returned or used in `if`, `then`, `after`, calculated fields or Boolean rules.

In block form, the operator belongs to the inner expression:

```mud
when {
    calendar.day changes
}
```

### `old` in reactive rules

Within the `when` and `if` of a reactive rule:

```text
old e
```

evaluates the pure expression $e$ in $W_{n-1}$ and retains its type. The expression must be evaluable in both $W_{n-1}$ and $W_n$. It is not limited to the expression observed by `changes`:

```mud
when price changes
if price > old price and stock < old stock
```

An `if` without `old` is evaluated over $W_n$. `old` is not permitted within `then`: D-058 introduces temporal observation, not retrospective effects.

Within the `after` of an action or test, `old` retains the semantics of D-042 and D-055: it observes the stable state preceding the complete resolution, not the preceding wave. Outside those contexts and a reactive `when` or `if`, `old` is a static error.

A temporal comparison can measure quantitative changes without additional syntax:

```mud
when position - old position >= 10 meters
```

MUD 1.0 therefore introduces no `changes by`. The types that permit subtraction determine the type and meaning of the difference; `changes` remains available for every type with equality.

### Baseline

For bindings present in the first snapshot materialised by `start with`:

- each temporal reading `old e` initially takes the same value as $e$ in $W_0$;
- `Changed` and `Temporal` retain that baseline and do not pulse by themselves;
- a `Rise` retains the virtual previous false value from D-041 and may pulse when its initial condition is true;
- in a composition, temporal branches do not pulse and `Rise` branches are evaluated with that virtual previous value.

If a `Rise` branch causes an initial firing, an `old e` used by the rule's `if` reads the baseline $W_0$ and therefore initially matches the current value of $e$.

A binding created after `start with` retains the previous policy: its first active wave establishes its complete baseline without firing any trigger, and comparison begins in the following wave.

## Consequences

- The surface AST retains `changes` as a suffix and the written composition; the semantic model must preserve the behaviour of zero or more matches, their bindings/witnesses and causal identities. D-096 does not prescribe a closed IR encoding for those matches.
- Reactive memory retains the previous values required by `when` and `if`, not merely an aggregate Boolean.
- Temporal pulses may occur in consecutive waves.
- A quantitative difference uses the ordinary operators and the magnitude system.
- The identity and preservation of this memory when a binding disappears remain in Q-005.

## Rejected alternatives

### Maximum precedence

This would make `position + offset changes` attempt to combine `position` with a trigger applied only to `offset`. `changes` must first receive the complete value constructed to its left.

### `changes by`

It does not establish whether the difference is signed, absolute, exact or minimal, and would have direct meaning only for some types. `old` and the ordinary operators express the check without a second syntax.

### `old` only on the changed expression

The transition already provides two complete snapshots. Preventing cross-comparisons such as current price against previous stock neither adds safety nor simplifies the runtime.

## Verification

1. `changes` on access, addition, conversion and comparison with the agreed precedence.
2. Union of matches through `or`, and compatible natural join/Cartesian product through `and`, while preserving causally distinct occurrences.
3. Raising an ordinary Boolean operand to `Rise` in a temporal composition.
4. Two consecutive changes produce two pulses.
5. `old` in `when` measures a difference and may pulse in consecutive transitions.
6. `old` in `if` queries any pure expression available in both snapshots.
7. Rejection of `changes` outside `when`, reactive `old` within `then`, and unsupported temporal operators.
8. No temporal pulse at the initial baseline, and a possible initial pulse from a `Rise` branch.
9. A subsequently created binding establishes its baseline without firing.
10. Rejection of `changes by`.

## Current amendment by D-096

The `Trigger` algebra is generalised from Boolean pulses to zero or more causal matches. A match retains bindings/witnesses and occurrence identity. `and` performs a natural join of compatible matches and `or` their union. Messages, reactive rules and `always` may be declarative trigger sources; an `on` declaration reference takes no call parentheses.
