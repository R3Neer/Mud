---
id: D-155
title: Uniform normative analysis and finiteness diagnostics
status: current
date: 2026-10-13
supersedes: []
superseded-by: []
questions:
  - Q-028
  - Q-029
affects:
  - specification/11-type-system.md
  - specification/21-expressions.md
  - specification/types
  - specification/README.md
---

# ADR-155 — Uniform normative analysis and finiteness diagnostics

## Decision

Each language version fixes the same normative analysis procedure for mandatory finiteness/enumerability and termination certification. Implementations may share a reusable reference analyzer or implement the procedure independently, but must reproduce its results. Specifying only a set of permitted inference rules is insufficient: normalization, proof search and its completion conditions must also be specified. Optional stronger analysis can explain or suggest changes, but cannot enlarge the admitted programs for that language version. Extending normative admission requires an explicit conformance-contract update.

Distinguish a proved violation (infinite or lacking the required admitted enumeration), a completed normative analysis that leaves the obligation unproved, and a tool analysis interrupted by resource exhaustion. The first two prevent admission with different diagnostic reasons. The third means verification is incomplete; it is not a normative invalid-program judgement. These are tool outcomes, not three new Mud values, language types or runtime Error channels. Runtime resource exhaustion retains its separate contract.

A tool resource bound does not impose a language-level maximum on integer endpoints, collection sizes or contract depths and cannot replace the mandatory elementary basis. Finite/countable mathematics does not by itself grant language enumeration, including Rum's full numeric domain.

## Unresolved procedure and scope

Q-028 retains exact finite-analysis normalization/search/termination specification and required evidence. Q-029 retains the classes and complete method for termination certification. The lexicographic-descent proposal was not accepted and introduces no rule. Existing decreasing-measure obligations remain; no compiler/runtime/reference-analyzer implementation is requested here. These advanced analysis questions do not prevent documenting independently fixed construct typing and effect contracts.

## Verification and provenance

Extends [[ADR-151-finite-collections-and-mandatory-enumeration-proof-basis|D-151]]. MUD-TYPE-035 and reviewed proof-boundary corpus cases distinguish violation, unproved obligation and interrupted verification. Q-028/Q-029 remain active rather than presenting a policy as a completed algorithm.
