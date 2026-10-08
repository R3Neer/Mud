---
id: D-144
title: Public TypeKind categories
status: current
date: 2026-10-08
supersedes: []
superseded-by: []
questions:
  - Q-060
affects:
  - specification/11-type-system.md
  - specification/09-abstract-syntax.md
---

# ADR-144 — Public TypeKind categories

## Context

The author selects public categories, renames Product to Tuple and ExactDictionary to Dictionary, and chooses an extensible catalogue. This partially settles D-087's catalogue boundary without selecting extension identity/registration or completing the descriptor inventory.

## Decision

Classify the public exterior, not an alias's hidden representation or compiler nodes. Nominal thing/alias/family categories are Thing, Alias and Family. Nat, Int, Num, Rum, Money, Text, Char and Bool are Basic; Any is separate. Anonymous forms use Tuple, Collection, Union, Interval, Dictionary and FunctionalDictionary. Magnitude and PointMagnitude are separate; cyclic points remain PointMagnitude. Produced look/sublook types use LookResult; message/submessage payload types use MessagePayload. Callable categories are ActionCallable, LookCallable and BooleanRuleCallable; reactive/always rules do not become Boolean callables. Generic applications retain their constructor's category rather than acquiring GenericApplication. Descriptors are separated by semantic kind, including TypeDescriptor, FieldDescriptor, ParticipantDescriptor, MetadataDescriptor and DomainDescriptor, rather than one undifferentiated Descriptor.

The catalogue permits additions; consumers cannot assume the selected core exhausts all future or implementation-extension categories. Extensions do not reclassify standard forms, expose internal nodes as public kinds or turn an alias vector into a new mandatory kind. Extension identities, compatibility/registration rules, the complete descriptor inventory and remaining normalization boundary cases stay in Q-060.

## Alternatives and consequences

Reject representation-based alias classification, GenericApplication and the names Product/ExactDictionary. Public Tuple naming does not rename product notation or existing AST constructors. No complete extensible-family mechanism is selected here.

## Verification

MUD-TYPE-026 and the accepted category table integrate the choices. Q-060 remains partial with exact outstanding closure work. No chapter is promoted.
