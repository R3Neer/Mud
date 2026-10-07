---
id: D-110
title: "Tentative wave journal and atomic confirmation"
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - Q-072
  - Q-073
  - Q-002
  - Q-035
affects:
  - "Tentative state, reference runtime, waves, consolidation, after, imagine and causal outputs"
---

# ADR-110 — Tentative wave journal and atomic confirmation

- Formalised/amended by: [[ADR-128-sequential-effects-and-staged-consolidation|D-128]].

- Amended by: [[ADR-119-invocation-owned-completion-and-imagine|D-119]].

- Amended by: [[ADR-118-action-replies-refusals-and-errors|D-118]].

- Develops: [[ADR-042-shares-root-and-results|D-042]] and [[ADR-043-speculative-query-with-allowed|D-043]].
- Preserves the consolidation algebra of [[ADR-046-algebra-and-conflicts-of-effects|D-046]], [[ADR-060-additive-deltas-and-nat-normalisation|D-060]] and [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]], and internal-call sequencing of [[ADR-096-modules-callables-look-message-and-activation|D-096]].
- Complements the foreign transaction boundary of [[ADR-109-foreign-language-blocks-and-value-exports|D-109]].

- Amended by: [[ADR-133-provisional-messages-and-scope-aware-tickets|D-133]].

- Amended by: [[ADR-139-reality-levels-branches-and-relative-confirmation|D-139]].

- Amended by: [[ADR-140-readable-patches-and-host-only-confirmation-tickets|D-140]].

## Decision

The reference runtime will use a tentative journal, with private sequential deltas before consolidation and consolidated patches/snapshots for each wave. The Git-patch analogy describes keeping changes isolated and disposable; it does not introduce textual merges, repository operations or a selected serialised patch format. D-140 requires readable textual patches of incorporated work; schema and reply access remain Q-073, independently of private journal layout.

Within one `then`, statements and internal calls observe prior authorised private effects at their textual positions. Concurrent siblings start from the common wave projection, without reading one another's partial deltas. Consolidation uses the existing semantic algebra and detects conflicts. Consolidated effects update only the resolution's tentative projection, which subsequent waves may observe; they never prematurely update confirmed world storage.

Each invocation runs after once its own causal work stabilizes, before its caller resumes. Shared causes belong to the common enclosing invocation. Completed children are not rechecked. The outer resolution commits once its work, checkpoints and after succeed; nested completion is relative confirmation with automatic incorporation into the containing level, not independent stable-root confirmation. Containing disposal still discards incorporated work; Q-072 retains the full algorithm. Non-success scopes discard tentative effects and pending occurrences and drop already published tickets under reply/recovery rules. Old retains its contextual entry/snapshot meaning.

`imagine` uses the same complete semantic resolution protocol in an isolated alternative branch and always discards the journal, including on acceptance. It returns ActionReply unchanged, with no implicit Boolean conversion. It does not consume real randomness, resolution identities, confirmed queues, logs or host message delivery. Foreign calls within speculation require the same pure/transactional isolation guarantees; native irreversible I/O cannot be undone by a journal.

Tentative message occurrences participate in later causal waves. Shared normal messages publish a frozen payload with Waiting after validated consolidation; real commit makes surviving tickets Kept, and scope rollback makes affected tickets Dropped. These callbacks do not expose tentative storage or publish confirmed world activity. Debugging may retain an explicitly separate diagnostic trace without publishing speculative events as confirmed world activity.

## Non-decisions

Chapter 28 defines operational effect-family and finite batch contracts. This journal decision does not specify memoisation, budgets and diagnostics for imagine (Q-035). Journal representation, in-memory overlays, persistence, compression and resource management are reference-runtime implementation choices. No future semantic IR or nominal-HIR fields are introduced.

## Verification scenarios

1. Two concurrent `+= 3` and `+= 4` deltas from `10` consolidate to `17`, rather than last-writer `13`/`14` or a textual conflict.
2. A subsequent wave reads consolidated tentative changes while the confirmed world retains its initial state.
3. A false final `after` or a failed invariant discards all prior waves and drops published affected tickets.
4. A nested action's successful effects remain tentative until the outer invocation completes its own postcondition and commit.
5. Imagine returns Success, Refusal or Errors without world/queue/randomness changes.
6. Sequential versus concurrent structural effects retain their existing distinct algebra; recording patches cannot introduce an arbitrary merge order.
7. Foreign transactional writes are discarded on failure/speculation; irreversible native side effects are rejected without an appropriate delivery/transaction contract.
