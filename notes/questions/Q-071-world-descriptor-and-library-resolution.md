---
id: Q-071
title: World descriptor and library resolution
priority: P1
opened: 2026-10-07
resolved:
closed:
decisions:
  - D-138
affects:
  - World configuration, packages, source layout and dependency resolution
superseded-by: []
---

# Q-071 — World descriptor and library resolution

## Already decided

An included library base and installable official extensions are planned. The descriptor direction is `mud.world.toml`. Existing part access and name-import rules remain unchanged. Breadth of library contracts precedes detailed implementation.

## Pending

Define required/optional tables, accepted values, world-root discovery and schema evolution; package identity versus exposed part paths; sources, version constraints, collision/multiple-version rules and lockfile identity. Determine how external distributions enter the world namespace without weakening direct uses, private-file boundaries or type closure. No accepted descriptor schema exists yet.

Adapter declaration, alias lookup, per-distribution environments and native manifests are coordinated with Q-069 rather than answered here. Runtime configuration and recording depend on the causal/patch contracts.

## Closure criteria

- C1: Specify a minimal valid descriptor, full schema, discovery and deterministic diagnostics for unknown/incompatible configuration.
- C2: Specify package resolution, source/version identity and locking, with conflicting-source/version and offline cases.
- C3: Specify distribution-to-part mapping, collision handling and direct uses/type-closure conformance cases.
- C4: Define the boundary with native adapter configuration and runtime/recording settings without embedding unresolved semantics.
