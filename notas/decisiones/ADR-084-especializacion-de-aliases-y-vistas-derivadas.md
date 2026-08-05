---
id: D-084
title: "Especialización de aliases, miembros heredados y vistas derivadas"
status: vigente
date: 2026-08-04
supersedes: []
superseded-by: []
questions:
  - Q-056
affects:
  - "aliases, gramática, sintaxis, resolución nominal, colecciones derivadas y cuerpos vacíos de `thing`"
---
# ADR-084 — Especialización de aliases, miembros heredados y vistas derivadas

- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Modifica: [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|D-015]], [[notas/decisiones/ADR-018-as-declara-is-consulta|D-018]], [[notas/decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|D-019]], [[notas/decisiones/ADR-031-aliases-nominales-e-inmutables|D-031]], [[notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal|D-032]], [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]], [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]], [[notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco|D-068]], [[notas/decisiones/ADR-074-uniones-nominales-y-estrechamiento|D-074]], [[notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]] y [[notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]].
- Reduce: [[notas/preguntas/Q-056-forma-normalizada-y-recursion-de-aliases|Q-056]].
- Documentos afectados: gramática, AST superficial y resuelto, nombres y anclas, modelo matemático y semántica de colecciones derivadas.

## Contexto

Los aliases ya eran tipos nominales e inmutables, pero no estaba fijado cómo especializarlos, combinar representaciones heredadas ni heredar una forma estructural. Los campos derivados tampoco podían declarar de manera uniforme un contrato colectivo con capacidad interior propia. Además, la sintaxis exigía un cuerpo de `thing` incluso cuando estaba vacío.

## Decisión

### Especialización nominal

Todo alias puede declarar una lista no ordenada de antecesores mediante `as`. La relación directa debe ser acíclica y su clausura `is` es reflexiva, transitiva y antisimétrica. El orden escrito no introduce prioridad ni MRO.

Un alias nominal raíz introduce su representación con `:= Tipo`. Un descendiente hereda la representación efectiva y no puede redeclararla. La especialización múltiple exige una intersección compatible de las representaciones de todas las antecesoras; una unión `A | B` no satisface esta obligación.

Una declaración con antecesores puede omitir la definición local. `alias A` sin antecesores ni definición es inválido.

### Forma estructural heredada

Los aliases estructurales heredan componentes almacenados y campos derivados. El mismo miembro original alcanzado por varias rutas se deduplica por su ancla; miembros independientes con el mismo nombre producen conflicto, aunque sean textualmente iguales.

Un descendiente puede sobrescribir únicamente el predeterminado de un componente almacenado heredado. No puede cambiar su tipo, dominio, cardinalidad, unicidad, orden o capacidad interior. Los campos derivados heredados no se redefinen.

Los miembros pertenecen al tipo nominal del alias. Una estructura desnuda no los obtiene por coincidencia estructural; debe adquirir el alias por contexto o mediante `to`.

### Campos y colecciones derivadas

Un alias estructural puede declarar campos derivados con `:=`. Son puros, no almacenados y no asignables. Pueden declarar tipo, dominio, cardinalidad, unicidad, orden y capacidad interior `[mut]` como contrato del resultado, no como transformación de la expresión.

La capacidad interior de una colección derivada pertenece a esa vista y es independiente de la fuente. Permite modificar las `thing` directamente contenidas, pero no la pertenencia de la colección derivada.

La selección se mantiene fija durante una instantánea de evaluación. Tras consolidar los efectos, la vista se recalcula sobre el nuevo estado y se validan sus contratos; un incumplimiento produce `failed` y rollback. Una colección almacenada no se autopoda ni recalcula su pertenencia.

### Cuerpos vacíos de `thing`

El cuerpo de una `thing` puede omitirse cuando no contiene miembros. `thing A`, `thing A {}` y `thing A;` producen el mismo AST e IR, aunque la CST conserva la forma escrita.

## Alternativas

Se rechaza interpretar el orden de antecesores como prioridad, resolver la especialización múltiple mediante unión, fusionar miembros independientes solo por nombre o propagar automáticamente la capacidad interior desde la fuente de una vista.

## Consecuencias

- El grafo nominal incorpora aristas de especialización entre aliases.
- La elaboración calcula representaciones y miembros efectivos antes de habilitar el acceso nominal.
- La CST, los AST y los catálogos sintácticos representan antecesores, definiciones opcionales, campos derivados y sobrescrituras.
- [[notas/preguntas/Q-056-forma-normalizada-y-recursion-de-aliases|Q-056]] queda limitada a normalización y recursión de aliases.

## Verificación

1. Aceptación de especialización simple y múltiple, y rechazo de ciclos.
2. Rechazo de representaciones nominales heredadas incompatibles o redeclaradas.
3. Deduplicación de diamantes por origen y diagnóstico de colisiones independientes.
4. Herencia de componentes y derivados, con sobrescritura exclusiva de predeterminados almacenados.
5. Acceso a miembros solo después de adquirir el tipo nominal.
6. Capacidad interior propia de vistas derivadas y pertenencia estable durante cada instantánea.
7. Recálculo posterior, validación del contrato y rollback ante incumplimiento.
8. Equivalencia semántica de las tres formas vacías de `thing`.
