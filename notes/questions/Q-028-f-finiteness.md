---
id: Q-028
title: Finiteness
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-155
  - D-151
  - D-044
  - D-047
  - D-081
  - D-088
affects: []
superseded-by: []
---

# Q-028 — Finiteness

## Content

Analysis limits, conservative approximations and messages when finiteness cannot be proven.

Status: **partially decided** by [[notes/decisions/ADR-044-reachability-eventually|D-044]], [[notes/decisions/ADR-047-quantifiers-and-finite-iteration|D-047]], [[notes/decisions/ADR-081-collection-filtering-take-and-indexing|D-081]] and [[notes/decisions/ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]].

Failure to prove finiteness or enumerability statically rejects a use that requires it; it does not produce a negative runtime answer. The same obligation applies to filters and `take`. D-088 retains this requirement for `for each`, selection and quantifiers/aggregators, and limits traversable cyclic domains to one fundamental period. The mandatory elementary basis is specified; the uniform procedure and diagnostic classes are fixed, while its complete normalization/search/completion specification remains to be written.

## Already decided

D-151 retains finite collections, distinguishes unbounded static cardinality from infinite values, fixes a mandatory elementary enumeration proof basis, and corrects Rum's finite binary64 domain description without enabling numeric interval enumeration. No infinite lazy sequence type is introduced.

## Pending

- Specify and evidence the exact shared normative procedure: normalization, supported finite-proof search and completion conditions. Implementation-dependent admission and language-level limits inferred from tool resource caps are not pending choices.
- Provide contrasting evidence for proved violation, completed-but-unproved obligation and resource-interrupted tool verification, without introducing new runtime value/error types.
- Coordinate deeper state-space finiteness with reachability and termination without treating a finite snapshot as a uniform bound on future worlds.

## Closure criteria

- C1: The mandatory basis and proof premises are covered by normative rules and evidence.
- C2: The shared procedure and its completion/search conditions are specified; diagnostic distinctions are evidenced.
