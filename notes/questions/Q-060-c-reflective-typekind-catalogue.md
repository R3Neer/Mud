---
id: Q-060
title: Reflective `TypeKind` catalogue
priority: P1
opened: 2026-08-16
resolved:
closed:
decisions:
  - D-148
  - D-144
  - D-087
affects:
  - specification/09-abstract-syntax.md
superseded-by: []
---

# Q-060 — Reflective `TypeKind` catalogue

## Question

Which public members does `TypeKind` contain, what stability does MUD guarantee for this reflective catalogue, and how does it relate to the type system's normalised internal forms?

## Context

D-087 makes `Type~kind` observable, but deliberately leaves the concrete `TypeKind` catalogue to the type-system specification. Without an active question, this part of the reflective API could be closed accidentally while formalising internal types.

## Already decided

D-144 and MUD-TYPE-026 fix the public exterior principle and selected categories, including Tuple, Dictionary, FunctionalDictionary, distinct descriptors and callable groups. Applied generics retain their constructor category. D-148 fixes a closed builtin family per language version, normalized projection with nominal preservation, uniform Collection classification, ComponentDescriptor and the DeclarationDescriptor fallback. Libraries cannot extend the catalogue.

## Pending

- Audit the complete public builtin descriptor/type inventory and any remaining projection boundary not covered by the selected categories and normalization policy.
- Specify observable compatibility for catalogue changes between language versions; extensible-category registration is no longer a pending language feature.

## Closure criterion

- C1: A complete normative core catalogue and projection exists.
- C2: Fixed-family behavior and observable version compatibility are specified.
- C3: Internal forms project without exposing incidental implementation nodes.

## Resolution

Partially resolved by [[../decisions/ADR-144-public-type-kind-categories]] and [[../decisions/ADR-148-fixed-type-kind-family-and-normalized-projection]]. The selected categories are accepted; the pending items are not implied by this choice.
