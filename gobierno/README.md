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
- [[CICLO-DOCUMENTAL|Ciclo documental]]
- [[POLITICA-DE-DECISIONES|Política de decisiones]]
- [[POLITICA-DE-PREGUNTAS|Política de preguntas]]
- [[USO-DE-REPO-PATCHER|RepoPatcher experimental para paquetes descargables y aplicación local]]
- [[notas/decisiones/README|Índice generado de decisiones]]

## Separación de autoridades

| Directorio | Autoridad |
| --- | --- |
| `especificacion/` | Norma del lenguaje y criterios de conformidad |
| `aprendizaje/` | Material didáctico, ejercicios y progreso |
| `notas/` | Análisis, riesgos y planificación no normativos |
| `notas/decisiones/` | Procedencia y ciclo de vida de decisiones |
| `notas/preguntas/` | Incertidumbres abiertas y trazabilidad de su cierre |
| `gobierno/` | Procesos editoriales y de control de cambios |

## Herramientas experimentales

RepoPatcher permanece en `tooling/` como experimento de paquetes portables y aplicación local. No define el flujo preferente de cambios remotos desde ChatGPT; ese trabajo sigue la política Git del repositorio y las instrucciones de `AGENTS.md`.
