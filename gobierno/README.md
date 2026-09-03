---
title: MUD project governance
aliases:
  - MUD governance
tags:
  - mud/gobierno
status: vigente
---

# MUD project governance

This directory contains processes that govern the project's evolution, but do
not define the language's meaning.

## Documents

- [[POLITICA-DE-COMMITS|Commit policy]]
- [[POLITICA-DE-ARCHIVOS-TEMPORALES|Temporary-file policy]]
- [[temporales.base|Active-temporaries view]]
- [[CICLO-DOCUMENTAL|Document lifecycle]]
- [[POLITICA-DE-DECISIONES|Decision policy]]
- [[POLITICA-DE-PREGUNTAS|Question policy]]
- [[notas/decisiones/README|Generated decision index]]

## Separation of authorities

| Directory | Authority |
| --- | --- |
| `especificacion/` | Language rules and conformance criteria |
| `notas/` | Non-normative analysis, risks and planning |
| `notas/decisiones/` | Decision provenance and lifecycle |
| `notas/preguntas/` | Open uncertainties and traceability of their closure |
| `gobierno/` | Editorial and change-control processes |

## Validators

- `python gobierno/validate_temporaries.py`: checks the lifecycle of temporary documents.
- `python gobierno/validate_spec_editorial.py`: applies the MUD-EDIT-002 mechanical barrier and checks that `Q-NNN` references agree with their statuses and with `questions:`.
- `python gobierno/test_validate_spec_editorial.py`: runs the editorial barrier's regression fixtures.
- `python tooling/translation/check_migration.py`: while the migration to English continues, combines the R3Translate profile, its generated glossary and the editorial barriers.
