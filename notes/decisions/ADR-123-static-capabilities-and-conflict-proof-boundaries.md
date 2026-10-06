---
id: D-123
title: "Static capabilities and conflict proof boundaries"
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - "Q-006"
  - "Q-021"
affects:
  - "[[specification/14-fields-and-mutability]]"
---

# ADR-123 — Static capabilities and conflict proof boundaries

## Context

The author authorised formalisation of D-026, D-046, D-117 and the accepted block/adapter contracts. Static acceptance must distinguish mandatory cardinality evidence from residual concrete overlaps.

## Decision

Chapter 14 defines root-based writable invariance, reconstruction through immutable intermediate values, immediate inner capabilities, inherited block modes, private regions, static schemas and effect summaries. Minimum conflict analysis handles resolved equal roots, equal/distinct constant keys, distinct components and known generations. Proved incompatible coexistent contributions are rejected; symbolic destination/value overlap not decided by the mandatory proof basis remains a consolidation check.

Stored cardinality has the stronger existing D-026 obligation: prove preservation at the end of each then and for possible consolidations. Unknown preservation is conservatively rejected, even when an individual argument or query could use a runtime admission check. Finite bounds, known membership, correlated guards, sequential normalization, deduplication and uniqueness no-ops must be included. No complete arbitrary predicate solver is required. These rules delimit the remaining minimum-completeness questions Q-006 and Q-021.

Foreign contracts and recovery cannot manufacture write permission or bypass the protected block mode. Full causal transitions, lifetime protocols and adapter ABI remain outside this static phase. The chapter remains proposed pending publication.

## Verification

MUD-EFFECT-001 through MUD-EFFECT-006, writable variance witnesses, static-cardinality versus runtime-admission cases, and residual symbolic-key overlap with separately proved cardinality.
