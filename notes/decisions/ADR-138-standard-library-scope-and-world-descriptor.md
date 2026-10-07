---
id: D-138
title: Standard library scope and world descriptor direction
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions:
  - Q-069
  - Q-071
affects:
  - "[[specification/05-source-text]]"
  - "[[notes/standard-library-design]]"
  - "[[notes/world-descriptor-design]]"
  - Library planning and dependency tooling
---

# ADR-138 — Standard library scope and world descriptor direction

## Context

The author resumes standard-library planning deferred by D-134. The aim is practical general-purpose Mud programmes with less repetitive code and fewer direct foreign fragments. The author accepts an included base with separately installable official extensions, prefers breadth of contracts before detailed implementation, and accepts TOML as the world-descriptor direction.

## Decision

Plan an included standard-library base and official installable extensions. Develop a broad capability catalogue, contracts and representative uses before requiring complete implementations. Mud implementations may use native adapter support internally. This does not authorise compiler/runtime or library implementation before D-013's formalisation gate.

Use `mud.world.toml` as the planned world descriptor. Its tables, required fields, version semantics, package resolution and locking are not yet specified. `mud.part` retains its existing minimal direct `uses` contract; `using` remains name import rather than dependency installation. No example descriptor establishes an executable manifest schema or silently mounts external parts.

## Alternatives and pending proposals

A custom descriptor language was considered; TOML avoids defining a second configuration grammar. A monolithic mandatory standard library was not chosen. YAML is not the selected direction. Removing build/format fields, author-selected adapter aliases, mandatory declarations, native-manifest references and editor quick fixes remain proposals, not accepted syntax.

SQL is a useful persistence-adapter candidate. No SQL dialect, first implementation, adapter label or database-transaction protocol is selected. Q-069 retains adapter declaration/hosting; Q-071 owns world/package resolution and descriptor schema.

## Integration and verification

The developed source chapter records only the descriptor boundary. The notes distinguish accepted direction, working proposals and questions. Grammar, CST, Surface AST and nominal HIR still describe `.mud` and `mud.part`, not a TOML parser. No concrete library names, APIs, compiler switches or new access modifiers are introduced.
