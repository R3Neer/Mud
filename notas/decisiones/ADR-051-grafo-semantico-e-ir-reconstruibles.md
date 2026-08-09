---
id: D-051
title: "Grafo semántico e IR reconstruibles"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-009"
  - "Q-016"
  - "Q-027"
  - "Q-034"
  - "Q-054"
  - "Q-059"
affects:
  - "arquitectura, grafo semántico, IR, conformidad"
---
# ADR-051 — Grafo semántico e IR reconstruibles

- Ampliada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Ampliada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]
- Modificada por: [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]]
- Modificada además por: [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]]
- Ampliada por: [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]]
- Relacionada con: [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]]
- Preguntas relacionadas: Q-009, Q-016, Q-027, Q-034, Q-054, Q-059
- Documentos afectados: arquitectura, grafo semántico, IR, conformidad

## Contexto

El grafo y el IR son fundamentales para impacto, explicación y ejecución, pero no deben convertirse en fuentes alternativas de verdad.

## Decisión

Los archivos `.mud` y sus decisiones de versión son la única fuente semántica. El AST, la tabla de símbolos, el grafo y el IR se reconstruyen a partir de ella.

El AST conserva forma escrita y procedencia. El IR conserva significado resuelto y debe:

- declarar `schemaVersion`;
- usar anclas resueltas;
- distinguir las tres variantes de regla;
- separar participantes de `given`;
- representar `for` y `on` conforme a D-025, D-036 y D-063, incluidas cardinalidad colectiva, mutabilidad exterior o interior, refinamientos nominales, restricciones conjuntas y vinculación por identidad, valor o lugar;
- conservar predeterminados estáticos y modos posicionales o nominales de los `given`, que carecen de capacidades de escritura;
- normalizar tipos, aliases, dominios, cardinalidades, unidades e intervalos;
- representar efectos, lecturas, escrituras, llamadas y dependencias;
- distinguir las vinculaciones locales inmutables de los campos, lugares y efectos, conservando su ámbito y orden de evaluación;
- conservar referencias a archivo y rango de origen;
- representar actividad lógica y dependencias suspendidas;
- incluir `look`, `message` y la evaluación diferida de sus salidas.
- distinguir `TestDecl`, su conjunto inicial local, sus efectos, sus aserciones y sus diagnósticos.

El grafo es una proyección consultable del IR. Como mínimo reconoce nodos para declaraciones, componentes, campos, dominios, unidades, participantes, `given`, patrones de vinculación, expresiones `allowed` y consultas `eventually`.

Sus familias de aristas incluyen:

- identidad y especialización: `IS`;
- declaración y tipo: componentes, campos, valores, unidades, participantes y `given`;
- dominios, cardinalidad, mutabilidad exterior o interior, lugares receptores y vinculación mediante `in`;
- lectura, escritura y consulta de reglas;
- dependencias de `when`, `if`, `after`, `old` y `always`;
- activaciones, lecturas, escrituras y diagnósticos pertenecientes a tests;
- llamadas y vinculaciones de acciones;
- dependencias de `allowed` y `eventually`;
- `CREATES`, `DESTROYS`, `ADDS_TO` y `REMOVES_FROM`;
- derivación dimensional, `POINT_OVER` y equivalencias de unidad;
- dependencias generales, de dominio y estocásticas;
- producción y lectura diferida de `look` y `message`;
- dependencias duras que determinan suspensión lógica.

Los nombres concretos de campos JSON y aristas se fijarán con el esquema de Q-009. El catálogo conceptual anterior sí es obligatorio: una representación conforme no puede perder esas distinciones aunque las codifique de otro modo.

## Consecuencias

- Una discrepancia se resuelve descartando y reconstruyendo el derivado.
- Dos herramientas pueden intercambiar IR solo cuando declaren una versión de esquema compatible.

## Verificación

1. Reconstrucción determinista desde el mismo programa.
2. Procedencia IR → AST → rango de fuente.
3. Consultas de lectores, escritores, llamadas y dependencias transitivas.
4. Representación diferenciada de `look`, `message`, tests y las tres reglas.
5. Rechazo o migración explícita de una versión incompatible.
