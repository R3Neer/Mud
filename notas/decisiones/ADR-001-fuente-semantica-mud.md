---
id: D-001
title: "`.mud` como fuente semántica de verdad"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "especificacion/01-alcance-y-conformidad.md"
  - "arquitectura de compilador, runtime y materializadores"
---

# ADR-001 — `.mud` como fuente semántica de verdad

## Contexto

La lógica de un dominio puede quedar repartida entre código, datos, tests,
configuración y documentación. Si varias de esas representaciones pueden añadir
significado por separado, no existe una fuente desde la que reconstruir o
auditar el comportamiento completo.

## Decisión

Los archivos `.mud` son la única fuente semántica del comportamiento de dominio
representado por MUD. AST, IR, grafos, código generado, índices, documentación
derivada y materializaciones son proyecciones reconstruibles y no pueden añadir
reglas de dominio.

Las decisiones y la especificación gobiernan el lenguaje con el que se
interpreta la fuente, pero no forman parte del estado de un mundo MUD.

## Consecuencias

- Una implementación debe poder reconstruir sus derivados desde la fuente.
- El significado duradero no puede residir únicamente en prompts, cachés o
  código manual.
- D-011, D-051 y D-052 precisan los contratos de los derivados.

## Verificación

Dos reconstrucciones con la misma fuente, versión de especificación y versión
de compilador deben preservar las mismas distinciones semánticas.
