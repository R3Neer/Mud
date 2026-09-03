---
id: D-104
title: "British English for the editorial migration"
status: current
date: 2026-09-02
supersedes: []
superseded-by: []
questions: []
affects:
  - "temporary translation glossary and profile (removed after migration)"
  - "README.md"
  - "LICENSE"
  - "TRADEMARKS.md"
  - "complete migration of content and paths to English"
---

# ADR-104 — British English for the editorial migration

## Context

Mud is beginning a complete editorial migration from Spanish to English. The
first public documents in English and the temporary glossary already establish
some of the vocabulary that the migration will use.

Without a reference variety, independent translations may mix spellings and
equivalent forms, making the repository appear inconsistent and causing the
glossary to cease being a reliable source.

## Decision

British English will be the canonical variety for Mud's entire editorial
migration. This decision applies to visible text, titles, translated metadata,
glossaries, public documentation and future file or folder names that are
natural words.

In particular, forms such as *behaviour*, *modelling*, *materialisation*,
*normalisation*, *stabilisation*, *organisation* and *authorisation* will be
preferred consistently.

Identifiers, Mud constructs, extensions, formats, dependencies, commands,
external proper names and paths subject to a technical contract will retain
their established spelling. `LICENSE`, for example, remains the conventional
file name even though the noun in prose is *licence*.

## Consequences

- The temporary glossary fixes the British forms, and future translations must
  consult it before being automated or reviewed.
- Already published English documents are corrected so as not to introduce an
  initial exception.
- Each translation batch review must detect and resolve accidental American
  spellings, except in the excluded technical elements.
- This decision does not modify Mud syntax or translate text inside code blocks
  or identifiers that form part of the specification.

## Alternatives considered

- American English: rejected because of the author's editorial preference.
- Mixing variants by document or translator: rejected because it weakens the
  consistency that the glossary must guarantee.
