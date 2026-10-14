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

## Procedure and independent scope

D-166/D-167/D-168 specify the contextual, finite and recursive source-body
procedures. The author accepts finite lexicographic descent, declaration phases,
certified pure operation classes, actual finite Rum order and exact affine scalar
synthesis. Q-028/Q-029 close with scoped rules and evidence, without claiming a
complete arbitrary-predicate solver, future-state profile or causal completion.
Those independent advanced/native protocols retain their existing questions.
No compiler/runtime/reference-analyzer implementation is requested here.

## Verification and provenance

Extends [[ADR-151-finite-collections-and-mandatory-enumeration-proof-basis|D-151]]. MUD-TYPE-035 and reviewed proof-boundary corpus cases distinguish violation, unproved obligation and interrupted verification. D-168 completes the scoped normalization/search/completion procedures; their certificates do not implement the compiler or causal algorithm.
