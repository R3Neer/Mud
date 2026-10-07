---
id: Q-074
title: Generalised host tickets and exterior intentions
priority: P1
opened: 2026-10-07
resolved:
closed:
decisions:
  - D-140
affects:
  - Host observations, patch views, adapter intentions and delivery results
superseded-by: []
---

# Q-074 — Generalised host tickets and exterior intentions

## Already decided

Tickets are host-only. Existing message publication and Waiting/Kept/Dropped contracts remain specified; inner relative confirmation leaves Waiting and surviving stable-root incorporation makes Kept. Scope disposal drops provisional observations. Ticket state is not delivery success or cancellation authority.

## Pending

Select the additional ticket-bearing objects and define identity, observation scope, provisional patch/intention payload, lifetime, subscription/retention and adapter API. Define how preparation/confirmed delivery/execution results interact with transactional adapters and failures after stable-root confirmation. Runtime/recording defaults are not chosen.

Q-072 defines levels and completion; Q-073 defines patches. Q-069/Q-070 retain native ABI, conversions and resource protocols. Q-067 remains closed for its original message-delivery scope; this question extends that boundary rather than reopening accepted payload semantics.

## Closure criteria

- C1: Define extra observation objects, identities, scope provenance and read-only exposure without leaking writable tentative handles or publishing imagine/test branches.
- C2: Define relative/stable-root state transitions and race-free observation, including nested failure, recovery and lifetime after disposal.
- C3: Define prepared exterior intentions and their execution-result/error contract, distinguishing confirmation from successful delivery and delimiting transactional guarantees.
- C4: Provide reviewed traces for provisional patch observation, duplicate/reconnected subscriptions, nested incorporation/disposal and delivery failure after confirmation.
