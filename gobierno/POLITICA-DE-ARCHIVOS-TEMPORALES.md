---
title: Policy of MUD temporary files
aliases:
  - Temporary files
tags:
  - mud/gobierno
  - mud/temporales
status: vigente
---

# Policy of MUD temporary files

## Purpose

This policy governs configuration documents and artefacts that must remain versioned across multiple commits because they coordinate work in progress, but which do not form part of the project’s permanent state.

An ordinary ephemeral file is not versioned. Logs, builds, caches, dumps, local tool state files and other reproducible debris must be stored outside the repository or be covered by `.gitignore`.

## Fuente de verdad

The metadata within the file itself is the only source of truth regarding its temporal nature. A Markdown document that is intentionally time-sensitive uses the following in its frontmatter:

```yaml
temporary: true
temporary-reason: "Motivo por el que debe permanecer versionado"
temporary-delete-when: "Condición semántica de eliminación"
temporary-delete-after: 2026-09-30
```

`temporary-delete-after` is optional and is only used when there is a specific deadline.

A TOML file that is intended to be temporary uses the same properties in its
table root:

```toml
temporary = true
temporary-reason = "Motivo por el que debe permanecer versionado"
temporary-delete-when = "Condición semántica de eliminación"
temporary-delete-after = 2026-09-30
```

`temporary: false` is not used. If a temporary document is legitimately converted into a permanent one, `temporary` and all `temporary-*` properties are removed. If it is no longer required, the file is deleted.

## Meaning of the properties

- `temporary: true`: the document must eventually be deleted or explicitly cease to be temporary cycle, thereby becoming permanent.
- `temporary-reason`: explains why it deserves to be versioned in the meantime. This is mandatory and must not be left blank.
- `temporary-delete-when`: mandatory semantics condition that determines when it must be removed. It is mandatory and cannot be left blank.
- `temporary-delete-after`: optional deadline in ISO format `YYYY-MM-DD`. A date that has already passed will block the commit.

The properties are flat and belong to the file they govern. They are not retained
a parallel manual log of temporary files.

## Alcance

The contract `temporary:*` applies to Markdown documents and TOML files
deliberately adapted. No other time artefact is introduced into
`main` via this policy; it must remain outside the repository, in a
branch in the laboratory or be covered by a specific policy that
establish an equivalent cycle lifespan.

## View of Obsidian

`[[temporales.base|gobierno/temporales.base]]` is a human-readable view derived from the properties of Markdown notes. It is not a second source of truth and no files are added to it manually. Temporary TOML files appear in the validator’s full inventory, even though Obsidian Bases does not display them.

The Centre offers:

- **Active temporary records**: all documents with `temporary: true`.
- **With a deadline**: weather reports issued by `temporary-delete-after`, sorted by date.
- **Incomplete metadata**: temporary records without a reason or without a condition for deletion.

## Validation mechanical

From root of repository:

```powershell
python gobierno/validate_temporaries.py
```

The validator:

- detects versioned Markdown documents and TOML files that have not been ignored;
-  reads the properties from the Markdown frontmatter or the root TOML table;
-  always prints the list of active temporary records;
-  requires `temporary-reason` and `temporary-delete-when` to be non-empty;
-  rejects `temporary: false` and properties `temporary-*` without `temporary: true`;
-  validates `temporary-delete-after` as an ISO date where it exists;
-  fails if a deadline has already passed.

The validator does not attempt to interpret arbitrary semantic conditions such as ‘Stage 8 is completed’. The person or agent preparing the commit must check the printed inventory and decide whether any condition has already been met.

## Gate before every commit

Before creating any commit, the validator is run and the inventory of `temporary: true` is checked.

If a document’s `temporary-delete-when` condition is already met, the document must be deleted before the commit is finalised, unless the change itself is explicitly modifying its cycle lifecycle. An expired `temporary-delete-after` date is a mechanical block and cannot be ignored by means of an informal exception.

review applies to all active temporary files, not just those modified by the commit.

