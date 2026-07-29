---
id: D-002
title: "MUD describe dominio, no arquitectura de aplicación"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "especificacion/01-alcance-y-conformidad.md"
  - "frontera entre lenguaje y materializadores"
---

# ADR-002 — MUD describe dominio, no arquitectura de aplicación

## Contexto

MUD necesita representar reglas, estado y causalidad sin convertir detalles de
una interfaz, una base de datos o un framework concreto en semántica del
lenguaje.

## Decisión

MUD describe el dominio y su comportamiento observable. No prescribe la
arquitectura general de la aplicación que lo hospeda, su interfaz de usuario, su
protocolo de red, su base de datos ni el framework usado por una
materialización.

La especificación sí puede imponer las estructuras necesarias para ejecutar
MUD de forma conforme, como identidad, atomicidad, orden, tiempo lógico o azar
reproducible. Esa neutralidad tecnológica no significa neutralidad respecto del
modelo semántico propio.

## Consecuencias

- Los adaptadores técnicos permanecen fuera de la semántica de dominio.
- Una materialización puede cambiar de tecnología sin redefinir el mundo.
- D-052 desarrolla la frontera entre compilador y materializadores.
