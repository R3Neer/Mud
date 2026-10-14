---
id: D-168
title: Finite normative static certification procedure
status: current
date: 2026-10-14
supersedes: []
superseded-by: []
questions:
  - Q-028
  - Q-029
affects:
  - specification/01-scope-and-conformance.md
  - specification/10-names-and-anchors.md
  - specification/README.md
  - specification/11-type-system.md
  - specification/13-aliases.md
  - specification/15-fields-and-mutability.md
  - specification/16-collections.md
  - specification/17-dictionaries.md
  - specification/18-domains-and-intervals.md
  - specification/20-blocks-and-recovery.md
  - specification/21-expressions.md
  - specification/22-quantifiers-and-iteration.md
  - specification/23-boolean-rules.md
  - specification/24-reactive-rules.md
  - specification/25-always-rules.md
  - specification/26-public-boundary.md
  - specification/28-effects.md
  - specification/types
---

# ADR-168 — Finite normative static certification procedure

## Formalization of accepted policy

D-151/D-155 already require finite collections, a mandatory elementary basis,
one normative procedure per target, exact completion conditions and distinct
violation/unproved/interruption outcomes. D-166/D-167 supply the contextual and
recursive classes accepted by the author. This decision records their procedural
integration rather than an implementation-specific admission policy.

## Procedure

specification/types/finite-static-certification.md defines source/value-origin
normalization, finite propositional/availability regions, exact polynomial
normalization with conservative unsupported relations, mixed affine elimination,
finite binary64 reasoning, elementary measure facts, source enumeration certificates
and nonexpansive generic application closure. Every unsupported mandatory
obligation is completed-but-unproved rejection; it is not infinite trial search.

Rational elimination removes variables; integer elimination uses coefficient
normalization and finite congruence periods. Large constants impose no source
limit. Ranking profile/phase search and affine rational synthesis have explicit
finite completion. Equivalent implementation optimization must preserve the
complete verdict, not just soundness on accepted inputs. Opaque relations and
source kinds never acquire guessed proofs.

## Scope and evidence

Q-028 closes for source/application finiteness and its complete stated proof
procedure. Q-029 closes for eligible body classes and the defined ranking search.
A finite snapshot/body certificate does not prove a finite future state space
or causal completion: Q-027/Q-030, Q-020/Q-072 and native protocols retain those
scopes. No analysis profile is silently created for eventually.

Fourteen supplied arithmetic/ranking certificates, existing interval/generic/type
witnesses and reviewed source cases evidence the procedure's sound boundaries.
These kernels do not parse or typecheck Mud, extract an entire analysis or implement
a compiler/runtime. D-151/D-155/D-085/D-044 bodies are reconciled literally.
