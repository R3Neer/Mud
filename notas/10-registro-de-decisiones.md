# Registro de decisiones

Este archivo es un índice de decisiones, no una duplicación de la especificación. Cada decisión nueva debería tener su propio archivo futuro en `notas/decisiones/ADR-NNN-titulo.md` cuando necesite razonamiento amplio.

## Estados

- **Vigente**: norma actual.
- **Propuesta**: candidata pendiente de aprobación.

Este registro y `notas/decisiones/` contienen únicamente decisiones y propuestas vigentes. Cuando una deja de estarlo, se elimina del estado de trabajo; Git conserva su contenido y evolución. Los identificadores retirados no se reutilizan.

## Decisiones vigentes

| ID | Estado | Decisión | Documento dueño | Procedencia |
| --- | --- | --- | --- | --- |
| D-001 | Vigente | `.mud` es la fuente semántica de verdad | [01-vision-y-alcance.md](01-vision-y-alcance.md) | Secciones 2.1 y 76 |
| D-002 | Vigente | MUD describe dominio, no arquitectura de aplicación | [01-vision-y-alcance.md](01-vision-y-alcance.md) | Secciones 2.2 y 66 |
| D-003 | Vigente | MUD es un lenguaje declarativo, no lenguaje natural controlado | [01-vision-y-alcance.md](01-vision-y-alcance.md) | Sección 2.3 |
| D-006 | Vigente | Las reglas booleanas son puras y las acciones forman la API de escritura | [02-modelo-del-lenguaje.md](02-modelo-del-lenguaje.md) | Secciones 7, 31, 36 y 62 |
| D-007 | Vigente | Las resoluciones causales ocurren por ondas sobre instantáneas | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | Secciones 45 a 49 |
| D-008 | Vigente | Una acción produce `accepted`, `rejected` o `failed` | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | Sección 42 |
| D-009 | Vigente | `allowed` es especulación descartable y propaga fallos | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | Sección 43 |
| D-010 | Vigente | `eventually` exige prueba de finitud y terminación | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | Sección 44 |
| D-011 | Vigente | Los derivados no pueden añadir comportamiento de dominio | [04-arquitectura-del-sistema.md](04-arquitectura-del-sistema.md) | Secciones 2.1, 63 a 66 |
| D-012 | Vigente | Los cambios semánticos válidos se validan y versionan atómicamente | [05-cambios-semanticos-y-git.md](05-cambios-semanticos-y-git.md) | Secciones 68 a 71 e introducción del usuario |
| D-013 | Vigente | La especificación formal del lenguaje completo precederá a la continuación de su implementación | [especificacion/README.md](../especificacion/README.md) | Decisión del autor, 2026-07-27 |
| D-014 | Vigente | Las `thing` forman un único dominio; las concretas son cosas y posibles antecesoras, y `is` es reflexivo | [ADR-014](decisiones/ADR-014-ontologia-unificada-de-things.md) | Decisión del autor, 2026-07-27; vocabulario actualizado por D-025 |
| D-015 | Vigente | La especialización hereda esquema y predeterminados, mantiene estados independientes y rechaza ciclos | [ADR-015](decisiones/ADR-015-especializacion-aciclica-y-estado-independiente.md) | Decisión del autor, 2026-07-27 |
| D-017 | Vigente | Todo tipo bien formado posee un valor predeterminado perteneciente a su dominio | [ADR-017](decisiones/ADR-017-valor-predeterminado-de-todo-tipo.md) | Decisión del autor, 2026-07-27 |
| D-018 | Vigente | `as` declara especialización directa e `is` consulta su clausura reflexiva y transitiva | [ADR-018](decisiones/ADR-018-as-declara-is-consulta.md) | Decisión del autor, 2026-07-27 |
| D-019 | Vigente | La mutabilidad de una colección y la capacidad sobre sus miembros son ortogonales incluso en `[1]` | [ADR-019](decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros.md) | Decisión del autor, 2026-07-27 |
| D-021 | Vigente | `destroy` suspende `thing`, reglas y dependientes sin borrar su almacenamiento; `remove` sí elimina una propiedad y su carga | [ADR-021](decisiones/ADR-021-ciclo-de-vida-logico-y-suspension.md) | Decisión del autor, 2026-07-27 |
| D-022 | Vigente | Una llamada a una regla booleana inactiva se borra estructuralmente y la expresión exterior vacía se cierra con verdadero | [ADR-022](decisiones/ADR-022-borrado-de-reglas-booleanas-inactivas.md) | Decisión del autor, 2026-07-27 |
| D-023 | Vigente | Los `then` conservan secuencialidad local y consolidan efectos estructurales de forma determinista | [ADR-023](decisiones/ADR-023-consolidacion-de-efectos-estructurales.md) | Decisión del autor, 2026-07-27 |
| D-025 | Vigente | `thing` y `as` sustituyen `construct` y `from`; `on` se usa en observadores y `for` en solicitudes; toda cláusula admite llaves y puede omitirlas con un solo elemento | [ADR-025](decisiones/ADR-025-vocabulario-cabeceras-y-bloques.md) | Decisión del autor, 2026-07-27 |
| D-026 | Vigente | La membresía de `thing` es siempre estricta y cada `then` debe demostrar estáticamente su cardinalidad final y la compatibilidad de consolidación | [ADR-026](decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then.md) | Decisión del autor, 2026-07-27 |
| D-027 | Vigente | `look` consulta el estado estable y `message` publica tras estabilizar campos calculados cuyo tipo puede declararse o inferirse | [ADR-027](decisiones/ADR-027-salidas-look-y-message.md) | Decisión del autor, 2026-07-27; tipo opcional precisado el 2026-07-28 |
| D-028 | Vigente, ampliada por D-034 | Los tipos numéricos básicos representan números; las magnitudes aportan dimensión, admiten dominio tras la representación y derivan automáticamente unidades compatibles | [ADR-028](decisiones/ADR-028-sistema-de-magnitudes-y-unidades.md) | Decisión del autor, 2026-07-28 |
| D-029 | Vigente | `*` designa el límite efectivo lateral; los dominios de magnitud usan límites canónicos desnudos y solo los puntos admiten `[a..b cycle)` | [ADR-029](decisiones/ADR-029-intervalos-estrellas-y-ciclos.md) | Decisión del autor, 2026-07-28 |
| D-030 | Vigente como rama cuantitativa; ampliada por D-032 | `in` cambia la unidad de expresión y la rama cuantitativa de `to` convierte cantidades compatibles | [ADR-030](decisiones/ADR-030-conversion-cuantitativa-explicita.md) | Decisión del autor, 2026-07-28 |
| D-031 | Vigente | Todo alias es un tipo nominal de valor, inmutable y sin identidad ni ciclo de vida runtime | [ADR-031](decisiones/ADR-031-aliases-nominales-e-inmutables.md) | Decisión del autor, 2026-07-28 |
| D-032 | Vigente | `to` admite casting nominal estructural; los literales se construyen por contexto y las comparaciones no coercionan valores ya tipados | [ADR-032](decisiones/ADR-032-construccion-contextual-y-casting-nominal.md) | Decisión del autor, 2026-07-28 |
| D-033 | Vigente | Los aliases estructurales pueden ser claves y se enumeran como productos cartesianos lexicográficos cuando sus componentes son finitos y enumerables | [ADR-033](decisiones/ADR-033-claves-y-enumeracion-de-aliases.md) | Decisión del autor, 2026-07-28 |
| D-034 | Vigente | `Number` es racional exacto; `Rumber` usa `binary64` explícito, no se mezcla implícitamente y sus intervalos no son enumerables | [ADR-034](decisiones/ADR-034-number-exacto-y-rumber-binary64.md) | Decisión del autor, 2026-07-28 |
| D-035 | Vigente | El namespace procede de la ruta; `using` controla visibilidad, `ordered` es reservada y las anclas estables no contienen el archivo | [ADR-035](decisiones/ADR-035-organizacion-nombres-using-y-anclas.md) | Migración normativa de las secciones 4, 5 y 9; vocabulario cerrado el 2026-07-28 |
| D-036 | Vigente | Los participantes pueden omitir nombre si la resolución es unívoca; las etiquetas opcionales de `given` conservan siempre la posición | [ADR-036](decisiones/ADR-036-participantes-receptores-y-llamadas.md) | Migración normativa de las secciones 6 y 7, actualizada por D-025 |
| D-037 | Vigente | Los campos almacenados ordenan tipo, dominio y colección; `:=` declara un cálculo puro con anotación de tipo opcional | [ADR-037](decisiones/ADR-037-campos-y-dominios-declarativos.md) | Migración normativa de las secciones 13, 15 y 20; inferencia de tipo decidida por el autor el 2026-07-28 |
| D-038 | Vigente | `family` declara tipos nominales finitos cuyos miembros pueden completar un esquema uniforme de datos inmutables mediante predeterminados | [ADR-038](decisiones/ADR-038-familias-cerradas-de-valores.md) | Migración normativa de la sección 12, completada por decisión del autor el 2026-07-28 |
| D-039 | Vigente | Las colecciones conservan multiplicidad salvo `unique`; sus inserciones repetidas se consolidan idempotentemente y los diccionarios tienen claves intrínsecamente únicas | [ADR-039](decisiones/ADR-039-colecciones-y-diccionarios.md) | Migración normativa de las secciones 16 a 18; unicidad y avisos precisados por decisión del autor el 2026-07-28 |
| D-040 | Vigente | La aritmética exacta amplía tipos de forma controlada; `Money` tiene escala decimal dos y `Natural` satura su resta en cero | [ADR-040](decisiones/ADR-040-semantica-numerica-basica-restante.md) | Migración normativa de las secciones 19 y 29, coordinada con D-034 |
| D-041 | Vigente | Las reglas booleanas, reactivas y `always` son variantes distintas con contratos cerrados | [ADR-041](decisiones/ADR-041-contratos-de-las-tres-clases-de-regla.md) | Migración normativa de las secciones 31 a 35, actualizada por D-021, D-022 y D-025 |
| D-042 | Vigente | Las acciones forman transacciones causales atómicas y producen exclusivamente `accepted`, `rejected` o `failed` | [ADR-042](decisiones/ADR-042-acciones-raiz-y-resultados.md) | Migración normativa de las secciones 36 a 42, actualizada por D-025 |
| D-043 | Vigente | `allowed` ejecuta el protocolo completo de una acción en una copia descartable y propaga los fallos | [ADR-043](decisiones/ADR-043-consulta-especulativa-allowed.md) | Migración normativa de la sección 43 |
| D-044 | Vigente con admisibilidad conservadora | `eventually` expresa alcanzabilidad existencial sobre una colección de acciones y solo se admite sobre una transición finita, enumerable y terminante | [ADR-044](decisiones/ADR-044-alcanzabilidad-eventually.md) | Migración normativa de la sección 44 y sintaxis completada el 2026-07-28 |
| D-045 | Vigente en su núcleo | Las consecuencias se resuelven por ondas sobre instantáneas, con una sola resolución activa y cola externa | [ADR-045](decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola.md) | Migración normativa de las secciones 45 a 49 |
| D-046 | Vigente como núcleo | Los efectos concurrentes forman deltas privados y se consolidan mediante un álgebra determinista de compatibilidad | [ADR-046](decisiones/ADR-046-algebra-y-conflictos-de-efectos.md) | Migración normativa de las secciones 48, 50 y 51, ampliada por D-023 y D-026 |
| D-047 | Vigente | Cuantificadores, agregaciones y `for each` exigen fuentes finitas enumerables y un orden semántico definido | [ADR-047](decisiones/ADR-047-cuantificadores-e-iteracion-finita.md) | Migración normativa de las secciones 52 y 53, coordinada con D-033 y D-034 |
| D-048 | Vigente en su núcleo | El azar procede de puntos semánticos sembrados y los fallos no se degradan silenciosamente a falsedad | [ADR-048](decisiones/ADR-048-azar-reproducible-y-fallos.md) | Migración normativa de las secciones 57 y 58, coordinada con D-034 |
| D-049 | Vigente | Operadores, conversiones y encadenamientos poseen agrupación normativa; los intervalos se normalizan por contenido | [ADR-049](decisiones/ADR-049-operadores-precedencia-e-intervalos-normalizados.md) | Migración normativa de las secciones 27 a 29 y gramática completada el 2026-07-28 |
| D-050 | Vigente | MUD fija comentarios, textos ordinarios y multilínea; el salto o `;` termina salvo prefijo sintácticamente incompleto | [ADR-050](decisiones/ADR-050-comentarios-terminadores-y-separadores-numericos.md) | Migración normativa de las secciones 30, 60 y 61 y sintaxis completada el 2026-07-28 |
| D-051 | Vigente como contrato arquitectónico | AST, grafo e IR son derivados reconstruibles que conservan todas las distinciones semánticas y la procedencia | [ADR-051](decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles.md) | Migración revisada de las secciones 63 y 64 |
| D-052 | Vigente como frontera arquitectónica | El pipeline separa parsing, resolución, análisis e IR; materializadores y editor preservan la semántica | [ADR-052](decisiones/ADR-052-pipeline-materializadores-y-conformidad.md) | Migración revisada de las secciones 65, 66, 72 a 74 |
| D-053 | Vigente como política de producto | El operador semántico clasifica, analiza impacto, valida y versiona cada mutación sin inventar reglas | [ADR-053](decisiones/ADR-053-operador-semantico-y-flujo-de-autoria.md) | Migración revisada de las secciones 67 a 71 y 78 |
| D-054 | Vigente | Toda `thing` y regla tiene una definición canónica de primer nivel; `create Nombre` solo activa y `start with` declara el conjunto inicial no ordenado | [ADR-054](decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md) | Decisión del autor, 2026-07-28 |
| D-055 | Vigente | `test` declara pruebas aisladas con `start with`, `then` y aserciones `after`; `otherwise` aporta diagnósticos de fallo y las anclas usan `test::*` | [ADR-055](decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md) | Decisión del autor, 2026-07-28 |
| D-056 | Vigente | `Character` representa escalares Unicode; `Text` conserva posición y no equivale a una colección de caracteres ordenada | [ADR-056](decisiones/ADR-056-character-texto-y-orden-unicode.md) | Decisión del autor, 2026-07-28 |
| D-057 | Vigente | Las EBNF léxica y concreta, junto con su tabla de precedencia y reglas contextuales, definen la sintaxis completa de MUD 1.0 | [ADR-057](decisiones/ADR-057-gramatica-concreta-y-continuacion.md) | Decisión del autor, 2026-07-28 |

## Propuestas de estas notas

| ID | Estado | Propuesta | Motivo | Pregunta relacionada |
| --- | --- | --- | --- | --- |
| P-002 | Propuesta | Separar AST de superficie e IR canónico | Conservar procedencia y desacoplar sintaxis de semántica | Q-009 |
| P-003 | Propuesta | No crear commits para consultas `READ` puras | Git registra cambios de estado, no lecturas | Q-008 |
| P-004 | Propuesta | Preparar cambios en un área aislada y publicar al validar | Evitar rollback incompleto y commits contaminados | Q-008 |
| P-005 | Propuesta | Posponer `allowed`, `eventually` y azar hasta estabilizar el runtime | Reutilizar una semántica transaccional probada | Q-026 a Q-035 |

## Plantilla ADR

```markdown
# ADR-NNN — Título

- Estado: Propuesta
- Fecha:
- Preguntas: Q-NNN
- Documentos afectados:

## Contexto

Qué problema obliga a decidir y qué comportamiento ya está comprometido.

## Decisión

Regla normativa, expresada de forma comprobable.

## Alternativas

Opciones consideradas y por qué se descartan.

## Consecuencias

Impacto en sintaxis, AST, IR, runtime, grafo, tooling, compatibilidad y tests.

## Ejemplos

Casos válidos, inválidos y límites.

## Verificación

Pruebas o propiedades que demuestran la decisión.
```

## Proceso

1. Una pregunta abierta motiva una propuesta.
2. La propuesta enumera alternativas y consecuencias.
3. Se aprueba, rechaza o sustituye explícitamente.
4. Se actualizan especificación, nota dueña y tests.
5. El registro enlaza la decisión sin repetir toda su argumentación.
