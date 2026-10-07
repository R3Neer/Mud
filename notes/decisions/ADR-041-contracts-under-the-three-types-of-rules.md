---
id: D-041
title: "Contracts under the three types of rules"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-005"
  - "Q-050"
affects:
  - "language model, static semantics, dynamic semantics"
---
# ADR-041 — Contracts under the three types of rules

- Amended by: [[ADR-126-reactive-binding-identity-and-observation-episodes|D-126]].

- Amended by: [[ADR-119-invocation-owned-completion-and-imagine|D-119]].

- Amended by: [[ADR-118-action-replies-refusals-and-errors|D-118]].

- Related to: [[notes/decisions/ADR-025-vocabulary-from-thing-headings-and-sections|D-025]], [[notes/decisions/ADR-055-declarative-and-diagnostic-tests-otherwise|D-055]]
- Amended by: [[notes/decisions/ADR-058-temporal-triggers-changes-and-reactive-old|D-058]] and [[ADR-079-external-diagnostics-for-always-rules|D-079]]
- As further amended by: [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]]
- Also amended by: [[notes/decisions/ADR-063-signatures-given-and-joint-on-bindings|D-063]]
- Expanded by: [[notes/decisions/ADR-071-local-bindings-in-boolean-blocks|D-071]]
- Example of membership updated by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]]
- Related questions: Q-005, Q-050
- Documents concerned: model of language, semantics static, semantics dynamic

## Context

MUD uses a single declarative word, `rule`, for three different mechanisms. Sharing a name must not allow for ambiguous bodies or a general variant with arbitrary combinations of clauses.

## Decision

The AST comprises three distinct variants: Boolean rule, reactive rule and ruler `always`.

### Regla booleana

```mud
rule CanAttack for
    attacker: Army,
    defender: Army
given
    maximumDistance: Length
{
    ...
}
```

Register participants via `for`, may state `given`, is pure and returns `Bool`. You can use quantifiers, Boolean aggregations, `imagine` and, where the analysis so permits, `eventually`.

Their `given` They are read-only values and can be declared as static defaults. Calls bind them by position or by name in accordance with D-063.

You cannot type state, apply effects, create, destroy or read a field calculated stochastic. It query explicitly via the protocol for receivers and arguments of D-036.

One Boolean rule Non-productive pruning is carried out in accordance with the structural pruning of D-022, not as a call which returns a fixed Boolean value.

### Regla reactiva

```mud
rule OpenGate on gate: Gate [mut] {
    when gate.unlocked
    if not gate.open
    then gate.open = true
}
```

It declares automatic links through `on`, does not support `given`, requires `when`, admits `if` and has consequences through `then`. The `then` block can combine effects, locals and calls to `action` or `subaction` within causal resolution, in accordance with D-096. Boolean rules can be queried with `imagine` when the resulting graph remains acceptable.

Roles within the same header `on` are solved jointly and may form finite cyclic relational constraints in accordance with D-063.

Be $W_n$ the snapshot read at the beginning of the wave $n$ and let it be $v_n(b,e)$ the value of the expression $e$ for recruitment $b$ in that snapshot. For a link that already has a history, a `when e` 'Purely Boolean' only fires when:

$$
\neg v_{n-1}(b,e)\land v_n(b,e).
$$

Therefore, only shoot in the transition $\mathsf{false}\longrightarrow\mathsf{true}$. The runtime retains the value previous by identity of engagement.

The suffix `changes` accepts any pure expression with a defined equality and produces, in the wave $n$ the pulse:

$$
\operatorname{changes}_n(b,e)
\iff
v_{n-1}(b,e)\ne v_n(b,e).
$$

This pulse is calculated directly for each pair of consecutive snapshots. It is not a stored Boolean value, is not reset by a change to `false`, and does not undergo the $\mathsf{false}\rightarrow\mathsf{true}$ edge test again. If $e$ changes between two consecutive snapshot pairs, `changes` fires on both transitions. Only the net change between snapshots matters; transient values within a private delta are not observable.

Temporary triggers are made up of the words `and` and `or`. An ordinary Boolean operand in a composition is raised to its `false` → `true` transition; it is not interpreted as a sustained level. The grammar, `old` scope and elaboration of these combinations are set out in D-058.

### Initialisation of the reactive memory

The links found in the first snapshot by combining part `start with` contributions, or contributions compiled for a test world, receive a virtual previous Boolean value of $\mathsf{false}$ for each branch. If a branch is true in that first stabilisation snapshot, it fires. Temporal expressions, including `changes` and `old`, compare against the initial snapshot itself: `changes` does not fire and `old e` equals `e`.

A connection that was not present in that first snapshot, whether because a rule activated it or because participants arrived, does not take part in the root or wave that creates it. During its first wave it stores the current value without firing `when` or producing a `changes` pulse. Subsequent waves compare two snapshots normally. In particular, if it stores $\mathsf{false}$ and the condition is $\mathsf{true}$ in the next wave, `when` fires; if it is first memorised as $\mathsf{true}$, that mere appearance does not trigger it.

### Ruler `always`

```mud
always rule ValidPosition on game: Game {
    game.board has game.position
}
```

An always rule declares automatic on bindings, has no given or world effects, and checks a pure Boolean body after each consolidated root and wave. False yields AlwaysRefusal; unsuccessful evaluation yields Error. Otherwise handles only the latter through the protected expression block, without a missing-handler warning.

### Cycle of communal life

All three variants have one canonical top-level definition, which can be activated via `start with` or `create Name` and suspended by `destroy`, in accordance with D-021 and D-054. They retain their variant when reactivated. Suspending an `always` rule temporarily waives this obligation; reactivation cannot publish a state that violates it.

All three variants fall into the category of anchor `rule::*`. In particular, `always` is a contextual word in front of `rule`, neither a nominal category nor a prefix from anchor independent.

## Consequences

- A heading or combination of clauses that corresponds to more than one variant is rejected.
- Only Boolean rules can be called using result Boolean.
- Of all the rules, only the multiple-choice questions contain `then` and have consequences that may alter the world.
- Reactive rules and `always` They may also act as declarative trigger sources in accordance with D-096.
- A false always invariant refuses the transition with AlwaysRefusal; errors while computing it remain Error values.
- Persistent binding identity uses the rule and role-associated participant identities. Disappearance, suspension or a changed activation/materialisation ends its observation episode; reappearance establishes a baseline without firing.

## Verification

1. One valid example and one invalid example for each variant.
2. Rejection of `given` on a ruler `on`.
3. Rejection of effects in Boolean rules and `always`.
4. A shot from a `when` purely Boolean only in `false → true`.
5. Pruning a call suspended Boolean.
6. `changes` click on consecutive changes without a wave false intermediate.
7. Absence of a pulse when an expression changes temporarily but remains the same value between snapshots.
8. Opening shot of a `when` genuine, originating from `start with`.
9. Initialisation without triggering a binding created outside `start with`.
10. A combination of two `changes` expressions and a Boolean transition using `and` and `or`.
11. Consecutive pulses preserved within a time sequence.
12. AlwaysRefusal on false, computing Error on unsuccessful evaluation, and no missing-diagnostic warning.

## Amendment current by D-096

One rule reactive remains non-callable as Boolean rule, but his `then` can invoke actual actions and sub-actions within the causal resolution active. Reactive rules and `always` They can also act as declarative trigger sources: the reactive one fires when it is actually triggered, and the `always` when being assessed for recruitment/onda relevant. Actions, sub-actions, looks, Boolean rules and tests do not act as triggers.
