---
id: Q-060
title: Reflective `TypeKind` catalogue
priority: P1
opened: 2026-08-16
resolved: false
closed:
decisions:
  - D-087
affects:
  - especificacion/08-sintaxis-abstracta.md
superseded-by: []
---

# Q-060 — Reflective `TypeKind` catalogue

## Question

Which public members does `TypeKind` contain, what stability does MUD guarantee for this reflective catalogue, and how does it relate to the type system's normalised internal forms?

## Context

D-087 makes `Type~kind` observable, but deliberately leaves the concrete `TypeKind` catalogue to the type-system specification. Without an active question, this part of the reflective API could be closed accidentally while formalising internal types.

## Already decided

- Every value exposes `~type: Type`.
- `Type` exposes `~kind`.
- The `TypeKind` catalogue is part of the reflective API and must not automatically be confused with internal compiler constructors.

## Outstanding

- C1: Enumerate the minimum public categories of MUD 1.0.
- C2: Decide which catalogue changes are compatible between versions.
- C3: Define the relation between a public category and normalised internal forms the compiler may use.

## Closure criterion

- C1: A complete normative catalogue exists for MUD 1.0.
- C2: The specification declares its observable stability.
- C3: Every relevant internal form can be projected deterministically to a public `TypeKind` member without accidentally exposing implementation details.

## Resolution

Pending.
