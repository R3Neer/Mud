---
id: D-133
title: "Provisional messages and scope-aware tickets"
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions:
  - Q-067
affects:
  - "[[specification/04-mathematical-model]]"
  - "[[specification/07-concrete-grammar]]"
  - "[[specification/19-expressions]]"
  - "[[specification/25-effects]]"
  - Message payload, host boundary, rollback and adapter obligations
---

# ADR-133 — Provisional messages and scope-aware tickets

## Context

The author rejects waiting for final resolution or final-payload-equality filtering: long causal resolutions should permit responsive host behaviour. A cancellable, eventually confirmable occurrence preserves isolation. Accepted names are Ticket and Waiting/Kept/Dropped. This amends D-042, D-045, D-096, D-110 and D-119.

## Decision

A message/submessage occurrence is born when its `when` matches and its `if`, if present, is true. Its public fields are evaluated and frozen as one immutable payload in that causal view. The internal and external observations share that payload and occurrence identity. Later field changes, participant destruction or recreation neither reproject the payload nor suppress it by final-state equality. Participants in `on` remain canonical identity descriptors; their later inactivity does not invalidate the event or grant a host mutable world handle.

A shared normal `message` is provisionally delivered after the producing wave is consolidated and its mandatory always/domain/cardinality checkpoints succeed. No sibling private prefix or failed checkpoint is published. Internal causal consumers still see the occurrence in the next wave. A `submessage`, a declaration in a `part only` file, an isolated test or `imagine` has no external delivery. A root-produced occurrence passes the analogous root consolidation/checkpoint barrier. Publication does not confirm tentative world state, and host `look` continues to read confirmed state.

The host envelope keeps declaration/occurrence identity, `on` bindings, immutable payload and `ticket` separate. A `Ticket` is a read-only host-facing occurrence handle whose `state` is `Waiting`, `Kept` or `Dropped`. It is not a Mud thing, a writable participant, a new keyword or a user-constructible source type. It has no new nominal anchor. Its occurrence identity is distinct even when another message has the same payload. Concrete ABI and native representation follow the adapter contracts.

Every published ticket starts Waiting. It transitions once to Kept when the real outer resolution commits and its producing rollback scope survives, or to Dropped when that scope or an enclosing scope is discarded. Both terminal states are permanent. Successful child completion leaves Waiting until outer confirmation. Later caller changes do not recheck the child's after or invalidate historical payload values. A child's refusal/error drops its attempted occurrences and causal descendants. Outer refusal/error drops all surviving pending tickets. For jointly caused work the owner is the nearest common enclosing invocation; an entire physical wave does not acquire a single owner.

Block rollback is part of ticket provenance. A failed protected block drops its occurrences even if `otherwise` recovers and the outer action succeeds. Handler occurrences belong to their new surviving scope and get new tickets. An occurrence discarded before its publication barrier emits no provisional host notification. Payload-evaluation errors enter the ordinary error channel; they do not create a successfully published occurrence with a partially calculated payload.

The host can read current ticket state and subscribe to terminal updates. Subscription registration and its initial current-state observation must be serialised with state transitions so that a host cannot miss completion between reading Waiting and registering. Local observation and remote occurrence-identity notifications obey this same contract; transport replay/reconnection protocols are adapter details. The host cannot set ticket state or cancel a Mud resolution through this handle. Kept is observable only after the confirmed state is available.

Waiting permits speculative host responses with cancellation/compensation; irreversible external effects require Kept or an explicit transactional adapter contract. Dropped does not undo arbitrary I/O, sound or already displayed frames. Ticket observation is not permission to read tentative storage. Published frozen payloads and terminal ticket state remain readable as historical evidence after rollback; private writable handles and failed foreign exports do not escape.

Publication preserves causal order across wave barriers. A reproducible technical order within a wave does not give semantic priority to equal-time occurrences. Tickets report validity of the recorded causal occurrence, not whether its payload still equals current state. Unbounded resolution duration or nontermination may leave Waiting pending; timeout/oscillation policy is separate from inventing Kept or Dropped.

## Consequences and verification

No source keyword, new Mud type constructor or nominal HIR field is needed for the host envelope. Runtime scope/occurrence provenance supplies the ticket, independently of nominal anchors. This is a semantic API contract, not an implemented transport. Q-069/Q-070 retain concrete native hosting, representation, reconnection and lifetime protocols. Declarative conformance traces in specification/effects/message-delivery-cases.json cover the accepted edge cases without claiming a scheduler implementation.
