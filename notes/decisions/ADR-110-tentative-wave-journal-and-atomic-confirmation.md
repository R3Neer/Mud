---
id: D-110
title: "Tentative wave journal and atomic confirmation"
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - Q-002
  - Q-035
affects:
  - "Tentative state, reference runtime, waves, consolidation, after, allowed and causal outputs"
---

# ADR-110 — Tentative wave journal and atomic confirmation

- Amended by: [[ADR-118-action-replies-refusals-and-errors|D-118]].

- Develops: [[ADR-042-shares-root-and-results|D-042]] and [[ADR-043-speculative-query-with-allowed|D-043]].
- Preserves the consolidation algebra of [[ADR-046-algebra-and-conflicts-of-effects|D-046]], [[ADR-060-additive-deltas-and-nat-normalisation|D-060]] and [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]], and internal-call sequencing of [[ADR-096-modules-callables-look-message-and-activation|D-096]].
- Complements the foreign transaction boundary of [[ADR-109-foreign-language-blocks-and-value-exports|D-109]].

## Decision

The reference runtime will use a tentative journal, with private sequential deltas before consolidation and consolidated patches/snapshots for each wave. The Git-patch analogy describes keeping changes isolated and disposable; it does not introduce textual merges, repository operations or an implementation-independent serialised patch format.

Within one `then`, statements and internal calls observe prior authorised private effects at their textual positions. Concurrent siblings start from the common wave projection, without reading one another's partial deltas. Consolidation uses the existing semantic algebra and detects conflicts. Consolidated effects update only the resolution's tentative projection, which subsequent waves may observe; they never prematurely update confirmed world storage.

After the complete resolution stabilises, all applicable invariants and the `after` clauses of every executed action/subaction must pass. The successful final checks produce the final transition record, and the resulting transition is then confirmed atomically. A rejected or failed resolution discards its entire journal and tentative outputs, including earlier waves. Completion of one wave or one nested action is not a commit boundary. `old` retains its existing contextual snapshot meaning.

`allowed` uses the same complete semantic resolution protocol on an isolated speculative projection and always discards the journal, including on acceptance. `Success` maps to `true`, `Refusal` to `false`, and `Errors` propagates. It does not consume real randomness, resolution identities, confirmed queues, logs or host message delivery. Foreign calls within speculation require the same pure/transactional isolation guarantees; native irreversible I/O cannot be undone by a journal.

Tentative message occurrences may participate in causal triggers in later waves, but external delivery occurs only after a real commit. Debugging may retain an explicitly separate diagnostic trace without publishing speculative events as confirmed world activity.

## Non-decisions

This does not complete the operational semantics of every effect family (Q-002) or specify memoisation, budgets and diagnostics for `allowed` (Q-035). Journal representation, in-memory overlays, persistence, compression and resource management are reference-runtime implementation choices. No future semantic IR or nominal-HIR fields are introduced.

## Verification scenarios

1. Two concurrent `+= 3` and `+= 4` deltas from `10` consolidate to `17`, rather than last-writer `13`/`14` or a textual conflict.
2. A subsequent wave reads consolidated tentative changes while the confirmed world retains its initial state.
3. A false final `after` or a failed invariant discards all prior waves and cancels external messages.
4. A nested action's successful effects remain tentative until every executed action's final postcondition succeeds.
5. Successful `allowed` returns true with no world/queue/randomness change; rejection returns false, technical failure propagates.
6. Sequential versus concurrent structural effects retain their existing distinct algebra; recording patches cannot introduce an arbitrary merge order.
7. Foreign transactional writes are discarded on failure/speculation; irreversible native side effects are rejected without an appropriate delivery/transaction contract.
