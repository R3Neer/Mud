---
title: Governance from the MUD project
aliases:
  - Gobierno
tags:
  - mud/gobierno
status: vigente
---

# Governance from the MUD project

This directory contains processes that govern the project’s development, but do not define the meaning of the language.

## Documents

- [[POLITICA-DE-COMMITS|Policy commits]]
- [[POLITICA-DE-ARCHIVOS-TEMPORALES|Policy of temporary files]]
- [[temporales.base|Overview of active storms]]
- [[CICLO-DOCUMENTAL|Ciclo documental]]
- [[POLITICA-DE-DECISIONES|Policy decisions]]
- [[POLITICA-DE-PREGUNTAS|Policy questions]]
- [[notas/decisiones/README|Index generated from decisions]]

## Separation of powers

| Directory | Authority |
| --- | --- |
| `especificacion/` | Language standards and criteria for conformance |
| `notas/` | Non-regulatory analysis, risks and planning |
| `notas/decisiones/` | Provenance and cycle on decision-making |
| `notas/preguntas/` | Outstanding uncertainties and traceability their resolution |
| `gobierno/` | Editorial and change control processes |

## Validators

- `python gobierno/validate_temporaries.py`: checks the cycle retention period for temporary documents.
- `python gobierno/validate_spec_editorial.py`: applies the mechanical barrier from MUD-EDIT-002 and checks that the references `Q-NNN` are consistent with their states and with `questions:`.
- `python gobierno/test_validate_spec_editorial.py`: runs the regression fixtures for the publishing barrier.
- `python tooling/translation/check_migration.py`: whilst the migration to English is underway, combine the R3Translate profile, its generated glossary and the editorial barriers.

