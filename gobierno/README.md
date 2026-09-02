---
title: Gobierno del proyecto MUD
aliases:
  - Gobierno
tags:
  - mud/gobierno
status: vigente
---

# Gobierno del proyecto MUD

Este directorio contiene procesos que gobiernan la evolución del proyecto, pero no definen el significado del lenguaje.

## Documentos

- [[POLITICA-DE-COMMITS|Política de commits]]
- [[POLITICA-DE-ARCHIVOS-TEMPORALES|Política de archivos temporales]]
- [[temporales.base|Vista de temporales activos]]
- [[CICLO-DOCUMENTAL|Ciclo documental]]
- [[POLITICA-DE-DECISIONES|Política de decisiones]]
- [[POLITICA-DE-PREGUNTAS|Política de preguntas]]
- [[notas/decisiones/README|Índice generado de decisiones]]

## Separación de autoridades

| Directorio | Autoridad |
| --- | --- |
| `especificacion/` | Norma del lenguaje y criterios de conformidad |
| `notas/` | Análisis, riesgos y planificación no normativos |
| `notas/decisiones/` | Procedencia y ciclo de vida de decisiones |
| `notas/preguntas/` | Incertidumbres abiertas y trazabilidad de su cierre |
| `gobierno/` | Procesos editoriales y de control de cambios |

## Validadores

- `python gobierno/validate_temporaries.py`: comprueba el ciclo de vida de documentos temporales.
- `python gobierno/validate_spec_editorial.py`: aplica la barrera mecánica de MUD-EDIT-002 y verifica la coherencia de referencias `Q-NNN` con sus estados y con `questions:`.
- `python gobierno/test_validate_spec_editorial.py`: ejecuta los fixtures de regresión de la barrera editorial.
- `python tooling/translation/check_migration.py`: mientras dure la migración al inglés, combina el perfil de R3Translate, su glosario generado y las barreras editoriales.
