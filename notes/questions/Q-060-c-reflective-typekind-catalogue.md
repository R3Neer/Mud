---
id: Q-060
title: Reflective `TypeKind` catalogue
priority: P1
opened: 2026-08-16
resolved:
closed:
decisions:
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

D-144 and MUD-TYPE-026 fix the public exterior principle and selected categories, including Tuple, Dictionary, FunctionalDictionary, distinct descriptors and callable groups. Applied generics retain their constructor category. The author chooses additions rather than an exhaustive closed-per-version catalogue; standard categories cannot be reclassified.

## Pending

- Complete the descriptor category inventory and deterministic projection boundaries, including singleton/normalized anonymous forms.
- Choose extension identity and registration, collision handling and catalogue compatibility rules.
- Define how the extensible reflective catalogue relates to ordinary closed family contracts.

## Closure criterion

- C1: A complete normative core catalogue and projection exists.
- C2: Extension identity, registration and observable compatibility are specified.
- C3: Internal forms project without exposing incidental implementation nodes.

## Resolution

Partially resolved by [[../decisions/ADR-144-public-type-kind-categories]]. The selected categories are accepted; the pending items are not implied by this choice.
