---
title: Static contracts of always rules
tags:
  - mud/specification
status: proposed
normative: true
depends-on:
  - "[[04-mathematical-model]]"
  - "[[11-type-system]]"
  - "[[20-blocks-and-recovery]]"
  - "[[21-expressions]]"
  - "[[24-reactive-rules]]"
  - "[[28-effects]]"
questions:
  - Q-007
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
  - D-063
  - D-071
  - D-087
  - D-096
  - D-118
  - D-120
  - D-123
  - D-128
  - D-137
  - D-155
  - D-162
---

# 25. Static contracts of always rules

## Invariant declarations

An always rule checks a pure Boolean condition for its automatic bindings at
the mandatory consolidated checkpoints. It is distinct from a callable Boolean
query and a reactive consequence rule.

```mud
always rule Nonnegative on account: Account {
    account.balance >= 0
}
```

Account has an accessible Money balance contract. Successfully computing false
refuses the proposed resolution; failing to compute a Bool produces Error.

> [!rule] MUD-ALWAYS-001 — Pure invariant signature
> An always rule uses the admitted joint on binding contract and a pure
> singleton-Bool ExpressionBlock. It has no for/given parameters, generic
> parameters, when/then consequences or real world effects. Otherwise may
> recover computing errors under the same pure Bool result contract.

## Binding and body admission

On types, related sources, nominal refinements, joint header scope and inner
capabilities follow [[24-reactive-rules#Joint on admission]]. Each role binds one
value. Finite enumerable sources and unique type solutions are mandatory;
relationship cycles are not computed-domain fixed points. Binding identity
deduplicates repeated assignments, with no implicit inequality between roles.
Equality-dependent value participants retain MUD-TYPE-040's exclusions.

Let B(W) be the admitted binding set supplied for checkpoint view W, and C_b the
declaring environment under one b in B(W). Require
`C_b |- condition <= Bool [1] |> (epsilon,O)` under Expression permissions.
All domain, shape, purity, call and termination obligations remain required.
Inner capability cannot authorize a write from this pure mode. Boolean-body
locals have the ordinary immutable sequential scope; no forward references,
assignment, shadowing or persistent invariant storage is introduced.

Every condition and transitive query uses one coherent checkpoint view. Pure
look/sublook and Boolean calls may read that view without becoming effects.
Direct stochastic calculation/derived stochastic reads are invalid; valid
ordinary stored values remain readable. Imagine/eventually require their own
admitted isolated/reachability profiles and do not grant world effects.
Old/changes have no general always-condition context: causal observation of
the declaration is separate from inserting temporal operators into its Bool body.

## Checkpoint interface and outcomes

> [!rule] MUD-ALWAYS-002 — Validate each consolidated checkpoint
> Every effective always binding must complete normally with true after the
> consolidated root and after each consolidated wave. False produces
> AlwaysRefusal; a computing Fault produces Error occurrences. A later wave
> cannot repair an already failed checkpoint.

The successful-check predicate for W is that each b in B(W) produces Normal(true).
This is an interface requirement on supplied consolidated views, not a causal
scheduler or discovery algorithm. Checking a sibling private prefix instead of
the consolidated view does not satisfy it. Checkpoint failure uses the enclosing
resolution's refusal/error and rollback contract; it is not automatically a
recoverable Error merely because the invariant is false.

AlwaysRefusal retains mandatory reason and origin identifying the always
declaration, plus its BoolCheck condition record. A successfully false condition
has root BoolCheck.value false; child checks preserve actual short circuit and
unevaluated branches without reevaluating them. The trace records the final
condition's expression structure; earlier local definitions and called query
internals are not expanded into a general execution log. Capture the diagnostic
before rollback and retain it as immutable data.

Computing failures, invalid writes/domains and effect conflicts retain their
Error contracts. A handler can recover a computing fault to the required Bool
without gaining authority; if it recovers false, the invariant still refuses.
Text-only false diagnostics and Refusal on bindings are invalid. There is no
missing-otherwise warning, no implicit false-to-Error conversion and no finally.
The exhaustive error subtype/technical-defect boundary remains
[[../notes/questions/Q-007-f-technical-failures|Q-007]].

## Activity and dependencies

The canonical declaration has explicit lifecycle activity and hard-dependency
suspension. An inactive/suspended always has no current effective check, while
its definition, signature and metadata remain canonical. Restoring its
dependencies/activation restores the obligation: a violating candidate cannot
be published merely because the rule was unavailable before restoration.
Create/destroy operates on the rule definition, not individual bindings.

Dependency summaries include participant/source/domain reads, calculated locals
and transitive queries. Caches may only preserve the same complete view,
availability, inputs, error and dependency observations; they cannot suppress
a required checkpoint. Pure admission alone does not prove no causal cycles
or define dynamic-call impact.

## Causal-source contract and excluded algorithm

An always declaration can be referenced without `()` as a causal source.
It contributes an evaluation occurrence for its relevant binding/wave, separate
from the truth value of its condition. It is not a Boolean call or a shorthand
failure event. Tooling must warn about the established risk of useless causality
or lack of stabilization when using this source.

Match identity and payload/binding flow obey the same trigger interface as other
admitted declarative sources. Source occurrence delivery, attribution, readiness,
completion and rollback-scope ownership are supplied by the causal algorithm,
still [[../notes/questions/Q-072-causal-work-and-reality-completion-algorithm|Q-072]].
Oscillation/wave-limit policy remains
[[../notes/questions/Q-020-o-oscillations-and-wave-limit|Q-020]]. Static impact follows [[types/contextual-call-analysis]];
finite/termination procedures remain Q-028/Q-029. These boundaries
do not permit arbitrary checkpoints, guessed scheduling or relaxed static proofs.

## Counterexamples and conformance evidence

An always body containing `account.balance = 0` is invalid even if intended to
repair its own condition. False cannot be caught with otherwise as Refusal.
Adding when/then or given changes the declaration into no accepted rule variant.
A false root invariant cannot wait for a later reactive rule to repair it.
Observing Nonnegative as a trigger does not mean “Nonnegative failed”.

[[types/typing-cases.yaml]], AST variant/handler coverage and [[effects/README]]
record purity, Error versus Refusal, binding and checkpoint examples. Shared
Normal/Fault and diagnostics follow [[20-blocks-and-recovery]] and
[[21-expressions]]. No causal algorithm, runtime invariant engine, host protocol
or new nominal HIR memory/effect field is implemented here.
