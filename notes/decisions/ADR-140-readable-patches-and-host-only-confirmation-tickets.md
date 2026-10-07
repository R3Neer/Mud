---
id: D-140
title: Readable patches and host-only confirmation tickets
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions:
  - Q-072
  - Q-073
  - Q-074
affects:
  - Mathematical model, reply contracts, effects, messages and architecture
  - Patch representation, host observations and reproduction
---

# ADR-140 — Readable patches and host-only confirmation tickets

## Context

The author confirms automatic patch incorporation and intends a readable textual result rather than an executable representation or mandatory disk file. Tickets remain exclusively host-facing. This amends D-110, D-118, D-127 and D-133 while retaining ActionReply as the sole action result and existing message delivery guarantees.

## Decision

A successful action's incorporated changes must be obtainable as a readable, serialisable textual Mud patch. Incorporation is automatic at the appropriate relative frontier; obtaining/returning a patch does not apply its contribution again and does not require host approval. A child incorporation stays provisional with respect to containing levels and the stable root.

No patch syntax, format version, source Patch type, Success component or accessor is selected. Success is already a nominal alias; the patch-access interface and exact reply representation remain Q-073. This requirement is not an additional user-defined action domain result and does not permit action-specific return types.

Prepare exterior effect intentions provisionally; ordinary irreversible application must wait until their originating containing work is confirmed into the stable root, unless an explicit transactional adapter contract provides the agreed alternative guarantees. A textual patch does not make arbitrary exterior effects reversible or their delivery atomic with world confirmation. Native execution can fail after world confirmation; its observable result/recovery protocol remains open.

Generalise Ticket as a host-facing confirmation concept for provisional observations. Existing message tickets retain Waiting/Kept/Dropped, permanent terminal states, scope disposal, publication barriers and race-free observation. Relative inner confirmation leaves Waiting. Kept requires surviving incorporation into the stable root, with confirmed state available first; containing disposal produces Dropped. The host cannot mutate tentative state or cancel an invocation through Ticket. Tickets are not a new Mud source value/type or syntax.

The exact additional ticket-bearing objects, identities, provisional patch-view API and lifetimes remain Q-074. The existing message envelope is the concrete specified instance. Imagine/test branches do not publish speculative host outputs. Kept reports confirmation, not successful material execution of an exterior operation.

## Deferred design and alternatives

A textual format should have an explicit semantic structure, but that structure is not the compiler's IR and need not be stored as a physical file for every call. Recorded transition application and re-executing the original programme are different guarantees. Future libraries may inspect/apply patches only under a validated contract; field-value maps alone do not settle concurrent transforms, read dependencies, generations or joint contributions.

Recording options, retention, access and configuration are not selected. No runtime/recording TOML tables are approved. Formalise causal execution first (Q-072), then patches/reproduction (Q-073), coordinating the ticket boundary (Q-074). Host-decided incorporation and arbitrary automatic replay of exterior effects are not chosen.

## Verification obligations

Reading a returned child patch does not duplicate parent changes. Parent disposal discards relatively incorporated child work and drops associated pending message tickets. Stable-root confirmation precedes Kept. An exterior delivery result must not be equated to ticket state. These obligations do not supply an executable patch merger or adapter protocol.
