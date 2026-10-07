---
id: D-009
title: "`imagine` as a baseless rumour"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-007"
  - "Q-035"
affects:
  - "admissibility and speculative query chapter"
---

# ADR-009 — `imagine` as a baseless rumour

- Amended by: [[ADR-119-invocation-owned-completion-and-imagine|D-119]].

## Context

Check only the preconditions for a action may declare a
request whose resolution 'complete' would end in conflict, invariant
unfulfilled or failure.

- Amended by: [[ADR-139-reality-levels-branches-and-relative-confirmation|D-139]].

## Decision

`imagine` executes the complete invocation protocol in a disposable alternative branch and returns ActionReply. Inner relative confirmation does not reach the stable root or publish exterior outputs. An Errors alternative is returned as an ordinary reply value, rather than converted to false or raised merely by returning it.

## Consequences

D-043 develops the semantics in full, together with his comments.

