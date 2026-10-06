---
id: D-112
title: Explicit storage initialisation
status: current
date: 2026-10-06
supersedes:
  - D-017
superseded-by: []
questions:
  - Q-047
affects:
  - Language contracts and their developed normative surfaces
---

# ADR-112 — Explicit storage initialisation

## Context

The author chooses explicit storage initialisation rather than a type-wide default function. This replaces D-017 and amends D-015, D-026, D-031, D-032, D-038, D-068, D-069, D-074 and D-085.

## Decision

Every newly declared stored thing field includes an explicit initialiser. Descendants inherit that declaration and initialiser without repeating them. Existing specific initialisation contributions retain their precedence and inheritance rules. A refinement must preserve a valid effective initialiser or replace it. Recreating a destroyed materialisation reruns effective initialisation from the canonical schema, never from prior or ancestor mutable state.

There is no default(type) function or automatic choice of zero, false, a family member or a world participant. Type validity and supplying a value are separate. An empty domain cannot supply a required value; a zero-minimum collection can explicitly use empty.

Structural alias components may omit a default: they are then required in every construction. Positional construction supplies all components. Named construction may omit only components with explicit effective defaults. Defaults are pure static expressions satisfying the complete component contract; inheritance and overrides retain their existing substitutability rules. Every component is present in the resulting immutable value.

Every stored family datum has an explicit schema default or an explicit assignment in every member. Member assignment takes precedence over schema default, with no type fallback. Calculated data already have defining expressions.

Explicit given defaults and intrinsic metadata defaults such as ~name and ~prefixes retain their individual contracts. User-defined stored metadata must resolve to an explicit declaration/file value; a type annotation alone invents no value.

## Integration review

The mathematical, grammar, CST and Surface AST surfaces distinguish mandatory storage initialisers from optional alias/family defaults. Alias and family completeness are elaboration constraints. The nominal HIR retains the same field symbols, owners and initialisation references; it requires no type-default node. Type and lifecycle chapters not yet developed retain interim authority through this decision.

## Verification

1. count: Nat without = is invalid syntax; count: Nat = 0 is valid.
2. Inherited initialisation needs no repetition; incompatible refinement is rejected.
3. A required alias component cannot be omitted; an explicit component default can.
4. Every family member initialises required data, including positive-cardinality collections.
5. Destroy/create reinitialises from the canonical schema.
