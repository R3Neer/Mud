---
title: Static contracts of reactive rules
tags:
  - mud/specification
status: proposed
normative: true
depends-on:
  - "[[04-mathematical-model]]"
  - "[[10-names-and-anchors]]"
  - "[[11-type-system]]"
  - "[[15-fields-and-mutability]]"
  - "[[20-blocks-and-recovery]]"
  - "[[21-expressions]]"
  - "[[28-effects]]"
questions:
  - Q-020
  - Q-028
  - Q-029
  - Q-072
decisions:
  - D-166
  - D-021
  - D-036
  - D-041
  - D-048
  - D-058
  - D-063
  - D-087
  - D-096
  - D-118
  - D-123
  - D-126
  - D-128
  - D-137
  - D-155
  - D-162
---

# 24. Static contracts of reactive rules

## Automatic bindings and consequences

A reactive rule has automatically related on roles, a required when trigger,
an optional pure if guard and authorised then consequences. It is a canonical
activatable declaration, not a Bool callable or a source of action return values.

```mud
rule OpenGate on gate: Gate [mut] {
    when gate.unlocked
    if not gate.open
    then gate.open = true
}
```

Gate has visible Bool unlocked and mutable Bool open fields in the declaring
part. Inner capability authorizes the member write; it does not authorize
replacing the on role or mutate foreign private fields.

## Joint on admission

> [!rule] MUD-REACT-001 — Finite relational binding contract
> Each named on role binds one value, without outer mutability or collection
> cardinality/order/uniqueness modifiers. Collect the entire header before
> resolving related sources and optional nominal refinements. Require a unique
> static type solution and finite enumerable source/constraint evidence.

A direct typed role uses the finite concrete active strict-descendant universe
in the supplied wave snapshot. A type such as Nat has no implicit direct on
universe; use an admitted related source. Related `name[: Type] in source`
selects members meeting both source membership and optional nominal refinement.
All role names are visible throughout the header, including earlier sources.
Relations like a in b.friends and b in a.friends are joint finite constraints,
not recursive computed-domain equations or left-to-right variable initialization.

Let U_i(W,b) describe each role's universe/relation in snapshot W for candidate
assignment b. The binding set contains exactly the total assignments satisfying
all constraints. Repeated membership does not duplicate one assignment; roles
may have the same value unless an explicit constraint excludes it. Exchanging
two named roles gives a different assignment. Values actually compared to
establish assignment identity/join require supported equality under MUD-TYPE-040;
functional policy values cannot gain internal equality from on syntax.

The operational interface supplies one fixed binding set at wave entry.
Effects cannot retroactively edit it. This contract specifies the set and
admission obligations, not an indexing strategy, enumeration priority or causal
binding-discovery algorithm. Hard-dependency suspension removes current effective
bindings without rewriting signature slots.

## Preambles and body checking

After metadata and before behavior clauses, pure immutable stored/live-derived
locals and positional patterns are admitted. Their initializer/body checks
retain ordinary static type, domain, shape and flow contracts, without outer
effects. A stored local captures once when its frame is instantiated; a live
derivation reads its definition in the applicable view. Neither introduces
persistent rule fields. The causal algorithm must supply the corresponding
evaluation frames; this chapter does not choose additional frame lifetimes.

For a checked binding b, let C_b be the declaring environment and permissions.
Require when to elaborate to an admitted temporal source, if to check as pure
non-stochastic Bool [1], and then to check in Effect mode with all authority,
complete-block cardinality/domain and transitive effect obligations. No given,
generic parameters or Boolean-rule invocation result is introduced. False if
suppresses consequences, not observation; a computing fault uses Error recovery.
Permitted real action/subaction calls remain within the active resolution and
cannot open another host root.

## Trigger categories and composition

> [!rule] MUD-REACT-002 — Temporal qualification is not a stored type
> A when accepts Rise of an ordinary pure Bool, Temporal comparison involving
> old, Changed of a pure equality-supported expression, or an admitted causal
> declaration source. Trigger qualification is not a first-class public type,
> ordinary Bool value or host callable.

For one continuing observation episode, let prev(e) and now(e) denote values
from the supplied consecutive snapshots. Rise(e) pulses when not prev(e) and
now(e). A Bool expression using old is tested directly over that pair, without
another rising-edge test. Changed(e) pulses on supported inequality of prev/now
at each transition; two consecutive changes can pulse twice. Transient private
values that leave equal wave snapshots create no Changed pulse.

Changes is valid only in reactive/message when and has lower precedence than
arithmetic/conversion/comparison, higher than and/or. It cannot be stored,
returned, used as an if value or applied to functional values requiring
unsupported equality. Old in reactive when/if retains the operand's type and
reads the previous snapshot; it is invalid in then. Action/test after uses its
own entry-view old contract, not this wave pair.

Temporal compositions use and as natural join of compatible matches (Cartesian
product when no binding is shared) and or as union. Match occurrence identity
preserves distinct equal-payload occurrences. An ordinary Bool subexpression is
raised as one Rise unit; its internal ordinary Boolean logic remains ordinary.
Not/xor/implications and symbolic collection operators do not accept Trigger
operands. These restrictions do not prohibit ordinary Boolean operations inside
a Bool branch before temporal qualification.

Message occurrences, actual reactive firings and always evaluations can supply
declarative sources without `()`. Action/subaction, look/sublook, Boolean rules
and tests cannot. A derived local may name a causal declaration source without
preselecting an occurrence. A trigger source can expose payload/bindings only
where every possible match establishes them. Joint and combines available
bindings; alternative or guarantees only common compatible bindings. Type/flow
narrowing cannot invent a match absent from an alternative.

## Observation identity and baselines

Persistent binding identity associates the canonical rule with named participant
identities/values under the binding contract. Field changes and enumeration
position do not change that association. Observation memory belongs to an
episode under the same rule activation and concrete participant materialisations.
Absence/suspension or actual destruction/recreation ends the episode, even when
a generation change occurs between observed snapshots. Lifecycle no-ops do not.

Initial start-with bindings have virtual previous false for ordinary rising
branches; changes does not pulse and old sees the initial snapshot. Later/resumed
episodes start with a baseline and no memory-based pulse; comparison begins
with the next observation. Direct causal occurrences retain their independent
match identity and are not erased by temporal baselines. Empty-to-value in a
continuing observed expression is a real change; missing history is not empty.
Memory is tentative and respects rollback/isolation. These are interface
invariants, not a memory layout or update scheduler.

## Operational boundary and conformance

The complete discovery/readiness/causal attribution/completion algorithm remains
[[../notes/questions/Q-072-causal-work-and-reality-completion-algorithm|Q-072]].
Oscillation detection remains [[../notes/questions/Q-020-o-oscillations-and-wave-limit|Q-020]];
it is not inferred from static trigger composition. Dynamic-call impact follows [[types/contextual-call-analysis]];
finite/termination certification remains Q-028/Q-029. None of these gaps
permits unproved static permissions or fabricated runtime selection.

Reject given, outer-mutable on, nonenumerable related sources, ambiguous header
types, unsupported temporal operators, unguaranteed payload accesses, stochastic
guards and effects outside authority. `when gate.unlocked and gate.ready` is
one rising condition, while `when gate.position changes and gate.speed changes`
joins temporal matches. A false guard does not reset observation history.

Grammar/AST coverage, [[types/typing-cases.yaml]] and [[effects/README]] supply
signature/mode/binding/temporal and protected effect cases. Nominal HIR retains
role/source ownership and references; match identities, temporal memory,
permission proofs and selected causal owners are later semantic objects.
