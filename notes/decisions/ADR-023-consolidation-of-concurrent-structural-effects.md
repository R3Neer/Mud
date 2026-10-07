---
id: D-023
title: "Consolidation of concurrent structural effects"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-002"
  - "Q-006"
  - "Q-021"
  - "Q-046"
affects:
  - "future chapters 25, 28, 29 and 31"
---
# ADR-023 — Consolidation of concurrent structural effects

- Formalised/amended by: [[ADR-128-sequential-effects-and-staged-consolidation|D-128]].

- Amended by: [[ADR-125-instruction-local-lifecycle-no-ops|D-125]].

- Updated: 28 July 2026 to use the terminology from D-025
- Amended by: [[notes/decisions/ADR-066-static-values-and-local-bindings-in-then|D-066]]
- Amended by: [[ADR-096-modules-callables-look-message-and-activation|D-096]].
- Related to: [[notes/decisions/ADR-054-canonical-definitions-and-initial-activation|D-054]]
- Related questions: [[notes/questions/Q-002-m-exact-model-of-sequential-and-simultaneous-effects|Q-002]], [[notes/questions/Q-006-c-conflicts|Q-006]], [[notes/questions/Q-021-a-static-conflict-analysis|Q-021]], [[notes/questions/Q-046-c-ineffective-creation-inside-a-root|Q-046]]
- Documents affected: future chapters 25, 28, 29 and 31
- Amended by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].

- Clarified by: [[ADR-111-static-thing-field-schema|D-111]].

- Amended by: [[ADR-137-live-locals-stored-inference-and-binding-patterns|D-137]].

## Context

Several rules may be requested in the same batch:

- The activation of the same `thing` by means of `create`.
- The activation of the same rule.
- Incompatible activations and destructions.
- Additions and removals to the same collection.

It is not always possible to determine statically whether two rules will take effect in the same wave. The semantics nor can it depend on the actual order in which threads or internal structures traverse the `then`.

At the same time, the written instructions contained within a single `then` they must retain their sequence.

## Decision: two levels of assessment

Be $W_i$ the snapshot common feature of a root or a wave, and these are:

$$
t_1,\ldots,t_n
$$

the blocks `then` applicable.

Every $t_j$ is interpreted sequentially on a private overlay:

$$
\Delta_j
$$

which begins on $W_i$. A subsequent instruction from the same `then` You can see the previous effects of that block.

None `then` notes that during the same wave, the delta part of another `then`. The implementation may interleave or parallelise the computation, but this scheduling is not observable.

A local binding `name [derived-form] := value-body` registers a live derivation without storage. Its reads use the applicable private view, including preceding effects; stored `=` locals instead capture once. Neither declaration alone produces a world delta.

Once all the blocks have been completed, each one is normalised delta private and are then consolidated:

$$
\operatorname{merge}_{W_i}
(\Delta_1,\ldots,\Delta_n)
$$

The consolidation produces a single delta attempt or a conflict which causes the resolution.

## Structural order between blocks

After respecting and normalising the internal order of each `then`, the structural effects of different blocks are consolidated in the following order:

1. Activations `create` survivors.
2. Surviving collection-value additions.
3. Surviving collection-value removals.
4. Surviving ruins.

Therefore, if a `then` requests `create A` and another asks `destroy A`, the result consolidated leaves `A` destroyed.

Within a single block, the written order still prevails:

```mud
then {
    create A
    destroy A
}
```

ends with a request destruction site.

```mud
then {
    destroy A
    create A
}
```

ends with a request premises of activation. Local normalisation must preserve any effect observable interval within the block itself before calculating its state end.

This rule does not introduce a hidden temporal priority between rules: it defines an operation of consolidation declarative regarding their deltas.

## Several activations of the same declaration

Every `thing` and the rule has only one canonical definition top-class; every appearance `create d` is a benchmark for activation to the same descriptor. Aliases are excluded from the activation.

Several concurrent requests are idempotently merged:

$$
\{
\operatorname{create}(d),
\ldots,
\operatorname{create}(d)
\}
\rightsquigarrow
\operatorname{create}(d)
$$

Two complete definitions are a static error, even if their bodies are identical. A create targeting an explicitly active declaration is a no-op for that instruction only. Other effects of its rule or action still execute; mixed availability is evaluated against each branch's current private view.

## Temporary validity

Consolidated capitalisations and write-offs result in the effective projection from $W_{i+1}$. They do not alter matters retrospectively:

- The snapshot read by the `then` of the current wave.
- The bindings secured at the start of that wave.
- The previous memory used by `when` during that wave.

The new rules and suspensions affect the construction of bindings and the assessment of the next wave.

## Implications for analysis and runtime

- The compiler can use conservative analysis without having to resolve every dynamic match.
- The runtime needs to group requests by identity and type of effect.
- Every activation must be retained provenance to explain the reason for it.
- Local sequentiality can be implemented using overlays without publishing partial states.
- The outline causal It must specify which idempotent requests were consolidated.
- A conflict Structural dynamic does not produce a commit or state partial.

## Formalisation boundary

Lifecycle no-ops and mixed availability are specified by D-125. Static overlap/cardinality proof boundaries are specified in chapter 14. Chapter 25 specifies semantic destinations, sequential private effects and finite root/wave composition, including surviving internal-call contributions. Complete scheduler and native-hosting implementations remain separate work.

## Future verification

The suite must cover:

1. Static rejection of two definitions of the same thing `thing` or ruler.
2. Consolidation idempotent with respect to multiple invocations of the same missing definition.
3. Creation and destruction from different blocks, with final destruction.
4. Reverse order within a single `then`.
5. Effects only visible in the next wave.

