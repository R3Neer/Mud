---
id: D-170
title: Uniform immutable alias component markers
status: current
date: 2026-10-14
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/11-type-system.md
  - specification/13-aliases.md
  - specification/syntax
  - specification/types
---

# ADR-170 — Uniform immutable alias component markers

## Accepted policy

The author requires let for stored and derived immutable alias components/fields,
aligned with immutable thing fields. Mutable stored thing fields use mut;
alias components still have no outer mutation. A required alias component may
have no default; let declares its schema position, not a value evaluated while
the alias type is declared. Existing complete annotation/default rules remain.

Parameters, family stored data, metadata, assignments and inherited-default
overrides retain their distinct forms. No global let/mut declaration is admitted.
This partially clarifies D-169/D-031/D-113; immutable values, reconstruction and
initializer precedence are unchanged. Current affected ADR examples are migrated.

## Evidence

The component-declaration production, CST RHS, normalized AST documentation and
bounded grammar witnesses cover markers, defaults, type holes and invalid mut or
bare forms. Existing AliasComponentDecl and nominal component identities suffice;
no parser/compiler/runtime implementation is introduced.
