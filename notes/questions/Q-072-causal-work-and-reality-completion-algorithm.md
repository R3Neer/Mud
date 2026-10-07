---
id: Q-072
title: Causal work and reality completion algorithm
priority: P0
opened: 2026-10-07
resolved:
closed:
decisions:
  - D-139
affects:
  - State/evaluation, action requests, roots, waves, completion and rollback
superseded-by: []
---

# Q-072 — Causal work and reality completion algorithm

## Already decided

D-139 fixes levels versus branches, stable-root visibility, relative child confirmation and automatic incorporation. Invocation instances own causal work rather than waves. Existing joint provenance/common enclosing owner, per-invocation after and consolidation checkpoints remain constraints.

## Pending

Define the abstract state and algorithm rather than an informal notion of exhausted waves. Attribute when matches through derived reads, Boolean transitions, changes, binding episodes and joined occurrences. Register descendants before declaring their predecessor complete. Account for calls, messages, suspended native work, continuations and pending discovery barriers. Distinguish provenance from responsibility for completion.

Define relative level incorporation, disposal, scheduling/readiness and observation views, then establish completion and recovery/cancellation behaviour. Exterior-root concurrency and asynchronous source syntax are not implicitly authorised. Coordinate resource safeguards and oscillations with Q-007/Q-020, dynamically selected calls with Q-023 and native hosting with Q-069/Q-070.

## Closure criteria

- C1: Define all state components and transition inputs/outputs, including levels, branches, invocation identities, ownership, observation memory and waits.
- C2: Provide causal attribution rules and pseudocode for discovery, conjunction/disjunction, zero-net changes, episode baselines and joint provenance without guessing from wave membership.
- C3: Define complete advance/consolidation/completion/incorporation/disposal algorithms, with no interval that loses newly generated work and no reliance on global quiescence for unrelated invocations.
- C4: Specify blocking calls, exterior waits, protected recovery and technical interruption boundaries, explicitly delimiting unsupported concurrency.
- C5: Supply reviewed traces for independent owners, joint consequences, multistep reactions, pending I/O, child success/parent rollback, imagine, failed checkpoints and non-state causal cycles. State validation limits; a diagram alone is not closure.
