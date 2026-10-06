---
id: D-116
title: Contract-visible cross-module specialisation
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - Q-064
affects:
  - Language contracts and their developed normative surfaces
---

# ADR-116 — Contract-visible cross-module specialisation

## Context

The author accepts one cross-module specialisation policy for things and aliases, through the existing contract-visible type closure rather than another export keyword. This amends D-096 and closes Q-064.

## Decision

A module authorized by uses may specialize a thing or alias from another module exactly when its nominal type is in the visible public contract's transitive type closure. The closure includes operation participants/arguments, results, payloads and recursively required representation types. Merely importing a path with using supplies no permission; private types outside that closure remain unavailable as ancestors.

Specialization preserves all inherited substitutability and diamond/member conflict rules. Externally writable stored contracts are invariant; immutable contracts may strengthen guarantees under their existing rules. Inherited canonical initialization is compiled under its declaring owner's access rights and contributes to the descendant's static schema. Inheritance grants no new access to a thing's private ordinary fields, no foreign mutation authority, and no permission to activate another module's identities. Aliases expose their representation only as required to use their visible value contract.

The specialization edge is canonical regardless of module membership; anchors retain ordinary path identity. Linked-world populations and effective ancestry include external descendants when they meet ordinary activity/type criteria. Analysis must consider that extension surface, not assume a module's visible abstract type has only locally declared descendants. Reflection remains valid only when its contract cannot expose invisible entities; filtering private children is not a security policy.

English tooling and generated contract documentation show the complete contract-visible type frontier, its source operations and supported specialization obligations. This makes the available bases discoverable without searching signatures manually, and adds no new source visibility modifier.

## Verification

A public action accepting Base makes Base's nominal contract visible to an authorized module, which may declare Local as Base. A private implementation-only Helper remains an invalid ancestor. The same policy holds for aliases. Using without uses, private-field reading and cross-module start-with activation remain invalid. Diamonds deduplicate inherited declaration origins without sharing thing state.

## Integration review

The developed source/nominal surfaces retain uses versus using and inherited anchors. Nominal HIR already carries Specializes edges, owners and resolved references; authorization changes their admission, not their shape. The specification roadmap and current D-096 no longer prohibit all foreign thing ancestry.
