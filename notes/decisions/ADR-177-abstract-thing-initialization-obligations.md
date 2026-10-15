---
id: D-177
title: Abstract thing initialization obligations
status: current
date: 2026-10-15
supersedes: []
superseded-by: []
questions: []
affects:
  - Thing schemas, grammar optional defaults and static initialization completeness
---

# ADR-177 — Abstract thing initialization obligations

## Decision

An abstract thing may declare an immutable or mutable stored field without an
initializer. Its explicit effective contract must determine a complete type;
no initializer-based hole inference is available. An abstract descendant may
keep the obligation pending. Every concrete descendant must resolve every
required initializer before materialization, using an applicable inherited
initializer or its own explicit initializer under ordinary origin/conflict
rules. Abstractness does not fabricate values or allow uninitialized runtime
slots. Ordinary stored locals and newly declared concrete stored fields retain
mandatory initial values. Alias/family defaults keep their separate rules.

Partially amends D-015, D-037, D-085 and D-112. Preserve closed static schema computation,
nominal origin identity, diamond deduplication and initializer precedence.
No runtime world value is inherited from another thing. Finite supplied schema
certificates cover abstract deferral, concrete completion and unresolved joins.
