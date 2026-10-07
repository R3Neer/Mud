---
id: D-139
title: Reality levels, branches and relative confirmation
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions:
  - Q-072
affects:
  - "[[specification/04-mathematical-model]]"
  - "[[specification/07-concrete-grammar]]"
  - "[[specification/25-effects]]"
  - Dynamic chapter remits, invocation completion and architecture
---

# ADR-139 — Reality levels, branches and relative confirmation

## Context

The author distinguishes nested reality levels from alternative branches. A child may succeed relative to its level before its containing action reaches the stable exterior world. This amends the wording of D-042, D-110 and D-119 without introducing an asynchronous source construct.

## Decision

The reality root is the stable world observed by exterior consumers. Execution develops provisional levels; nested action invocations have relative confirmation frontiers. A successful child incorporates its contribution automatically into its caller's containing level. Success denotes confirmation relative to that frontier, not independent confirmation of the exterior root. Discarding a containing level discards incorporated child work without making the earlier relative result incorrect.

Alternative branches distinguish hypothetical evolution from nested confirmation. Imagine executes in an isolated disposable branch and returns the ordinary ActionReply, including relative Success, to its caller; its work never reaches the stable root. Levels and branches do not prescribe full physical world copies.

Waves belong to a reality and may combine contributions from several invocation instances. Actions own causal work, not complete physical waves. Repeated calls of one action have distinct invocation identities. Existing causal provenance, joint-work ownership by the nearest common enclosing invocation, private views, checkpoints and child after-before-caller-continuation remain applicable. A completed after is not an invariant over later writes.

## Pending operational formalisation

Q-072 must define the state, causal discovery/attribution, readiness, completion barriers and level incorporation/disposal algorithms. The author's proposal of waiting on all owners of waves previously shared is not accepted as the completion algorithm. Shared physical participation alone cannot be treated as an already established causal dependency. Continuous tides, exterior waits and joint consequences require contrasting evidence before the algorithm is chosen.

The existing single exterior-resolution queue is not replaced by concurrent exterior roots. Sibling asynchronous invocation, waits, joins, cancellation and root concurrency remain undecided. No asynchronous launch keyword is selected; in particular the illustrative word spawn is not a Mud syntax proposal to be integrated.

## Alternatives and consequences

A branch for every ordinary call would conflate alternative evolution with nested confirmation. Describing all nested success as no confirmation obscures the relative frontier. Neither alternative is chosen. Stable-root atomicity, rollback/recovery and imagine isolation remain mandatory; relative incorporation cannot publish stable storage or irreversible effects prematurely.

## Verification obligations

A child succeeds, its parent later fails and the stable world remains unchanged. A later caller write does not reevaluate the child's after. An imagined action may return Success while its branch is discarded. Independent owners sharing a wave and suspended exterior work are required algorithm cases, not a completed scheduler proof.
