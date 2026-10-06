---
id: D-043
title: Speculative query with `imagine`
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-007"
  - "Q-032"
  - "Q-035"
  - "Q-053"
affects:
  - "expressions, actions and admissibility analysis"
---

# ADR-043 — Speculative query with `imagine`

- Amended by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]], [[ADR-110-tentative-wave-journal-and-atomic-confirmation|D-110]] and [[ADR-119-invocation-owned-completion-and-imagine|D-119]].

## Decision

Imagine call evaluates an admissible action under the complete real invocation protocol in a disposable isolated projection. It returns ActionReply with Success, Refusal or nonempty Errors, never an implicit Bool. The operand retains ordinary binding and outer-capability requirements. Every root/wave checkpoint and invocation-owned after uses the same semantics as real execution.

The speculative journal is always discarded, including after Success. No real world, queues, logs, randomness consumption, resolution identity or host delivery changes. Random branches have stable semantic identity and do not consume a real invocation's branch. Mutable receiver places resolve to speculative storage. Foreign calls require isolation; irreversible delivery cannot occur in imagination.

Imagine is available in pure reading contexts; its reply is inspected with ordinary types/narrowing. The admissibility dependency graph is acyclic. Resource limits or executor defects cannot silently yield Refusal or false. Q-007 retains that external failure boundary; Q-032 retains cache/retry rules and stochastic-result exposure; Q-035 retains speculative budgets, memoization and diagnostics.

```mud
reply: ActionReply = imagine (source, destination).Transfer(amount)
permitted := reply is Success
```

## Verification

Check all reply alternatives, real/speculative trace correspondence under the same branch, no observable effects or randomness consumption, isolated mutable places and static rejection of admissibility cycles.
