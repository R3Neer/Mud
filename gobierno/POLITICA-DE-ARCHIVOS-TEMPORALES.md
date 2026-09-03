---
title: MUD temporary-file policy
aliases:
  - Temporary files
tags:
  - mud/gobierno
  - mud/temporales
status: vigente
---

# MUD temporary-file policy

## Purpose

This policy governs documents and configuration artefacts that must remain
versioned across several commits because they coordinate ongoing work, but do
not form part of the project's permanent state.

An ordinary ephemeral file is not versioned. Logs, builds, caches, dumps,
local tool state and other reproducible residue must live outside the
repository or be covered by `.gitignore`.

## Source of truth

The metadata in the file itself are the sole source of truth about its
temporariness. An intentionally temporary Markdown document uses this
frontmatter:

```yaml
temporary: true
temporary-reason: "Reason it must remain versioned"
temporary-delete-when: "Semantic deletion condition"
temporary-delete-after: 2026-09-30
```

`temporary-delete-after` is optional and is used only when an objective
deadline exists.

An intentionally temporary TOML file uses the same properties in its root
table:

```toml
temporary = true
temporary-reason = "Reason it must remain versioned"
temporary-delete-when = "Semantic deletion condition"
temporary-delete-after = 2026-09-30
```

`temporary: false` is not used. If a temporary document legitimately becomes
permanent, remove `temporary` and every `temporary-*` property. If it is no
longer needed, delete the file.

## Meaning of the properties

- `temporary: true`: the document must eventually disappear or explicitly
  leave its temporary lifecycle by becoming permanent.
- `temporary-reason`: explains why it deserves to remain versioned in the
  meantime. It is required and cannot be empty.
- `temporary-delete-when`: a required semantic condition that determines when
  it must be deleted. It cannot be empty.
- `temporary-delete-after`: an optional ISO `YYYY-MM-DD` deadline. A date that
  has already passed blocks the commit.

The properties are flat and belong to the file they govern. No parallel manual
register of temporary files is maintained.

## Scope

The `temporary:*` contract applies to intentionally versioned Markdown
documents and TOML files. No other temporary artefact enters `main` through
this policy; it must remain outside the repository, on a laboratory branch, or
be covered by a specific policy that establishes an equivalent lifecycle.

## Obsidian view

`[[temporales.base|gobierno/temporales.base]]` is a human-facing view derived
from the Properties of Markdown notes. It is not a second source of truth, and
no file is added to it manually. Temporary TOML files appear in the validator's
complete inventory even though Obsidian Bases does not display them.

The Base provides:

- **Active temporaries**: every document with `temporary: true`.
- **With a deadline**: temporaries declaring `temporary-delete-after`, ordered
  by date.
- **Incomplete metadata**: temporaries without a reason or deletion condition.

## Mechanical validation

From the repository root:

```powershell
python gobierno/validate_temporaries.py
```

The validator:

- discovers versioned, non-ignored Markdown documents and TOML files;
- reads properties from Markdown frontmatter or the TOML root table;
- always prints the inventory of active temporaries;
- requires non-empty `temporary-reason` and `temporary-delete-when`;
- rejects `temporary: false` and `temporary-*` properties without
  `temporary: true`;
- validates `temporary-delete-after` as an ISO date when present;
- fails when a deadline has already passed.

The validator does not try to interpret arbitrary semantic conditions such as
"Stage 8 is complete". The person or agent preparing the commit must review
the printed inventory and decide whether any condition has already been met.

## Gate before every commit

Before creating any commit, run the validator and review the inventory of
`temporary: true` documents.

If a document's `temporary-delete-when` condition is already met, delete the
document before closing the commit unless the change itself explicitly modifies
its lifecycle. An expired `temporary-delete-after` date is a mechanical block
and cannot be ignored through an informal exception.

The review applies to every active temporary, not only to files modified by the
commit.
