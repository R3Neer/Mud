---
title: Causal runtime formalisation work plan
status: analysis
tags:
  - mud/analysis
  - mud/runtime
---

# Causal runtime formalisation work plan

## Accepted foundation and scope

[[decisions/ADR-139-reality-levels-branches-and-relative-confirmation|D-139]] fixes relative levels, alternative branches and the stable exterior root. [[questions/Q-072-causal-work-and-reality-completion-algorithm|Q-072]] retains the full operational algorithm. This note is a review plan, not an implemented scheduler or a closed transition system.

The specification drafting order uses vertical cycles, not strict chapter numbering. After static contracts and chapter 25 effects, the relevant work is state/evaluation (26), requests/results (27), roots (28), waves (29), constraints/old (30) and conflicts/stabilisation (31). Develop these together in reviewable units. D-013 still requires complete formalisation before implementation; prototypes cannot decide language semantics by accident. Semantic IR layout, ABI, threads and asynchronous source syntax are separate choices.

## Review sequence

1. Abstract state: stable/provisional views, levels, branches, invocations, protected scopes, pending work and observation memory.
2. Work creation and causal attribution: calls, when matches, messages, derived reads, continuations and joint causes.
3. Wave advancement: readiness, suspension, common snapshots, consolidation and discovery barriers.
4. Completion: after, automatic relative incorporation, parent disposal and stable-root confirmation.
5. Exterior waits: adapter results, lifetime, cancellation/error and technical interruption contracts.
6. Complete pseudocode, auxiliary procedures, invariants and reviewed conformance traces.

Review each unit with the author before dependent choices. A top-level loop with undefined attribution/completion helpers does not constitute a complete algorithm. Textual patches follow this operational foundation; ticket frontiers are coordinated with it.

## Candidate bookkeeping — not an accepted state representation

A unit of work could carry identity, status, invocation responsible for completion, full causal provenance, containing level/branch/scope, dependencies and pending barriers. A proposal tests completion using finished then, no assigned pending work and no undiscovered consequence/checkpoint. Suspended work remains pending even when absent from a wave. Descendant registration and predecessor retirement must not permit premature completion.

Wave owner sets may assist consolidation and traces. Waiting for every owner of every historically shared wave can couple unrelated work: A recolours a flower and B waits for independent network work; shared participation gives no reason to delay A. This is a counterexample to that proposal, not a silently substituted algorithm.

Attribution needs explicit rules for consulted derived dependencies, net changes, transition observations, joined message/firing matches and lifecycle observation episodes. In particular, temporal history cannot cause perpetual waits on historical invocations. Existing changes semantics and initial/resumed baselines are preserved.

## Required contrasting traces

- A completes while unrelated B continues, despite a shared earlier wave.
- A remains pending while its exterior request has no executable wave contribution.
- A change creates a reaction which creates another reaction before completion.
- Joined causes ascend to the common enclosing frontier and are not counted/applied twice.
- Child confirmation is followed by parent refusal/error and complete containing-level disposal.
- Imagine returns relative Success but no host delivery or stable writes.
- Opposing effects leave no net changes pulse; direct occurrences retain multiplicity.
- Recovery drops protected work/tickets and registers distinct surviving handler work.
- Checkpoint false refuses immediately, while computing faults and resource interruptions remain distinct.
- A message-only causal cycle cannot be mistaken for quiescence because world fields stopped changing.

## Deferred questions

A syntax for asynchronous initiation, detached work, joins/handles and concurrent exterior roots is not chosen. The current single exterior-resolution queue remains the supported boundary. The physical runtime may optimise an abstract algorithm but cannot change views, checkpoints, randomness, ownership or results.
