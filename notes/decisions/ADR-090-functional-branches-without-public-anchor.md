---
id: D-090
title: "Functional branches without a public anchor"
status: current
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "functional dictionaries, anchors, post-typing and elaboration semantic representation, dependency graph, semantic operator and tooling"
---

# ADR-090 — Functional branches without a public anchor

- Modifies: [[ADR-085-functional-dictionaries-metadata-and-structured-activation|D-085]].
- Clarifies: [[ADR-087-reflective-metadata-stable-descriptors-and-external-visibility|D-087]].
- Extends: [[ADR-051-graph-future-semantics-and-reconstructable-information|D-051]] and [[ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]].

## Context

D-085 assigned functional-dictionary branches their own anchors so that they could be edited independently. D-087 subsequently established a stricter principle: a metadata-bearing entity needs a typed descriptor and a stable public anchor, and it expressly excluded functional branches because they lack a stable descriptor. Retaining a public branch anchor would preserve two incompatible identity models.

## Decision

A functional-dictionary branch has no public anchor, does not introduce `AnchoredSymbol`, and cannot have metadata of its own. The persistent entity is the owning dictionary.

Each branch has a structural key local to the owning dictionary. For an ordinary branch, the key derives from the canonical form of its selector after the necessary resolution and semantic normalisation; the `_` fallback uses a distinct and unique local variant. Two ordinary branches with the same canonical selector cannot exist in one dictionary. The concrete mechanical encoding of that key in a later representation is left unspecified.

The local key must structurally distinguish an ordinary branch from the fallback without requiring a second persistent identity. The source ordinal is retained separately. In `FirstMatch` it is part of the functional value because it determines priority; in `AllMatches` it retains provenance and diagnostics but does not become a persistent identity. A future representation may choose its encoding while preserving these properties.

Branch dependencies are represented by the pair formed by the owning dictionary's anchor and its local key. An external operation that needs persistence targets the dictionary and expresses branch editing as internal structure of the owner; it cannot treat the branch as an independent global entity.

## Consequences

- The contradiction between D-085 and D-087's admission principle is removed.
- Moving an ordered branch may change semantics without requiring anchor migration.
- Changing a selector may change the local key without constituting a public-entity rename.
- Two canonically equal selectors in one dictionary are invalid because they would represent the same local structural key.
- Set operations on functional dictionaries remain extensional and do not merge branch identities.

## Rejected alternatives

### Retain position-based subordinate anchors

Rejected because reordering `FirstMatch` branches would change identity as well as semantics, and because D-087 excludes the branch as an entity with a stable descriptor.

### Allow canonically duplicate selectors through a local index

Rejected because the branch already has a natural structural key: its canonical selector. Introducing an index would allow two entries with the same key and make editorial operations depend on a distinction that does not exist in the dictionary model.

## Verification

1. No functional branch receives a public anchor or `AnchoredSymbol`.
2. Local identity distinguishes an ordinary branch and the fallback without a contradictory second persistent identifier.
3. Branch dependencies can be reconstructed through the owning dictionary's anchor and its local structural key, without a global collision index.
4. The anchor catalogue does not enumerate functional branches as public entities.
5. D-085 no longer promises `CREATE`, `UPDATE`, `REMOVE` or `MOVE` directed at a branch anchor.
6. D-087 keeps branches outside the metadata-bearing surface.
