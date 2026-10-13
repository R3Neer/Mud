---
id: D-159
title: Fixed target static conformance and version boundaries
status: current
date: 2026-10-13
supersedes: []
superseded-by: []
questions:
  - Q-038
affects:
  - specification/01-scope-and-conformance.md
  - specification/11-type-system.md
  - specification/README.md
  - notes/type-formalisation-phase.md
---

# ADR-159 — Fixed target static conformance and version boundaries

## Formalization of accepted version policy

A static conformance claim identifies its effective target language version, covered constructs and checked assumptions. The compiler's release is not the target language version. For one target, the normative grammar/contracts, fixed reflective catalogues and certification procedure are the same across implementations. A reusable reference analyzer is optional; reproducing the normative results is mandatory. Tool interruption is reported as incomplete verification rather than a different acceptance result.

Changing compiler releases under the same target cannot silently adopt a newer catalogue, stronger admission procedure or altered numeric policy. Rechecking source under another target uses that target's full contract; successful compilation alone is not a guarantee of unchanged static public contracts or behavioral compatibility. No automatic source/IR/state migration, implicit unknown-kind fallback or version-number compatibility promise is introduced.

This specifies the static part of Q-038 from D-148/D-155 and the established editorial conformance boundary. The project descriptor's version declaration/default/discovery, IR schema migration, anchor/data migration and persisted-world/materialization procedures remain outside this scope and active under Q-038 and their related questions. No configuration spelling or source version annotation is invented.

## Verification

Chapter 01's draft defines fixed-target conformance judgements and contrasting compiler-release/target/certification/categorical-change cases. Chapter 11 and the phase audit cross-reference the boundary. Chapter 01 remains draft; the general version/migration question is not marked closed.
