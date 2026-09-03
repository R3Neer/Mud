---
id: D-007
title: "Causal resolution by waves over snapshots"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-005"
  - "Q-020"
affects:
  - "causal resolution and wave chapters"
---

# ADR-007 — Causal resolution by waves over snapshots

## Context

Assess reactions whilst mutating the same state enter results
depend on the order in which they are traversed and allow a rule to observe a
resolution partial.

## Decision

Causal consequences are resolved by waves. Each wave assesses its
conditions relating to a snapshot is defined and its effects are consolidated before
to produce the snapshot observed by the wave Next.

None state part of a wave is published as stable state.

## Consequences

D-045 builds partnerships, reactive memory y queue causal. D-046 y D-060
specify the consolidation deterministic model of effects.

