---
title: MUD project governance
aliases:
  - MUD governance
tags:
  - mud/governance
status: current
---

# MUD project governance

This directory contains processes that govern the project's evolution, but do
not define the language's meaning.

## Documents

- [[COMMITS-POLICY|Commit policy]]
- [[TEMPORARY-FILES-POLICY|Temporary-file policy]]
- [[temporales.base|Active-temporaries view]]
- [[DOCUMENT-LIFECYCLE|Document lifecycle]]
- [[DECISIONS-POLICY|Decision policy]]
- [[QUESTIONS-POLICY|Question policy]]
- [[notes/decisions/README|Generated decision index]]

## Separation of authorities

| Directory | Authority |
| --- | --- |
| `specification/` | Language rules and conformance criteria |
| `notes/` | Non-normative analysis, risks and planning |
| `notes/decisions/` | Decision provenance and lifecycle |
| `notes/questions/` | Open uncertainties and traceability of their closure |
| `governance/` | Editorial and change-control processes |

## Validators

- `python governance/validate_temporaries.py`: checks the lifecycle of temporary documents.
- `python governance/validate_spec_editorial.py`: applies the MUD-EDIT-002 mechanical barrier and checks that `Q-NNN` references agree with their statuses and with `questions:`.
- `python governance/test_validate_spec_editorial.py`: runs the editorial barrier's regression fixtures.
