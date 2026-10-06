---
id: D-119
title: Invocation-owned completion and imagine
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - Q-002
  - Q-035
  - Q-059
affects:
  - Language contracts and their developed normative surfaces
---

# ADR-119 — Invocation-owned completion and imagine

## Context

The author chooses invocation-owned stabilization, each invocation's own after before returning to its caller, and imagine as a speculative ActionReply expression. This amends D-009, D-042, D-043, D-096 and D-110.

## Decision

Every action/subaction invocation has a distinct internal causal owner within the one outer resolution. Its effects, message occurrences and reactive firings retain causal provenance. Consequences with one initiating owner belong to that invocation; a consequence jointly caused by different invocations belongs to their nearest common enclosing invocation. Ownership is by contribution/occurrence, not by assigning an entire physical wave to one action. Joint causes are retained, not replaced by a randomly chosen owner. These are execution identities, not new world things or public anchors.

An invocation finishes its then and stabilizes the causal work it owns. After no owned pending consequence remains, its after is evaluated once against that completion projection, before the caller continues. A completed child's after is not rechecked after later caller effects. Work jointly owned by an enclosing invocation waits for that owner's completion. No invocation waits for work whose cause is a caller statement that has not run yet.

Normal waves still consolidate compatible concurrent contributions over common views before checkpoints. Ownership neither serializes sibling contributions by source order nor allows reading their private deltas. Concurrent invocation continuations cross the applicable consolidation/completion barrier; after sees a consolidated completion projection, not a sibling's partially executed body. Always is checked after each consolidated root/wave. Its false condition refuses that attempted transition even if a later wave could repair it.

Nested completion is not a commit. Success retains the child's tentative effects for the caller, and outer confirmation occurs only after the outer invocation's causal work, checkpoints and after succeed. A child's non-success attempt rolls back its contribution scope before returning a reply; causal descendants and attempted outputs are included. A non-success outer request discards the entire resolution.

ActionReply is an ordinary value. Real action calls are admitted only in an effect-capable context, including a local value initializer evaluated by an effect block, subject to ordinary permissions. A pure expression/value computation cannot execute a real action by hiding it in a nested initializer. Explicitly obtaining a reply as a value permits observation of Success, Refusal or Errors after the attempted child scope has been settled/rolled back. An invocation used solely as an effect statement propagates non-success: Refusal aborts the current attempt, and Errors enter its enclosing block's error channel. Constructing or passing an Error value alone does not raise it. This distinguishes explicit result observation from silently ignoring failed effects; comprehensive test aggregation remains Q-059.

```mud
then {
    reply: ActionReply = actor.Move()
    # the reply can be passed to an ordinary rule/action contract
}
```

Imagine executes the same complete invocation, consolidation, checkpoint and after protocol in a disposable isolated projection and returns ActionReply, without converting it to Bool or propagating an Errors alternative merely because it is returned. It always discards tentative world writes, occurrence queues, real randomness consumption, resolution identities, logs and external delivery. Pure contexts can use imagine and then inspect its reply through ordinary types/narrowing. Static admissibility cycles remain invalid. Foreign operations used under imagination need checked/trusted isolation contracts and cannot publish irreversible effects.

```mud
reply: ActionReply = imagine actor.Move()
canMove := reply is Success
```

Imagine uses the existing prefix-operator precedence and root-capability checking of its operand; it is not a general sandbox for arbitrary effect statements. The word allowed is an ordinary identifier, not the speculative keyword. Cost/memoization/resource behavior remains Q-035 and cannot silently turn inability to evaluate into Refusal.

## Verification

A child's after sees its own stabilized work and runs before a subsequent parent write; that later write does not rerun the child's after. Joint causes belong to the common enclosing invocation. Completed child Success stays tentative until outer success; refusal or unhandled errors discard applicable scopes. Explicit reply capture remains inspectable, while a bare failed effect call propagates. Imagine returns each ActionReply alternative without publishing changes or consuming real randomness.

## Integration review

The mathematical, grammar, lexical and AST surfaces use ImagineQuery and invocation-owned completion. Existing CallExpr preserves written action calls; context typing admits/rejects real execution without new Surface AST effect classifications. Causal ownership is dynamic semantic data, not nominal HIR. The names chapter preserves operation anchors and ordinary reply locals. Planned dynamic chapters retain interim authority here.
