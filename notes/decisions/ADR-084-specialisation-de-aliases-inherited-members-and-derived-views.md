---
id: D-084
title: "Especialización de aliases, miembros heredados y vistas derivadas"
status: current
date: 2026-08-04
supersedes: []
superseded-by: []
questions:
  - Q-056
affects:
  - "aliases, gramática, sintaxis, resolución nominal, colecciones derivadas y cuerpos vacíos de `thing`"
---
# ADR-084 — Especialización de aliases, miembros heredados y vistas derivadas

- Modificada por: [[ADR-103-inner-capability-in-derived-values|D-103]].

- Modificada por: [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]]
- Modificada por: [[ADR-086-exact-nominal-identity-external-arrows-and-algebra-de-diccionarios|D-086]]
- Modifica: [[notes/decisions/ADR-015-acyclic-specialisation-and-state-independent|D-015]], [[notes/decisions/ADR-018-as-declares-specialisation-in-is-the-query|D-018]], [[notes/decisions/ADR-019-mutability-orthogonal-to-collection-and-members|D-019]], [[notes/decisions/ADR-031-nominal-aliases-immutable-and-without-cycle-of-life|D-031]], [[notes/decisions/ADR-032-contextual-construction-and-nominal-casting-of-aliases|D-032]], [[notes/decisions/ADR-037-fields-and-declarative-domains|D-037]], [[notes/decisions/ADR-054-canonical-definitions-and-initial-activation|D-054]], [[notes/decisions/ADR-068-universal-thing-and-intrinsic-name|D-068]], [[notes/decisions/ADR-074-nominal-unions-and-type-narrowing|D-074]], [[notes/decisions/ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]] y [[notes/decisions/ADR-081-filtering-take-and-indexing-de-collectiones|D-081]].
- Reduce: [[notes/questions/Q-056-f-normalised-form-and-alias-recursion|Q-056]].
- Documentos afectados: gramática, AST superficial y resuelto, nombres y anclas, modelo matemático y semántica de colecciones derivadas.
- Modificada por: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].

## Contexto

Los aliases ya eran tipos nominales e inmutables, pero no estaba fijado cómo especializarlos, combinar representaciones heredadas ni heredar una forma estructural. Los campos derivados tampoco podían declarar de manera uniforme un contrato colectivo con capacidad interior propia. Además, la sintaxis exigía un cuerpo de `thing` incluso cuando estaba vacío.

## Decisión

### Especialización nominal

Todo alias puede declarar una lista no ordenada de antecesores mediante `as`. La relación directa debe ser acíclica y su clausura `is` es reflexiva, transitiva y antisimétrica. El orden escrito no introduce prioridad ni MRO.

Un alias nominal raíz introduce su representación con `:= Tipo`. Un descendiente puede omitirla cuando la representación heredada ya es única y compatible, o declarar `:= Tipo` para refinarla o resolver explícitamente varias contribuciones. La representación local debe refinar simultáneamente todas las representaciones heredadas relevantes. Una unión `A | B` no satisface por sí misma esta obligación.

Una declaración con antecesores puede omitir la definición local. `alias A` sin antecesores ni definición es inválido.

### Forma estructural heredada

Los aliases estructurales heredan componentes almacenados y campos derivados. El mismo miembro original alcanzado por varias rutas se deduplica por su ancla. Contribuciones independientes equivalentes del mismo nombre pueden fusionarse; si sus contratos difieren, el descendiente debe resolverlos explícitamente con un contrato que refine todos los heredados. No existe prioridad por orden de `as`.

Un descendiente puede sobrescribir el predeterminado de un componente almacenado heredado y refinar su contrato, pues los valores alias son exteriormente inmutables, siempre que el nuevo contrato refine todas las contribuciones heredadas. Los campos derivados de un único origen conservan su expresión definitoria y pueden refinar su contrato. Si dos campos derivados independientes homónimos aportan expresiones distintas, el descendiente debe proporcionar una nueva definición derivada explícita cuyo contrato satisfaga todas las contribuciones.

Los miembros pertenecen al tipo nominal del alias. Una estructura desnuda no los obtiene por coincidencia estructural; debe adquirir el alias por contexto o mediante `to`.

### Campos y colecciones derivadas

Un alias estructural puede declarar campos derivados con `:=`. Son puros, no almacenados y no asignables. El tipo nominal o estructural explícito se comprueba estáticamente. Dominio, cardinalidad, unicidad y orden declarados en la forma derivada, exista o no tipo explícito, son coercitivos sobre el resultado y siguen la normalización de transformaciones locales. `[mut]` actúa como obligación de capacidad sobre las `thing` miembros inmediatos: puede conservar autoridad del origen cuando se preserva identidad semántica, pero no fabricarla.

La selección se mantiene fija durante una instantánea de evaluación. Tras consolidar los efectos, la vista se recalcula sobre el nuevo estado y se validan sus contratos; un incumplimiento produce `failed` y rollback. Una colección almacenada no se autopoda ni recalcula su pertenencia.

### Cuerpos vacíos de `thing`

El cuerpo de una `thing` puede omitirse cuando no contiene miembros. `thing A`, `thing A {}` y `thing A;` producen el mismo AST e IR, aunque la CST conserva la forma escrita.

## Alternativas

Se rechaza interpretar el orden de antecesores como prioridad, resolver la especialización múltiple mediante unión, fusionar miembros independientes incompatibles solo por nombre o fabricar capacidad interior mediante una coerción derivada.

## Consecuencias

- El grafo nominal incorpora aristas de especialización entre aliases.
- La elaboración calcula representaciones y miembros efectivos antes de habilitar el acceso nominal.
- La CST, los AST y los catálogos sintácticos representan antecesores, definiciones opcionales, campos derivados y sobrescrituras.
- [[notes/questions/Q-056-f-normalised-form-and-alias-recursion|Q-056]] queda limitada a normalización y recursión de aliases.

## Verificación

1. Aceptación de especialización simple y múltiple, y rechazo de ciclos.
2. Herencia de representación y resolución explícita mediante `:=` cuando varias contribuciones difieren, exigiendo refinamiento común.
3. Deduplicación de diamantes por origen, fusión de contribuciones independientes equivalentes y resolución explícita de contratos distintos.
4. Herencia de componentes y derivados, con sobrescritura de predeterminados, refinamientos sustituibles y nueva definición explícita ante colisión de expresiones derivadas independientes.
5. Acceso a miembros solo después de adquirir el tipo nominal.
6. Capacidad interior exigida y preservada por vistas derivadas sin fabricación de autoridad, y pertenencia estable durante cada instantánea.
7. Recálculo posterior, validación del contrato y rollback ante incumplimiento.
8. Equivalencia semántica de las tres formas vacías de `thing`.
