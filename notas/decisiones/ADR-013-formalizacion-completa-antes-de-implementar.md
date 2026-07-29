---
id: D-013
title: "Formalización completa antes de continuar la implementación"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "especificacion/README.md"
  - "planificación de implementación"
---

# ADR-013 — Formalización completa antes de continuar la implementación

## Contexto

Una implementación temprana resolvería por necesidad ambigüedades todavía
abiertas y podría convertir elecciones accidentales del código en semántica de
MUD.

## Decisión

La especificación formal de MUD 1.0 se completa antes de continuar la
implementación del lenguaje. Los prototipos o herramientas editoriales no
pueden usarse para cerrar silenciosamente cuestiones normativas.

El criterio de completitud y el orden de capítulos pertenecen a
[[especificacion/README|la especificación formal]].

## Consecuencias

- Las decisiones se promueven primero a una norma revisable.
- La implementación posterior se evalúa por conformidad con esa norma.
- Los huecos descubiertos por tooling se registran como preguntas o decisiones,
  no como comportamiento implícito.
