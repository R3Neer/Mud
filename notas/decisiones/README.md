<!-- Archivo generado por tooling/decisions/manage_decisions.py. -->
<!-- No editar manualmente. -->

# Decisiones de MUD

Cada decisión tiene un ADR estable. El ciclo de vida y los metadatos se rigen
por [[gobierno/POLITICA-DE-DECISIONES|la política de decisiones]].

## Resumen

- Total: 99.
- Vigentes: 98.
- Propuestas: 0.
- Sustituidas: 1.
- Retiradas: 0.
- Rechazadas: 0.

## Índice

| ID | Estado | Fecha | Decisión |
| --- | --- | --- | --- |
| D-001 | vigente | 2026-07-27 | [[notas/decisiones/ADR-001-fuente-semantica-mud|`.mud` as a source semantics really]] |
| D-002 | vigente | 2026-07-27 | [[notas/decisiones/ADR-002-dominio-no-arquitectura-de-aplicacion|MUD describes domain, not application architecture]] |
| D-003 | vigente | 2026-07-27 | [[notas/decisiones/ADR-003-lenguaje-declarativo-formal|MUD is a formal declarative language]] |
| D-006 | vigente | 2026-07-27 | [[notas/decisiones/ADR-006-pureza-y-frontera-de-escritura|Purity Boolean rules and write boundary]] |
| D-007 | vigente | 2026-07-27 | [[notas/decisiones/ADR-007-ondas-sobre-instantaneas|Causal resolution by waves over snapshots]] |
| D-008 | vigente | 2026-07-27 | [[notas/decisiones/ADR-008-resultados-de-accion|Results `accepted`, `rejected` y `failed`]] |
| D-009 | vigente | 2026-07-27 | [[notas/decisiones/ADR-009-consulta-allowed-descartable|`allowed` as a baseless rumour]] |
| D-010 | vigente | 2026-07-27 | [[notas/decisiones/ADR-010-admisibilidad-de-eventually|Finiteness y termination required by `eventually`]] |
| D-011 | vigente | 2026-07-27 | [[notas/decisiones/ADR-011-derivados-sin-semantica-adicional|Derivatives do not add behaviour of domain]] |
| D-012 | vigente | 2026-07-27 | [[notas/decisiones/ADR-012-cambios-semanticos-atomicos|Validation and atomic versioning of semantic changes]] |
| D-013 | vigente | 2026-07-27 | [[notas/decisiones/ADR-013-formalizacion-completa-antes-de-implementar|Complete formalisation before continuing with implementation]] |
| D-014 | vigente | 2026-07-27 | [[notas/decisiones/ADR-014-ontologia-unificada-de-things|Unified ontology of `thing`]] |
| D-015 | vigente | 2026-07-27 | [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|Acyclic specialisation and state independent]] |
| D-017 | vigente | 2026-07-27 | [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|Everything type well-built has default value]] |
| D-018 | vigente | 2026-07-27 | [[notas/decisiones/ADR-018-as-declara-is-consulta|`as` declares specialisation in `is` the query]] |
| D-019 | vigente | 2026-07-27 | [[notas/decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|Mutability orthogonal to collection and members]] |
| D-021 | vigente | 2026-07-27 | [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|Cycle logical lifespan and suspension by department]] |
| D-022 | vigente | 2026-07-27 | [[notas/decisiones/ADR-022-borrado-de-reglas-booleanas-inactivas|Structural deletion of inactive Boolean rules]] |
| D-023 | vigente | 2026-07-27 | [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|Consolidation of concurrent structural effects]] |
| D-025 | vigente | 2026-07-27 | [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|Vocabulary from `thing`, headings and sections]] |
| D-026 | vigente | 2026-07-27 | [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|Membership strict and cardinality by `then`]] |
| D-027 | sustituida | 2026-07-27 | [[notas/decisiones/ADR-027-salidas-look-y-message|Departures from the model by means of `look` y `message`]] |
| D-028 | vigente | 2026-07-28 | [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|System of quantities and units]] |
| D-029 | vigente | 2026-07-28 | [[notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos|Intervals, effective limits and cycles of point]] |
| D-030 | vigente | 2026-07-28 | [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|Explicit quantitative conversion using `to`]] |
| D-031 | vigente | 2026-07-28 | [[notas/decisiones/ADR-031-aliases-nominales-e-inmutables|Nominal aliases, immutable and without cycle of life]] |
| D-032 | vigente | 2026-07-28 | [[notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal|Contextual construction and nominal casting of aliases]] |
| D-033 | vigente | 2026-07-28 | [[notas/decisiones/ADR-033-claves-y-enumeracion-de-aliases|Composite keys and alias enumeration]] |
| D-034 | vigente | 2026-07-28 | [[notas/decisiones/ADR-034-number-exacto-y-rumber-binary64|`Num` exactly and `Rum` binary64]] |
| D-035 | vigente | 2026-07-28 | [[notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas|Organisation, names, `using` and anchors]] |
| D-036 | vigente | 2026-07-28 | [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|Participants, recipients and calls]] |
| D-037 | vigente | 2026-07-28 | [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|Fields and declarative domains]] |
| D-038 | vigente | 2026-07-28 | [[notas/decisiones/ADR-038-familias-cerradas-de-valores|Close-knit families with strong values]] |
| D-039 | vigente | 2026-07-28 | [[notas/decisiones/ADR-039-colecciones-y-diccionarios|Collections and dictionaries]] |
| D-040 | vigente | 2026-07-28 | [[notas/decisiones/ADR-040-semantica-numerica-basica-restante|Semantics remaining basic numeracy]] |
| D-041 | vigente | 2026-07-28 | [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|Contracts under the three types of rules]] |
| D-042 | vigente | 2026-07-28 | [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|Shares, root and results]] |
| D-043 | vigente | 2026-07-28 | [[notas/decisiones/ADR-043-consulta-especulativa-allowed|Consulta especulativa `allowed`]] |
| D-044 | vigente | 2026-07-28 | [[notas/decisiones/ADR-044-alcanzabilidad-eventually|Alcanzabilidad `eventually`]] |
| D-045 | vigente | 2026-07-28 | [[notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola|Causal resolution, connections and queue]] |
| D-046 | vigente | 2026-07-28 | [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|Algebra and conflicts of effects]] |
| D-047 | vigente | 2026-07-28 | [[notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita|Quantifiers and finite iteration]] |
| D-048 | vigente | 2026-07-28 | [[notas/decisiones/ADR-048-azar-reproducible-y-fallos|Reproducible randomness and errors]] |
| D-049 | vigente | 2026-07-28 | [[notas/decisiones/ADR-049-operadores-precedencia-e-intervalos-normalizados|Operators, precedence and standardised intervals]] |
| D-050 | vigente | 2026-07-28 | [[notas/decisiones/ADR-050-comentarios-terminadores-y-separadores-numericos|Comments, terminators, text and numeric separators]] |
| D-051 | vigente | 2026-07-28 | [[notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles|Graph future semantics and reconstructable information]] |
| D-052 | vigente | 2026-07-28 | [[notas/decisiones/ADR-052-pipeline-materializadores-y-conformidad|Pipelines, renderers and conformance]] |
| D-053 | vigente | 2026-07-28 | [[notas/decisiones/ADR-053-operador-semantico-y-flujo-de-autoria|Operador semántico y flujo de autoría]] |
| D-054 | vigente | 2026-07-28 | [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|Canonical definitions and initial activation]] |
| D-055 | vigente | 2026-07-28 | [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|Declarative and diagnostic tests `otherwise`]] |
| D-056 | vigente | 2026-07-28 | [[notas/decisiones/ADR-056-char-texto-y-orden-unicode|`Char`, `Text` and Unicode ordering]] |
| D-057 | vigente | 2026-07-28 | [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|Concrete grammar, precedence and continuation]] |
| D-058 | vigente | 2026-07-29 | [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|Temporal triggers, `changes` and reactive `old`]] |
| D-059 | vigente | 2026-07-29 | [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|Magnitude intervals and inverted endpoints]] |
| D-060 | vigente | 2026-07-29 | [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|Additive deltas and `Nat` normalisation]] |
| D-061 | vigente | 2026-07-29 | [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|Non-accepted results and `Text` templates]] |
| D-062 | vigente | 2026-07-29 | [[notas/decisiones/ADR-062-literales-canonicos-de-magnitudes-de-punto|Canonical point-magnitude literals]] |
| D-063 | vigente | 2026-07-30 | [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|Signatures, `given` and joint `on` bindings]] |
| D-064 | vigente | 2026-07-30 | [[notas/decisiones/ADR-064-orden-por-ruta-estable|Ordering by stable path]] |
| D-065 | vigente | 2026-07-30 | [[notas/decisiones/ADR-065-cabecera-using-de-fichero|File-level `using` header]] |
| D-066 | vigente | 2026-07-30 | [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|Static values and local bindings in `then`]] |
| D-067 | vigente | 2026-08-02 | [[notas/decisiones/ADR-067-nombres-breves-de-tipos-numericos|Nombres breves de los tipos numéricos]] |
| D-068 | vigente | 2026-08-02 | [[notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco|`Thing` universal y nombre intrínseco]] |
| D-069 | vigente | 2026-08-02 | [[notas/decisiones/ADR-069-literales-char-con-comillas-dobles|Literales `Char` con comillas dobles]] |
| D-070 | vigente | 2026-08-02 | [[notas/decisiones/ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|CST sin pérdidas y AST superficial normalizado]] |
| D-071 | vigente | 2026-08-02 | [[notas/decisiones/ADR-071-vinculaciones-locales-en-bloques-booleanos|Vinculaciones locales en bloques booleanos]] |
| D-072 | vigente | 2026-08-02 | [[notas/decisiones/ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas|Entornos de resolución y migraciones explícitas de anclas]] |
| D-073 | vigente | 2026-08-02 | [[notas/decisiones/ADR-073-as-thing-explicito-redundante|`as Thing` explícito válido pero redundante]] |
| D-074 | vigente | 2026-08-03 | [[notas/decisiones/ADR-074-uniones-nominales-y-estrechamiento|Uniones nominales y estrechamiento de tipos]] |
| D-075 | vigente | 2026-08-03 | [[notas/decisiones/ADR-075-dominios-enumerables-all-y-valores-derivados|Dominios enumerables, `all` y forma de valores derivados]] |
| D-076 | vigente | 2026-08-03 | [[notas/decisiones/ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|Unidades nombradas, prefijos y escritura adyacente]] |
| D-077 | vigente | 2026-08-03 | [[notas/decisiones/ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|Destrucción condicionada por cardinalidad y diagnóstico de transición]] |
| D-078 | vigente | 2026-08-03 | [[notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial|Resolución nominal, catálogo de anclas y grafo inicial]] |
| D-079 | vigente | 2026-08-04 | [[notas/decisiones/ADR-079-diagnostico-exterior-de-reglas-always|Diagnóstico exterior de reglas `always`]] |
| D-080 | vigente | 2026-08-04 | [[notas/decisiones/ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|Álgebra elevada y actualizaciones de colección]] |
| D-081 | vigente | 2026-08-04 | [[notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones|Filtrado, `take` e indexación de colecciones]] |
| D-082 | vigente | 2026-08-04 | [[notas/decisiones/ADR-082-cycle-como-modificador-de-dominio-de-punto|`cycle` como modificador de dominio de punto]] |
| D-083 | vigente | 2026-08-04 | [[notas/decisiones/ADR-083-magnitudes-base-sin-unidades|Magnitudes base sin unidades]] |
| D-084 | vigente | 2026-08-04 | [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|Especialización de aliases, miembros heredados y vistas derivadas]] |
| D-085 | vigente | 2026-08-05 | [[notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|Diccionarios funcionales, metadatos y activación estructurada]] |
| D-086 | vigente | 2026-08-05 | [[notas/decisiones/ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|Identidad nominal exacta, flechas exteriores y álgebra de diccionarios]] |
| D-087 | vigente | 2026-08-15 | [[notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|Metadatos reflectivos, descriptores estables y visibilidad exterior]] |
| D-088 | vigente | 2026-08-15 | [[notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion|Iteración, progresiones firmadas y bloques de expresión]] |
| D-089 | vigente | 2026-08-16 | [[notas/decisiones/ADR-089-clasificacion-contextual-de-formas-fuente|Clasificación contextual de formas fuente sin dependencia circular del scanner]] |
| D-090 | vigente | 2026-08-16 | [[notas/decisiones/ADR-090-ramas-funcionales-sin-ancla-publica|Ramas funcionales sin ancla pública]] |
| D-091 | vigente | 2026-08-16 | [[notas/decisiones/ADR-091-datos-de-family-como-descriptores-anclados|Datos de family como descriptores anclados]] |
| D-092 | vigente | 2026-08-16 | [[notas/decisiones/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas|Disponibilidad estática de propiedades reflectivas]] |
| D-093 | vigente | 2026-08-16 | [[notas/decisiones/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|AST superficial, HIR nominal y fase semántica posterior]] |
| D-094 | vigente | 2026-08-16 | [[notas/decisiones/ADR-094-anclas-terminales-de-metadatos-configurados|Anclas terminales de metadatos configurados]] |
| D-095 | vigente | 2026-08-16 | [[notas/decisiones/ADR-095-extremos-vacios-como-ausencia-ordinaria|Extremos vacíos como ausencia ordinaria]] |
| D-096 | vigente | 2026-08-28 | [[notas/decisiones/ADR-096-modulos-callables-look-message-y-activacion|Módulos, callables, `look`, `message` y activación]] |
| D-097 | vigente | 2026-08-28 | [[notas/decisiones/ADR-097-hir-nominal-vigente-e-ir-semantico-diferido|HIR nominal vigente e IR semántico diferido]] |
| D-098 | vigente | 2026-08-28 | [[notas/decisiones/ADR-098-rutas-asignables-y-write-back-de-aliases|Rutas asignables y write-back de aliases inmutables]] |
| D-099 | vigente | 2026-08-28 | [[notas/decisiones/ADR-099-materializaciones-frescas-tras-destroy-create|Materializaciones frescas tras `destroy` y `create`]] |
| D-100 | vigente | 2026-08-29 | [[notas/decisiones/ADR-100-orden-procedencia-pertenencia-y-consolidacion|Orden lógico, procedencia, pertenencia y consolidación de efectos]] |
| D-101 | vigente | 2026-08-29 | [[notas/decisiones/ADR-101-bloques-de-valor-variables-locales-y-extremos|Bloques de valor, variables locales almacenadas y extremos por testigos]] |
| D-102 | vigente | 2026-08-29 | [[notas/decisiones/ADR-102-forma-completa-de-datos-calculados-de-family|Forma completa de datos calculados de family]] |
| D-103 | vigente | 2026-08-29 | [[notas/decisiones/ADR-103-capacidad-interior-en-valores-derivados|Capacidad interior en valores derivados]] |
| D-104 | vigente | 2026-09-02 | [[notas/decisiones/ADR-104-ingles-britanico-para-la-migracion|Inglés británico para la migración editorial]] |

## Identificadores reservados

No contienen una decisión recuperable y no pueden reutilizarse:

`D-004`, `D-005`, `D-016`, `D-020`, `D-024`.

## Regeneración

```powershell
python tooling/decisions/manage_decisions.py generate
python tooling/decisions/manage_decisions.py validate
```
