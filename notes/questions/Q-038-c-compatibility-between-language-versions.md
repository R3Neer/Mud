---
id: Q-038
title: Compatibility between language versions
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-159
affects:
  - specification/01-scope-and-conformance.md
superseded-by: []
---

# Q-038 — Compatibility between language versions

## Already decided

[[../decisions/ADR-159-fixed-target-static-conformance-and-version-boundaries|D-159]] specifies fixed-target static conformance, compiler-release independence, version-specific closed catalogues, unchanged normative certification and explicit rechecking under another target. Source acceptance is distinct from public-contract, execution and persistence compatibility. No automatic migration or version-number compatibility promise is selected.

## Pending outside the independent static scope

- Project target-version declaration, default/discovery and descriptor schema, coordinated with Q-071.
- Source/anchor migration records and application, coordinated with Q-014.
- Versioned semantic IR and its migration, coordinated with Q-009.
- Persisted worlds/materializations and observation/host compatibility procedures, coordinated with their causal and host contracts.

These do not reopen the fixed-target static contract and are not prerequisites for writing its independent construct chapters.

## Closure criterion

- C1: Fixed-target source/static conformance and compatibility are specified with contrasting evidence.
- C2: Project declaration/default/discovery and source/IR/persistent migration protocols are specified and evidenced.

## Resolution

Partially resolved. C1 is covered by MUD-CONF-001 and the contrasting table in specification/01-scope-and-conformance.md. C2 remains outside the current static task and is not declared complete.
