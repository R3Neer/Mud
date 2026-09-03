---
title: Glosario transitorio de traducción español-inglés
aliases:
  - Glosario de migración al inglés
tags:
  - mud/notes
  - mud/traduccion
status: active
decisions:
  - D-104
temporary: true
temporary-reason: "Aplicar de forma reproducible las decisiones terminológicas durante la migración al inglés."
temporary-delete-when: "La migración completa del contenido y las rutas al inglés haya concluido y las reglas terminológicas permanentes se hayan integrado en su ubicación definitiva."
---

# Glosario transitorio de traducción español-inglés

> [!warning]
> Esta es una vista humana generada desde `tooling/translation/mud-es-en.toml`.
> No se edita a mano ni define semántica nueva de Mud.

## Contrato de migración

El perfil conserva código, matemáticas, HTML, URLs, rutas, embeds, destinos
de enlaces, identificadores y valores contractuales de frontmatter. Traduce
etiquetas visibles y los campos editoriales seleccionados. El destino es
inglés británico (`EN-GB`).

En `[[path|label]]` se conserva `path`; en `[label](URL)` se conserva la URL.
Los términos `force` se imponen mediante marcadores opacos y los términos
`review` requieren una decisión contextual.

## Formas Mud protegidas

| Forma literal | Forma literal | Forma literal |
| --- | --- | --- |
| `using` | `thing` | `as` |
| `alias` | `family` | `magnitude` |
| `rule` | `action` | `subaction` |
| `look` | `message` | `test` |
| `for` | `on` | `given` |
| `when` | `changes` | `if` |
| `then` | `after` | `with` |
| `otherwise` | `mut` | `unique` |
| `ordered` | `create` | `destroy` |
| `add` | `remove` | `from` |
| `each` | `by` | `through` |
| `take` | `exists` | `forall` |
| `count` | `min` | `max` |
| `to` | `eventually` | `allowed` |
| `old` | `is` | `iis` |
| `in` | `has` | `not` |
| `and` | `or` | `xor` |
| `Text` | `Char` | `Bool` |
| `Thing` | `Any` | `Nat` |
| `Int` | `Num` | `Rum` |
| `Money` | `Rand` | `Name` |
| `MudPath` | `Anchor` | `MudFile` |
| `Prefix` | `true` | `false` |
| `empty` | `all` | `_` |
| `abstract` | `always` | `start` |
| `value` | `type` | `name` |
| `path` | `anchor` | `file` |
| `plural` | `abbreviation` | `prefixes` |
| `format` | `root` | `unit` |
| `point` | `over` | `cycle` |

## Producto, autoridad y documentación

| Español | Inglés canónico | Tratamiento | Nota |
| --- | --- | --- | --- |
| alcance | scope | `force` | No usar reach para el alcance documental. |
| autoridad | authority | `force` | Normative authority cuando se refiere a la fuerza de una fuente. |
| autoridad consolidada | established authority | `force` | Evita el falso amigo consolidated authority. |
| autoridad transitoria | interim authority | `force` |  |
| capítulo | chapter | `force` |  |
| conformidad | conformance | `force` | No usar compliance para una implementación de lenguaje. |
| criterio de conformidad | conformance criterion | `force` |  |
| decisión | decision | `force` | Decision record para un ADR como documento. |
| decisión vigente | current decision | `force` | In-force decision solo si el contexto jurídico lo exige. |
| derivado | derived artifact / projection | `review` | Usar projection cuando se enfatiza que se reconstruye desde la fuente. |
| documento normativo | normative document | `force` |  |
| estado de publicación | publication status | `force` |  |
| especificación | specification | `force` |  |
| fuente de verdad | source of truth | `force` |  |
| historia / procedencia | history / provenance | `review` | Provenance para origen y trazabilidad de una regla o artefacto. |
| índice | index | `force` |  |
| norma | rule / specification requirement | `review` | Elegir rule para una regla concreta y requirement para obligación de conformidad. |
| pregunta activa | active question | `force` | No usar issue salvo que sea una issue de GitHub. |
| cuestión abierta | open question | `force` |  |
| requisito | requirement | `force` |  |
| superficie normativa | normative surface | `force` | Mantener esta expresión técnica. |
| trazabilidad | traceability | `force` |  |
| versión objetivo | target version | `force` |  |
| vigente | current | `force` | Para status no traducir hasta migrar sus valores y validadores. |

## Modelo y semántica del dominio

| Español | Inglés canónico | Tratamiento | Nota |
| --- | --- | --- | --- |
| acción | action | `force` | La construcción se escribe siempre action. |
| activación | activation | `force` |  |
| activación inicial | initial activation | `force` |  |
| admisibilidad | admissibility | `force` |  |
| aleatoriedad | randomness | `force` | Randomness, no randomnessness ni chance como término técnico. |
| ancla | anchor | `force` | No usar link, handle ni label. |
| ancla pública | public anchor | `force` |  |
| ancla terminal | terminal anchor | `force` |  |
| ámbito | scope | `force` |  |
| aplicación anfitriona | host application | `force` |  |
| autorización | authorisation | `force` |  |
| binding / vinculación | binding | `review` | Mantener binding para evitar confundirlo con una relación del dominio. |
| causal | causal | `force` |  |
| cola | queue | `force` |  |
| comportamiento observable | observable behaviour | `force` |  |
| consecuencia | consequence | `force` | Usar effect solo para un efecto semántico escrito o consolidado. |
| conflicto | conflict | `force` |  |
| consolidación | consolidation | `force` |  |
| consulta | query | `force` |  |
| consulta especulativa | speculative query | `force` |  |
| contrato | contract | `force` |  |
| declaración | declaration | `force` |  |
| definición canónica | canonical definition | `force` |  |
| delta | delta | `force` |  |
| dependencia dura | hard dependency | `force` |  |
| descriptor | descriptor | `force` |  |
| descriptor callable borrado | erased callable descriptor | `force` | Erased se refiere al borrado de información de tipo, no a una eliminación. |
| determinismo | determinism | `force` |  |
| diagnóstico | diagnostic | `force` | Diagnostic, no diagnosis. |
| dominio | domain | `force` | Domain model para el modelo; domain para la restricción de valores. |
| efecto | effect | `force` |  |
| efecto exterior | external effect | `force` |  |
| efecto pendiente | pending effect | `force` |  |
| explicación | explanation | `force` |  |
| fallo | failure | `force` | Distinguir de error. |
| fallo técnico | technical failure | `force` |  |
| frontera pública | public boundary | `force` |  |
| grafo | graph | `force` |  |
| grafo nominal | nominal graph | `force` |  |
| identidad | identity | `force` |  |
| identidad canónica | canonical identity | `force` |  |
| implementación conforme | conforming implementation | `force` |  |
| invariante | invariant | `force` | La regla se llama always rule; la propiedad que mantiene es an invariant. |
| lector / escritura | reader / write | `review` | Preferir read set y write set para conjuntos de dependencias. |
| materialización | materialisation | `force` | No usar implementation, generation ni instantiation como equivalentes generales. |
| modelo | model | `force` |  |
| mundo | world | `force` |  |
| mundo inicial | initial world | `force` |  |
| mundo estable | stable world | `force` |  |
| observación | observation | `force` |  |
| ocurrencia | occurrence | `force` | Para una ocurrencia de message. |
| onda | wave | `force` |  |
| onda causal | causal wave | `force` |  |
| operador semántico | semantic operator | `force` |  |
| orden estable | stable order | `force` |  |
| propietario | owner | `force` |  |
| pureza | purity | `force` |  |
| raíz | root | `force` |  |
| razón | reason | `force` | Campo o explicación de un resultado no aceptado. |
| reacción | reaction | `force` |  |
| regla reactiva | reactive rule | `force` |  |
| regla booleana | Boolean rule | `force` |  |
| regla always | always rule | `force` | No traducir always por always rule. |
| relación | relation | `force` |  |
| resolución | resolution | `force` |  |
| resolución causal | causal resolution | `force` |  |
| resolución nominal | nominal resolution | `force` |  |
| resultado | result | `force` |  |
| retroceso | rollback | `force` | No usar reversal para la operación transaccional. |
| semántica | semantics | `force` |  |
| semántica estática / dinámica | static / dynamic semantics | `review` |  |
| semilla | seed | `force` |  |
| solicitud | request | `force` |  |
| suspensión | suspension | `force` | Distinguir de destroy. |
| transición | transition | `force` |  |
| transición atómica | atomic transition | `force` |  |
| valor | value | `force` |  |
| valor predeterminado | default value | `force` |  |
| vinculación conjunta | joint binding | `force` |  |

## Estados y resultados

| Español | Inglés canónico | Tratamiento | Nota |
| --- | --- | --- | --- |
| aceptada / aceptado | accepted | `review` | El literal de Mud conserva minúsculas y acentos graves. |
| rechazada / rechazado | rejected | `review` | Un rechazo es una respuesta válida del dominio. |
| fallida / fallido | failed | `review` | No mezclar con rejected. |
| error | error | `force` | Un error impide evaluar o construir el resultado. |
| pasado | passed | `force` | Resultado de un test. |
| test fallido | failed test | `force` |  |
| test con error | errored test | `force` | Mantener la distinción con un test que simplemente falla. |
| estado | state | `force` |  |
| estado confirmado | confirmed state | `force` |  |
| estado estable | stable state | `force` |  |
| estado tentativo | tentative state | `force` |  |
| instantánea | snapshot | `force` |  |
| instantánea anterior | previous snapshot | `force` |  |
| estabilización | stabilisation | `force` |  |
| línea base | baseline | `force` | Para la memoria temporal reactiva. |
| memoria reactiva | reactive memory | `force` |  |

## Entidades, tipos y datos

| Español | Inglés canónico | Tratamiento | Nota |
| --- | --- | --- | --- |
| thing abstracta / concreta | abstract / concrete thing | `review` | No traducir la construcción como object, entity o class. |
| Thing incorporada | built-in Thing | `force` |  |
| alias | alias | `force` |  |
| alias nominal | nominal alias | `force` |  |
| alias estructural | structural alias | `force` |  |
| antecesora | ancestor | `force` |  |
| antecesora directa | direct ancestor | `force` |  |
| campo | field | `force` |  |
| campo almacenado | stored field | `force` |  |
| campo calculado | computed field | `force` |  |
| campo derivado | derived field | `force` |  |
| capacidad exterior / interior | outer / inner capability | `review` |  |
| cardinalidad | cardinality | `force` |  |
| carga propia | own stored data | `force` | No usar payload: ese término se reserva para message. |
| colección | collection | `force` |  |
| colección almacenada / derivada | stored / derived collection | `review` |  |
| contenido asociado | associated data | `force` |  |
| diccionario exacto / funcional | exact / functional dictionary | `review` |  |
| enumerabilidad | enumerability | `force` |  |
| familia cerrada | closed family | `force` | La construcción es family. |
| igualdad estructural | structural equality | `force` |  |
| igualdad nominal | nominal equality | `force` |  |
| igualdad de valores | value equality | `force` |  |
| magnitud | magnitude | `force` |  |
| magnitud base / derivada / de punto | base / derived / point magnitude | `review` |  |
| miembro | member | `force` |  |
| membresía | membership | `force` |  |
| metadato | metadata | `force` |  |
| metadato configurado | configured metadata | `force` |  |
| metadato intrínseco | intrinsic metadata | `force` |  |
| mutabilidad | mutability | `force` |  |
| nombre intrínseco | intrinsic name | `force` |  |
| orden parcial | partial order | `force` |  |
| pertenencia estricta | strict membership | `force` |  |
| punto | point | `force` | En prosa dimensional, point; no confundir con un punto tipográfico. |
| prefijo | prefix | `force` |  |
| presentación | presentation | `force` |  |
| proyección efectiva | effective projection | `force` |  |
| rama | branch | `force` |  |
| rama funcional | functional branch | `force` |  |
| relación inmutable | immutable relation | `force` |  |
| tipo | type | `force` |  |
| tipo anónimo | anonymous type | `force` |  |
| tipo callable | callable type | `force` |  |
| tipo nominal efectivo exacto | exact effective nominal type | `force` |  |
| tipo superior | top type | `force` |  |
| unión | union | `force` |  |
| unidad | unit | `force` |  |
| valor estructural | structural value | `force` |  |
| varianza | variance | `force` |  |

## Sintaxis, compilación y análisis

| Español | Inglés canónico | Tratamiento | Nota |
| --- | --- | --- | --- |
| analizador léxico | scanner | `force` | Usar scanner para la fase de Mud; lexer solo si se habla genéricamente. |
| analizador sintáctico | parser | `force` |  |
| AST superficial | surface AST | `force` |  |
| ASDL | ASDL | `force` |  |
| clasificación contextual | contextual classification | `force` |  |
| comentario | comment | `force` |  |
| cobertura sintáctica | syntax coverage | `force` |  |
| CST sin pérdidas | lossless CST | `force` |  |
| delimitador | delimiter | `force` |  |
| elaboración | elaboration | `force` | No traducir como development. |
| entorno | environment | `force` |  |
| EBNF | EBNF | `force` |  |
| espacio significativo | significant view | `force` |  |
| gramática concreta | concrete grammar | `force` |  |
| gramática léxica | lexical grammar | `force` |  |
| HIR nominal | nominal HIR | `force` |  |
| inferencia | inference | `force` |  |
| literal | literal | `force` |  |
| origen fuente | source origin | `force` |  |
| palabra contextual | contextual word | `force` |  |
| palabra reservada | reserved word | `force` |  |
| precedencia | precedence | `force` |  |
| procedencia | provenance | `force` |  |
| producción | production | `force` |  |
| representación semántica | semantic representation | `force` |  |
| resolución de nombres | name resolution | `force` |  |
| símbolo | symbol | `force` |  |
| sintaxis abstracta | abstract syntax | `force` |  |
| sintaxis concreta | concrete syntax | `force` |  |
| span | span | `force` |  |
| texto fuente | source text | `force` |  |
| token | token | `force` |  |
| trivia | trivia | `force` |  |
| validación contextual | contextual validation | `force` |  |

## Módulos, interfaz y pruebas

| Español | Inglés canónico | Tratamiento | Nota |
| --- | --- | --- | --- |
| argumento | argument | `force` | Un given se comporta como argumento, pero la palabra fuente sigue siendo given. |
| cierre de tipos | type closure | `force` |  |
| compatibilidad | compatibility | `force` |  |
| dependencia modular | module dependency | `force` |  |
| entrega | delivery | `force` | Para la entrega exterior de una ocurrencia. |
| frontera de aplicación | application boundary | `force` |  |
| interfaz anfitriona | host API | `force` |  |
| llamada | call | `force` |  |
| módulo | module | `force` |  |
| participante | participant | `force` | No usar parameter cuando denota un rol for u on. |
| payload | payload | `force` | Reservado para los campos públicos de una ocurrencia message. |
| propiedad pública | public property | `force` |  |
| receptor | receiver | `force` |  |
| reflexión | reflection | `force` |  |
| solicitud exterior | external request | `force` |  |
| test declarativo | declarative test | `force` |  |
| visibilidad | visibility | `force` |  |

## Análisis avanzado y operación

| Español | Inglés canónico | Tratamiento | Nota |
| --- | --- | --- | --- |
| alcanzabilidad | reachability | `force` |  |
| análisis estático | static analysis | `force` |  |
| análisis especulativo | speculative analysis | `force` |  |
| ciclo | cycle | `force` |  |
| ciclo ejecutable | executable cycle | `force` |  |
| decidibilidad | decidability | `force` |  |
| finitud | finiteness | `force` |  |
| oscilación | oscillation | `force` |  |
| perfil de mundos finitos | finite-world profile | `force` |  |
| propiedad metateórica | metatheoretic property | `force` |  |
| prueba de conformidad | conformance test | `force` |  |
| reproducibilidad | reproducibility | `force` |  |
| terminación | termination | `force` |  |
| amenaza | threat | `force` |  |
| permiso | permission | `force` |  |

## Términos editoriales y de proceso

| Español | Inglés canónico | Tratamiento | Nota |
| --- | --- | --- | --- |
| archivo temporal | temporary file | `force` |  |
| bóveda | vault | `force` | En el contexto de Obsidian. |
| cambio semántico | semantic change | `force` |  |
| ciclo documental | document lifecycle | `force` |  |
| commit atómico | atomic commit | `force` |  |
| documento generado | generated document | `force` |  |
| flujo de autoría | authoring workflow | `force` |  |
| governance | governance | `force` |  |
| historial Git | Git history | `force` |  |
| política | policy | `force` |  |
| promoción | promotion | `force` | Para elevar un documento en su estado de publicación. |
| repositorio | repository | `force` |  |
| revisión | review | `force` |  |
| ruta | path | `force` | Usar Mud path cuando sea la ruta lógica del lenguaje. |
| validación | validation | `force` |  |

## Pendientes de decisión terminológica

| Español | Inglés canónico | Tratamiento | Nota |
| --- | --- | --- | --- |
| retirada | retirement | `review` | Debe distinguirse de remove y destroy; quizá retirement resulte demasiado jurídico en algunas frases. |
| carga | stored data | `review` | Su sentido depende de si es estado, contenido de una declaración o datos de un mensaje. |
| vista | view | `review` | Puede significar una vista de lectura, una proyección o una interfaz de Obsidian. |
| forma | form | `review` | Puede ser sintáctica, normalizada o declarable. |
| propio | own / intrinsic | `review` | Own para propiedad o datos de una entidad; intrinsic para una propiedad inherente. |
| efectiva | effective | `review` | Debe reservarse para contratos, tipos, dominios o proyecciones resultantes; no equivale a actual en todos los casos. |
| exterior | external / outer | `review` | External para frontera o solicitud; outer para capacidad. |
| activable | activatable | `review` | Confirmar si el término se conserva o se reemplaza por una construcción más legible al redactar. |

## Decisiones de estilo

- Use British English: behaviour, modelling, materialisation and authorisation.
- Keep Mud as the proper name, .mud as the extension and mud only where code requires it.
- Keep literal Mud constructs in backticks in technical prose.
- Prefer semantic operator to semantic editor.
- Prefer materialiser to generator.
- Distinguish rule from requirement, effect from consequence, failure from error, and rejected from failed.
- Translate visible chapter, decision and question names, but do not rename their paths or wikilink targets in this phase.

## Grafías estadounidenses prohibidas

`behavior`, `behaviors`, `behavioral`, `color`, `colors`, `colored`, `coloring`, `modeling`, `modeled`, `modeler`, `materialization`, `materialized`, `materializing`, `materializer`, `authorization`, `authorized`, `unauthorized`, `stabilization`.
