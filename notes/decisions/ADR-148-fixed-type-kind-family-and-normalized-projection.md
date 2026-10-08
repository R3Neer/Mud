---
id: D-148
title: Fixed TypeKind family and normalized projection
status: current
date: 2026-10-08
supersedes: []
superseded-by: []
questions:
  - Q-060
affects:
  - specification/11-type-system.md
  - specification/types/typing-cases.yaml
---

# ADR-148 — Fixed TypeKind family and normalized projection

## Context

The author revisits D-144's extensibility choice. Ordinary libraries introduce aliases and other existing forms, not new public type constructors. Extension registration has no selected use case.

## Decision

TypeKind is a builtin closed family with a fixed catalogue for each language version. Programmes and libraries cannot add members. Future language versions may revise the catalogue through an explicit specification change; no extension identity or registration mechanism is required.

Classify the normalized effective public type, preserving nominal identities. Int | Int projects to Basic; an alias represented by Int remains Alias. Generic applications retain the constructor category. Collection cardinality, order, uniqueness and nested layers do not create additional kinds: the outermost collection is Collection.

Retain D-144's selected categories. Add ComponentDescriptor, distinct from FieldDescriptor, and DeclarationDescriptor for declaration descriptors without an established more specific category. This does not duplicate DeclarationKind or create ComponentKind. Established TypeDescriptor and callable categories remain specific. The TypeKind family itself has category Family.

## Consequences and remaining scope

This partially amends D-144 and clarifies D-087. Their selected-category contracts remain current. Complete coverage of public builtin descriptor types, projection boundaries not covered by these choices and version compatibility details remain Q-060; the family decision alone is not evidence of a complete catalogue.

## Verification

MUD-TYPE-026 and the category table in chapter 11 specify the accepted projection. The static corpus contrasts nominal aliases, normalized unions, collection properties and descriptor classes. No publication promotion or compiler implementation is claimed.
