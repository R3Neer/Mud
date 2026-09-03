<!-- Archivo generado por tooling/decisions/manage_decisions.py. -->
<!-- No editar manualmente. -->

# Decisiones de MUD

Cada decisión tiene un ADR estable. El ciclo de vida y los metadatos se rigen
por [[governance/DECISIONS-POLICY|la política de decisiones]].

## Resumen

- Total: 99.
- Current: 98.
- Proposed: 0.
- Superseded: 1.
- Withdrawn: 0.
- Rejected: 0.

## Índice

| ID | Estado | Fecha | Decisión |
| --- | --- | --- | --- |
| D-001 | current | 2026-07-27 | [[notes/decisions/ADR-001-mud-as-a-source-semantics-really|`.mud` as a source semantics really]] |
| D-002 | current | 2026-07-27 | [[notes/decisions/ADR-002-mud-describes-domain-not-application-architecture|MUD describes domain, not application architecture]] |
| D-003 | current | 2026-07-27 | [[notes/decisions/ADR-003-mud-is-a-formal-declarative-language|MUD is a formal declarative language]] |
| D-006 | current | 2026-07-27 | [[notes/decisions/ADR-006-purity-boolean-rules-and-write-boundary|Purity Boolean rules and write boundary]] |
| D-007 | current | 2026-07-27 | [[notes/decisions/ADR-007-causal-resolution-by-waves-over-snapshots|Causal resolution by waves over snapshots]] |
| D-008 | current | 2026-07-27 | [[notes/decisions/ADR-008-results-accepted-rejected-and-failed|Results `accepted`, `rejected` y `failed`]] |
| D-009 | current | 2026-07-27 | [[notes/decisions/ADR-009-allowed-as-a-baseless-rumour|`allowed` as a baseless rumour]] |
| D-010 | current | 2026-07-27 | [[notes/decisions/ADR-010-finiteness-and-termination-required-by-eventually|Finiteness y termination required by `eventually`]] |
| D-011 | current | 2026-07-27 | [[notes/decisions/ADR-011-derivatives-do-not-add-behaviour-of-domain|Derivatives do not add behaviour of domain]] |
| D-012 | current | 2026-07-27 | [[notes/decisions/ADR-012-validation-and-atomic-versioning-of-semantic-changes|Validation and atomic versioning of semantic changes]] |
| D-013 | current | 2026-07-27 | [[notes/decisions/ADR-013-complete-formalisation-before-continuing-with-implementation|Complete formalisation before continuing with implementation]] |
| D-014 | current | 2026-07-27 | [[notes/decisions/ADR-014-unified-ontology-of-thing|Unified ontology of `thing`]] |
| D-015 | current | 2026-07-27 | [[notes/decisions/ADR-015-acyclic-specialisation-and-state-independent|Acyclic specialisation and state independent]] |
| D-017 | current | 2026-07-27 | [[notes/decisions/ADR-017-everything-type-well-built-has-default-value|Everything type well-built has default value]] |
| D-018 | current | 2026-07-27 | [[notes/decisions/ADR-018-as-declares-specialisation-in-is-the-query|`as` declares specialisation in `is` the query]] |
| D-019 | current | 2026-07-27 | [[notes/decisions/ADR-019-mutability-orthogonal-to-collection-and-members|Mutability orthogonal to collection and members]] |
| D-021 | current | 2026-07-27 | [[notes/decisions/ADR-021-cycle-logical-lifespan-and-suspension-by-department|Cycle logical lifespan and suspension by department]] |
| D-022 | current | 2026-07-27 | [[notes/decisions/ADR-022-structural-deletion-of-inactive-boolean-rules|Structural deletion of inactive Boolean rules]] |
| D-023 | current | 2026-07-27 | [[notes/decisions/ADR-023-consolidation-of-concurrent-structural-effects|Consolidation of concurrent structural effects]] |
| D-025 | current | 2026-07-27 | [[notes/decisions/ADR-025-vocabulary-from-thing-headings-and-sections|Vocabulary from `thing`, headings and sections]] |
| D-026 | current | 2026-07-27 | [[notes/decisions/ADR-026-membership-strict-and-cardinality-by-then|Membership strict and cardinality by `then`]] |
| D-027 | superseded | 2026-07-27 | [[notes/decisions/ADR-027-departures-from-the-model-by-means-of-look-and-message|Departures from the model by means of `look` y `message`]] |
| D-028 | current | 2026-07-28 | [[notes/decisions/ADR-028-system-of-quantities-and-units|System of quantities and units]] |
| D-029 | current | 2026-07-28 | [[notes/decisions/ADR-029-intervals-effective-limits-and-cycles-of-point|Intervals, effective limits and cycles of point]] |
| D-030 | current | 2026-07-28 | [[notes/decisions/ADR-030-explicit-quantitative-conversion-using-to|Explicit quantitative conversion using `to`]] |
| D-031 | current | 2026-07-28 | [[notes/decisions/ADR-031-nominal-aliases-immutable-and-without-cycle-of-life|Nominal aliases, immutable and without cycle of life]] |
| D-032 | current | 2026-07-28 | [[notes/decisions/ADR-032-contextual-construction-and-nominal-casting-of-aliases|Contextual construction and nominal casting of aliases]] |
| D-033 | current | 2026-07-28 | [[notes/decisions/ADR-033-composite-keys-and-alias-enumeration|Composite keys and alias enumeration]] |
| D-034 | current | 2026-07-28 | [[notes/decisions/ADR-034-num-exactly-and-rum-binary64|`Num` exactly and `Rum` binary64]] |
| D-035 | current | 2026-07-28 | [[notes/decisions/ADR-035-organisation-names-using-and-anchors|Organisation, names, `using` and anchors]] |
| D-036 | current | 2026-07-28 | [[notes/decisions/ADR-036-participants-recipients-and-calls|Participants, recipients and calls]] |
| D-037 | current | 2026-07-28 | [[notes/decisions/ADR-037-fields-and-declarative-domains|Fields and declarative domains]] |
| D-038 | current | 2026-07-28 | [[notes/decisions/ADR-038-close-knit-families-with-strong-values|Close-knit families with strong values]] |
| D-039 | current | 2026-07-28 | [[notes/decisions/ADR-039-collections-and-dictionaries|Collections and dictionaries]] |
| D-040 | current | 2026-07-28 | [[notes/decisions/ADR-040-semantics-remaining-basic-numeracy|Semantics remaining basic numeracy]] |
| D-041 | current | 2026-07-28 | [[notes/decisions/ADR-041-contracts-under-the-three-types-of-rules|Contracts under the three types of rules]] |
| D-042 | current | 2026-07-28 | [[notes/decisions/ADR-042-shares-root-and-results|Shares, root and results]] |
| D-043 | current | 2026-07-28 | [[notes/decisions/ADR-043-consulta-especulativa-allowed|Consulta especulativa `allowed`]] |
| D-044 | current | 2026-07-28 | [[notes/decisions/ADR-044-alcanzabilidad-eventually|Alcanzabilidad `eventually`]] |
| D-045 | current | 2026-07-28 | [[notes/decisions/ADR-045-causal-resolution-connections-and-queue|Causal resolution, connections and queue]] |
| D-046 | current | 2026-07-28 | [[notes/decisions/ADR-046-algebra-and-conflicts-of-effects|Algebra and conflicts of effects]] |
| D-047 | current | 2026-07-28 | [[notes/decisions/ADR-047-quantifiers-and-finite-iteration|Quantifiers and finite iteration]] |
| D-048 | current | 2026-07-28 | [[notes/decisions/ADR-048-reproducible-randomness-and-errors|Reproducible randomness and errors]] |
| D-049 | current | 2026-07-28 | [[notes/decisions/ADR-049-operators-precedence-and-standardised-intervals|Operators, precedence and standardised intervals]] |
| D-050 | current | 2026-07-28 | [[notes/decisions/ADR-050-comments-terminators-text-and-numeric-separators|Comments, terminators, text and numeric separators]] |
| D-051 | current | 2026-07-28 | [[notes/decisions/ADR-051-graph-future-semantics-and-reconstructable-information|Graph future semantics and reconstructable information]] |
| D-052 | current | 2026-07-28 | [[notes/decisions/ADR-052-pipelines-renderers-and-conformance|Pipelines, renderers and conformance]] |
| D-053 | current | 2026-07-28 | [[notes/decisions/ADR-053-operador-semantico-and-flujo-de-autoria|Operador semántico y flujo de autoría]] |
| D-054 | current | 2026-07-28 | [[notes/decisions/ADR-054-canonical-definitions-and-initial-activation|Canonical definitions and initial activation]] |
| D-055 | current | 2026-07-28 | [[notes/decisions/ADR-055-declarative-and-diagnostic-tests-otherwise|Declarative and diagnostic tests `otherwise`]] |
| D-056 | current | 2026-07-28 | [[notes/decisions/ADR-056-char-text-and-unicode-ordering|`Char`, `Text` and Unicode ordering]] |
| D-057 | current | 2026-07-28 | [[notes/decisions/ADR-057-concrete-grammar-precedence-and-continuation|Concrete grammar, precedence and continuation]] |
| D-058 | current | 2026-07-29 | [[notes/decisions/ADR-058-temporal-triggers-changes-and-reactive-old|Temporal triggers, `changes` and reactive `old`]] |
| D-059 | current | 2026-07-29 | [[notes/decisions/ADR-059-magnitude-intervals-and-inverted-endpoints|Magnitude intervals and inverted endpoints]] |
| D-060 | current | 2026-07-29 | [[notes/decisions/ADR-060-additive-deltas-and-nat-normalisation|Additive deltas and `Nat` normalisation]] |
| D-061 | current | 2026-07-29 | [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|Non-accepted results and `Text` templates]] |
| D-062 | current | 2026-07-29 | [[notes/decisions/ADR-062-canonical-point-magnitude-literals|Canonical point-magnitude literals]] |
| D-063 | current | 2026-07-30 | [[notes/decisions/ADR-063-signatures-given-and-joint-on-bindings|Signatures, `given` and joint `on` bindings]] |
| D-064 | current | 2026-07-30 | [[notes/decisions/ADR-064-ordering-by-stable-path|Ordering by stable path]] |
| D-065 | current | 2026-07-30 | [[notes/decisions/ADR-065-file-level-using-header|File-level `using` header]] |
| D-066 | current | 2026-07-30 | [[notes/decisions/ADR-066-static-values-and-local-bindings-in-then|Static values and local bindings in `then`]] |
| D-067 | current | 2026-08-02 | [[notes/decisions/ADR-067-short-names-for-numeric-types|Short names for numeric types]] |
| D-068 | current | 2026-08-02 | [[notes/decisions/ADR-068-universal-thing-and-intrinsic-name|Universal `Thing` and intrinsic name]] |
| D-069 | current | 2026-08-02 | [[notes/decisions/ADR-069-char-literals-with-double-quotes|`Char` literals with double quotes]] |
| D-070 | current | 2026-08-02 | [[notes/decisions/ADR-070-lossless-cst-and-normalised-surface-ast|Lossless CST and normalised surface AST]] |
| D-071 | current | 2026-08-02 | [[notes/decisions/ADR-071-local-bindings-in-boolean-blocks|Local bindings in Boolean blocks]] |
| D-072 | current | 2026-08-02 | [[notes/decisions/ADR-072-resolution-environments-and-explicit-anchor-migrations|Resolution environments and explicit anchor migrations]] |
| D-073 | current | 2026-08-02 | [[notes/decisions/ADR-073-explicit-but-redundant-as-thing|Explicit but redundant `as Thing`]] |
| D-074 | current | 2026-08-03 | [[notes/decisions/ADR-074-nominal-unions-and-type-narrowing|Nominal unions and type narrowing]] |
| D-075 | current | 2026-08-03 | [[notes/decisions/ADR-075-enumerable-domains-all-and-derived-value-form|Enumerable domains, `all` and derived-value form]] |
| D-076 | current | 2026-08-03 | [[notes/decisions/ADR-076-named-units-prefixes-and-adjacent-notation|Named units, prefixes and adjacent notation]] |
| D-077 | current | 2026-08-03 | [[notes/decisions/ADR-077-cardinality-conditioned-destruction-and-transition-diagnostics|Cardinality-conditioned destruction and transition diagnostics]] |
| D-078 | current | 2026-08-03 | [[notes/decisions/ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|Nominal resolution, anchor catalogue and initial graph]] |
| D-079 | current | 2026-08-04 | [[notes/decisions/ADR-079-diagnostico-exterior-de-reglas-always|Diagnóstico exterior de reglas `always`]] |
| D-080 | current | 2026-08-04 | [[notes/decisions/ADR-080-algebra-elevada-and-actualizaciones-de-coleccion|Álgebra elevada y actualizaciones de colección]] |
| D-081 | current | 2026-08-04 | [[notes/decisions/ADR-081-filtrado-take-and-indexacion-de-colecciones|Filtrado, `take` e indexación de colecciones]] |
| D-082 | current | 2026-08-04 | [[notes/decisions/ADR-082-cycle-como-modificador-de-dominio-de-punto|`cycle` como modificador de dominio de punto]] |
| D-083 | current | 2026-08-04 | [[notes/decisions/ADR-083-magnitudes-base-sin-unidades|Magnitudes base sin unidades]] |
| D-084 | current | 2026-08-04 | [[notes/decisions/ADR-084-especializacion-de-aliases-miembros-heredados-and-vistas-derivadas|Especialización de aliases, miembros heredados y vistas derivadas]] |
| D-085 | current | 2026-08-05 | [[notes/decisions/ADR-085-diccionarios-funcionales-metadatos-and-activacion-estructurada|Diccionarios funcionales, metadatos y activación estructurada]] |
| D-086 | current | 2026-08-05 | [[notes/decisions/ADR-086-identidad-nominal-exacta-flechas-exteriores-and-algebra-de-diccionarios|Identidad nominal exacta, flechas exteriores y álgebra de diccionarios]] |
| D-087 | current | 2026-08-15 | [[notes/decisions/ADR-087-metadatos-reflectivos-descriptores-estables-and-visibilidad-exterior|Metadatos reflectivos, descriptores estables y visibilidad exterior]] |
| D-088 | current | 2026-08-15 | [[notes/decisions/ADR-088-iteracion-progresiones-firmadas-and-bloques-de-expresion|Iteración, progresiones firmadas y bloques de expresión]] |
| D-089 | current | 2026-08-16 | [[notes/decisions/ADR-089-clasificacion-contextual-de-formas-fuente-sin-dependencia-circular-del-scanner|Clasificación contextual de formas fuente sin dependencia circular del scanner]] |
| D-090 | current | 2026-08-16 | [[notes/decisions/ADR-090-ramas-funcionales-sin-ancla-publica|Ramas funcionales sin ancla pública]] |
| D-091 | current | 2026-08-16 | [[notes/decisions/ADR-091-datos-de-family-como-descriptores-anclados|Datos de family como descriptores anclados]] |
| D-092 | current | 2026-08-16 | [[notes/decisions/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas|Disponibilidad estática de propiedades reflectivas]] |
| D-093 | current | 2026-08-16 | [[notes/decisions/ADR-093-ast-superficial-hir-nominal-and-fase-semantica-posterior|AST superficial, HIR nominal y fase semántica posterior]] |
| D-094 | current | 2026-08-16 | [[notes/decisions/ADR-094-anclas-terminales-de-metadatos-configurados|Anclas terminales de metadatos configurados]] |
| D-095 | current | 2026-08-16 | [[notes/decisions/ADR-095-extremos-vacios-como-ausencia-ordinaria|Extremos vacíos como ausencia ordinaria]] |
| D-096 | current | 2026-08-28 | [[notes/decisions/ADR-096-modulos-callables-look-message-and-activacion|Módulos, callables, `look`, `message` y activación]] |
| D-097 | current | 2026-08-28 | [[notes/decisions/ADR-097-hir-nominal-vigente-and-ir-semantico-diferido|HIR nominal vigente e IR semántico diferido]] |
| D-098 | current | 2026-08-28 | [[notes/decisions/ADR-098-rutas-asignables-and-write-back-de-aliases-inmutables|Rutas asignables y write-back de aliases inmutables]] |
| D-099 | current | 2026-08-28 | [[notes/decisions/ADR-099-materializaciones-frescas-tras-destroy-and-create|Materializaciones frescas tras `destroy` y `create`]] |
| D-100 | current | 2026-08-29 | [[notes/decisions/ADR-100-orden-logico-procedencia-pertenencia-and-consolidacion-de-efectos|Orden lógico, procedencia, pertenencia y consolidación de efectos]] |
| D-101 | current | 2026-08-29 | [[notes/decisions/ADR-101-bloques-de-valor-variables-locales-almacenadas-and-extremos-por-testigos|Bloques de valor, variables locales almacenadas y extremos por testigos]] |
| D-102 | current | 2026-08-29 | [[notes/decisions/ADR-102-forma-completa-de-datos-calculados-de-family|Forma completa de datos calculados de family]] |
| D-103 | current | 2026-08-29 | [[notes/decisions/ADR-103-capacidad-interior-en-valores-derivados|Capacidad interior en valores derivados]] |
| D-104 | current | 2026-09-02 | [[notes/decisions/ADR-104-ingles-britanico-para-la-migracion-editorial|Inglés británico para la migración editorial]] |

## Identificadores reservados

No contienen una decisión recuperable y no pueden reutilizarse:

`D-004`, `D-005`, `D-016`, `D-020`, `D-024`.

## Regeneración

```powershell
python tooling/decisions/manage_decisions.py generate
python tooling/decisions/manage_decisions.py validate
```
