---
id: D-097
title: "HIR nominal vigente e IR semántico diferido"
status: vigente
date: 2026-08-28
supersedes: []
superseded-by: []
questions: []
affects:
  - "pipeline, resolución nominal, HIR nominal, tipado, elaboración, futura representación semántica, capítulo 09, validadores y artefactos mecánicos"
---

# ADR-097 — HIR nominal vigente e IR semántico diferido

- Modifica: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]], [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]] y [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].
- Precisa la frontera de fases usada por [[ADR-092-disponibilidad-estatica-de-propiedades-reflectivas|D-092]].

## Contexto

La arquitectura de MUD distingue correctamente el AST superficial, la resolución nominal y las fases posteriores de tipado y elaboración. Sin embargo, el repositorio había fijado un esquema ASDL detallado para la salida semántica posterior antes de disponer de una especificación desarrollada del sistema de tipos y de la elaboración que deberían producirla. Eso convertía decisiones todavía futuras sobre representación interna en un contrato normativo prematuro.

La resolución nominal sí está suficientemente delimitada: nombres, scopes, símbolos, bindings, anclas y las relaciones nominales de propiedad, especialización y referencia pueden definirse sin resolver tipos efectivos ni semántica dinámica.

## Decisión

MUD mantiene actualmente dos representaciones normativas en la cadena de frontend:

1. el AST superficial de `especificacion/sintaxis/mud-surface-ast.asdl`;
2. el HIR nominal producido por resolución de nombres, en `especificacion/nombres/mud-nominal-hir.asdl`.

El HIR nominal contiene únicamente información justificable por resolución nominal. Su grafo admite propiedad, especialización y referencia nominal. No contiene tipos efectivos, dominios efectivos, cardinalidades inferidas, conversiones elaboradas, efectos, dependencias semánticas ni evidencia de terminación.

El tipado y la elaboración siguen siendo fases arquitectónicas posteriores y podrán producir una representación semántica propia. Esa representación se denomina de forma conceptual **IR semántico futuro**, pero MUD no fija todavía:

- un archivo ASDL para ella;
- un esquema de serialización;
- nombres concretos de nodos o aristas;
- una `schemaVersion` actual;
- qué información derivada debe almacenarse materialmente frente a reconstruirse.

El catálogo conceptual de D-051 pasa a ser un conjunto de requisitos que deberá revisarse cuando exista una superficie desarrollada de tipado y elaboración suficiente para diseñar esa representación. No obliga a mantener hoy un esquema mecánico anticipado.

El directorio genérico `especificacion/ir/` deja de ser una superficie normativa. El HIR nominal se ubica junto a la resolución de nombres en `especificacion/nombres/`.

Todo cambio futuro que introduzca o modifique nombres, scopes, propietarios, bindings, categorías nominales, anclas, visibilidad nominal o especialización debe revisar en el mismo cambio el capítulo 09 y el HIR nominal, conforme a MUD-EDIT-004.

## Consecuencias

- Ningún validador puede exigir la existencia de `mud-semantic-ir.asdl`.
- Ningún documento de la especificación actual presenta como existente un contrato posterior a tipado y elaboración.
- El HIR nominal continúa siendo un contrato mecánico normativo y reconstruible desde AST superficial + reglas de resolución.
- Las decisiones que necesitan una distinción semántica posterior pueden conservarla como requisito de elaboración futura sin fijar por adelantado su codificación.
- Diseñar el futuro IR requerirá integrar las superficies de tipos y elaboración que existan entonces y podrá adoptar una estructura distinta a cualquier esquema experimental previo.

## Verificación

1. `especificacion/ir/` no existe.
2. `especificacion/nombres/mud-nominal-hir.asdl` existe y solo modela información nominal.
3. Los validadores no requieren ningún IR semántico actual.
4. El pipeline documental distingue HIR nominal vigente de representación semántica futura todavía no formalizada.
5. Los cambios que afecten resolución nominal tienen una obligación editorial explícita de revisar capítulo 09 + HIR nominal.
