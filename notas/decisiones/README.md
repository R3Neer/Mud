<!-- Archivo generado por tooling/decisions/manage_decisions.py. -->
<!-- No editar manualmente. -->

# Decisiones de MUD

Cada decisión tiene un ADR estable. El ciclo de vida y los metadatos se rigen
por [[gobierno/POLITICA-DE-DECISIONES|la política de decisiones]].

## Resumen

- Total: 91.
- Vigentes: 90.
- Propuestas: 0.
- Sustituidas: 1.
- Retiradas: 0.
- Rechazadas: 0.

## Índice

| ID | Estado | Fecha | Decisión |
| --- | --- | --- | --- |
| D-001 | vigente | 2026-07-27 | [[notas/decisiones/ADR-001-fuente-semantica-mud|`.mud` como fuente semántica de verdad]] |
| D-002 | vigente | 2026-07-27 | [[notas/decisiones/ADR-002-dominio-no-arquitectura-de-aplicacion|MUD describe dominio, no arquitectura de aplicación]] |
| D-003 | vigente | 2026-07-27 | [[notas/decisiones/ADR-003-lenguaje-declarativo-formal|MUD es un lenguaje declarativo formal]] |
| D-006 | vigente | 2026-07-27 | [[notas/decisiones/ADR-006-pureza-y-frontera-de-escritura|Pureza de reglas booleanas y frontera de escritura]] |
| D-007 | vigente | 2026-07-27 | [[notas/decisiones/ADR-007-ondas-sobre-instantaneas|Resolución causal por ondas sobre instantáneas]] |
| D-008 | vigente | 2026-07-27 | [[notas/decisiones/ADR-008-resultados-de-accion|Resultados `accepted`, `rejected` y `failed`]] |
| D-009 | vigente | 2026-07-27 | [[notas/decisiones/ADR-009-consulta-allowed-descartable|`allowed` como especulación descartable]] |
| D-010 | vigente | 2026-07-27 | [[notas/decisiones/ADR-010-admisibilidad-de-eventually|Finitud y terminación exigidas por `eventually`]] |
| D-011 | vigente | 2026-07-27 | [[notas/decisiones/ADR-011-derivados-sin-semantica-adicional|Los derivados no añaden comportamiento de dominio]] |
| D-012 | vigente | 2026-07-27 | [[notas/decisiones/ADR-012-cambios-semanticos-atomicos|Validación y versionado atómico de cambios semánticos]] |
| D-013 | vigente | 2026-07-27 | [[notas/decisiones/ADR-013-formalizacion-completa-antes-de-implementar|Formalización completa antes de continuar la implementación]] |
| D-014 | vigente | 2026-07-27 | [[notas/decisiones/ADR-014-ontologia-unificada-de-things|Ontología unificada de `thing`]] |
| D-015 | vigente | 2026-07-27 | [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|Especialización acíclica y estado independiente]] |
| D-017 | vigente | 2026-07-27 | [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|Todo tipo bien formado tiene valor predeterminado]] |
| D-018 | vigente | 2026-07-27 | [[notas/decisiones/ADR-018-as-declara-is-consulta|`as` declara especialización e `is` la consulta]] |
| D-019 | vigente | 2026-07-27 | [[notas/decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|Mutabilidad ortogonal de colección y miembros]] |
| D-021 | vigente | 2026-07-27 | [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|Ciclo de vida lógico y suspensión por dependencias]] |
| D-022 | vigente | 2026-07-27 | [[notas/decisiones/ADR-022-borrado-de-reglas-booleanas-inactivas|Borrado estructural de reglas booleanas inactivas]] |
| D-023 | vigente | 2026-07-27 | [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|Consolidación de efectos estructurales concurrentes]] |
| D-025 | vigente | 2026-07-27 | [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|Vocabulario de `thing`, cabeceras y bloques]] |
| D-026 | vigente | 2026-07-27 | [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|Membresía estricta y cardinalidad por `then`]] |
| D-027 | sustituida | 2026-07-27 | [[notas/decisiones/ADR-027-salidas-look-y-message|Salidas del modelo mediante `look` y `message`]] |
| D-028 | vigente | 2026-07-28 | [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|Sistema de magnitudes y unidades]] |
| D-029 | vigente | 2026-07-28 | [[notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos|Intervalos, límites efectivos y ciclos de punto]] |
| D-030 | vigente | 2026-07-28 | [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|Conversión cuantitativa explícita mediante `to`]] |
| D-031 | vigente | 2026-07-28 | [[notas/decisiones/ADR-031-aliases-nominales-e-inmutables|Aliases nominales, inmutables y sin ciclo de vida]] |
| D-032 | vigente | 2026-07-28 | [[notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal|Construcción contextual y casting nominal de aliases]] |
| D-033 | vigente | 2026-07-28 | [[notas/decisiones/ADR-033-claves-y-enumeracion-de-aliases|Claves compuestas y enumeración de aliases]] |
| D-034 | vigente | 2026-07-28 | [[notas/decisiones/ADR-034-number-exacto-y-rumber-binary64|`Num` exacto y `Rum` binary64]] |
| D-035 | vigente | 2026-07-28 | [[notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas|Organización, nombres, `using` y anclas]] |
| D-036 | vigente | 2026-07-28 | [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|Participantes, receptores y llamadas]] |
| D-037 | vigente | 2026-07-28 | [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|Campos y dominios declarativos]] |
| D-038 | vigente | 2026-07-28 | [[notas/decisiones/ADR-038-familias-cerradas-de-valores|Familias cerradas de valores]] |
| D-039 | vigente | 2026-07-28 | [[notas/decisiones/ADR-039-colecciones-y-diccionarios|Colecciones y diccionarios]] |
| D-040 | vigente | 2026-07-28 | [[notas/decisiones/ADR-040-semantica-numerica-basica-restante|Semántica numérica básica restante]] |
| D-041 | vigente | 2026-07-28 | [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|Contratos de las tres clases de regla]] |
| D-042 | vigente | 2026-07-28 | [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|Acciones, raíz y resultados]] |
| D-043 | vigente | 2026-07-28 | [[notas/decisiones/ADR-043-consulta-especulativa-allowed|Consulta especulativa `allowed`]] |
| D-044 | vigente | 2026-07-28 | [[notas/decisiones/ADR-044-alcanzabilidad-eventually|Alcanzabilidad `eventually`]] |
| D-045 | vigente | 2026-07-28 | [[notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola|Resolución causal, vinculaciones y cola]] |
| D-046 | vigente | 2026-07-28 | [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|Álgebra y conflictos de efectos]] |
| D-047 | vigente | 2026-07-28 | [[notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita|Cuantificadores e iteración finita]] |
| D-048 | vigente | 2026-07-28 | [[notas/decisiones/ADR-048-azar-reproducible-y-fallos|Azar reproducible y fallos]] |
| D-049 | vigente | 2026-07-28 | [[notas/decisiones/ADR-049-operadores-precedencia-e-intervalos-normalizados|Operadores, precedencia e intervalos normalizados]] |
| D-050 | vigente | 2026-07-28 | [[notas/decisiones/ADR-050-comentarios-terminadores-y-separadores-numericos|Comentarios, terminadores, texto y separadores numéricos]] |
| D-051 | vigente | 2026-07-28 | [[notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles|Grafo semántico e IR reconstruibles]] |
| D-052 | vigente | 2026-07-28 | [[notas/decisiones/ADR-052-pipeline-materializadores-y-conformidad|Pipeline, materializadores y conformidad]] |
| D-053 | vigente | 2026-07-28 | [[notas/decisiones/ADR-053-operador-semantico-y-flujo-de-autoria|Operador semántico y flujo de autoría]] |
| D-054 | vigente | 2026-07-28 | [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|Definiciones canónicas y activación inicial]] |
| D-055 | vigente | 2026-07-28 | [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|Tests declarativos y diagnósticos `otherwise`]] |
| D-056 | vigente | 2026-07-28 | [[notas/decisiones/ADR-056-char-texto-y-orden-unicode|`Char`, `Text` y orden Unicode]] |
| D-057 | vigente | 2026-07-28 | [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|Gramática concreta, precedencia y continuación]] |
| D-058 | vigente | 2026-07-29 | [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|Activadores temporales, `changes` y `old` reactivo]] |
| D-059 | vigente | 2026-07-29 | [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|Intervalos de magnitud y extremos invertidos]] |
| D-060 | vigente | 2026-07-29 | [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|Deltas aditivos y normalización de `Nat`]] |
| D-061 | vigente | 2026-07-29 | [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|Resultados no aceptados y plantillas `Text`]] |
| D-062 | vigente | 2026-07-29 | [[notas/decisiones/ADR-062-literales-canonicos-de-magnitudes-de-punto|Literales canónicos de magnitudes de punto]] |
| D-063 | vigente | 2026-07-30 | [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|Firmas, `given` y vinculaciones `on` conjuntas]] |
| D-064 | vigente | 2026-07-30 | [[notas/decisiones/ADR-064-orden-por-ruta-estable|Orden por ruta estable]] |
| D-065 | vigente | 2026-07-30 | [[notas/decisiones/ADR-065-cabecera-using-de-fichero|Cabecera `using` de fichero]] |
| D-066 | vigente | 2026-07-30 | [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|Valores estáticos y vinculaciones locales en `then`]] |
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
| D-085 | vigente | 2026-08-05 | [[notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|Diccionarios decisionales, metadatos y activación estructurada]] |
| D-086 | vigente | 2026-08-05 | [[notas/decisiones/ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|Identidad nominal exacta, flechas exteriores y álgebra de diccionarios]] |
| D-087 | vigente | 2026-08-15 | [[notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|Metadatos reflectivos, descriptores estables y visibilidad exterior]] |
| D-088 | vigente | 2026-08-15 | [[notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion|Iteración, progresiones firmadas y bloques de expresión]] |
| D-089 | vigente | 2026-08-16 | [[notas/decisiones/ADR-089-clasificacion-contextual-de-formas-fuente|Clasificación contextual de formas fuente sin dependencia circular del scanner]] |
| D-090 | vigente | 2026-08-16 | [[notas/decisiones/ADR-090-ramas-funcionales-sin-ancla-publica|Ramas funcionales sin ancla pública]] |
| D-091 | vigente | 2026-08-16 | [[notas/decisiones/ADR-091-datos-de-family-como-descriptores-anclados|Datos de family como descriptores anclados]] |
| D-092 | vigente | 2026-08-16 | [[notas/decisiones/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas|Disponibilidad estática de propiedades reflectivas]] |
| D-093 | vigente | 2026-08-16 | [[notas/decisiones/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|AST superficial, HIR nominal e IR semántico elaborado]] |
| D-094 | vigente | 2026-08-16 | [[notas/decisiones/ADR-094-anclas-terminales-de-metadatos-configurados|Anclas terminales de metadatos configurados]] |
| D-095 | vigente | 2026-08-16 | [[notas/decisiones/ADR-095-extremos-vacios-como-ausencia-ordinaria|Extremos vacíos como ausencia ordinaria]] |
| D-096 | vigente | 2026-08-28 | [[notas/decisiones/ADR-096-modulos-callables-look-message-y-activacion|Módulos, callables, `look`, `message` y activación]] |

## Identificadores reservados

No contienen una decisión recuperable y no pueden reutilizarse:

`D-004`, `D-005`, `D-016`, `D-020`, `D-024`.

## Regeneración

```powershell
python tooling/decisions/manage_decisions.py generate
python tooling/decisions/manage_decisions.py validate
```
