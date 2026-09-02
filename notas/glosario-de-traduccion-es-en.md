---
title: Glosario transitorio de traducción español-inglés
aliases:
  - Glosario de migración al inglés
tags:
  - mud/notas
  - mud/traduccion
status: activo
decisions:
  - D-104
temporary: true
temporary-reason: "Fijar un vocabulario inglés uniforme y proteger construcciones formales durante la migración integral del repositorio."
temporary-delete-when: "La migración del contenido y de las rutas al inglés haya concluido y las decisiones terminológicas que deban conservarse estén integradas en una guía permanente o en la especificación."
---

# Glosario transitorio de traducción español-inglés

> [!warning]
> Este documento dirige una migración editorial. No define semántica nueva de
> Mud ni sustituye la terminología normativa futura.

## Alcance y reglas de uso

Cada traducción de prosa debe usar las equivalencias de este documento. Una
entrada escrita entre acentos graves es una construcción, tipo o identificador
de Mud y se conserva exactamente como aparece. El texto que la explica sí se
traduce.

No se traduce ni modifica automáticamente:

- bloques de código, código inline, EBNF, ASDL, YAML normativo o archivos
  fuente no Markdown;
- identificadores `D-NNN`, `Q-NNN` y `MUD-...`;
- claves de frontmatter, valores de estado mientras los validadores esperen sus
  formas actuales, anclas, paths y destinos de enlaces;
- URLs, expresiones matemáticas, nombres de tipos, nombres de declaraciones y
  literales de programas Mud.

En un enlace `[[path|label]]` se preserva `path` y se traduce `label`. En un
enlace `[label](URL)` se preserva la URL y se traduce `label`.

## Palabras de la fuente Mud

Las siguientes palabras pertenecen a la sintaxis de Mud. Nunca se traducen en
programas, gramáticas, ejemplos ni referencias literales; la columna inglesa
indica únicamente cómo explicarlas en prosa.

| Clase | Forma Mud protegida | Explicación inglesa canónica |
| --- | --- | --- |
| Declaración | `using`, `thing`, `as`, `alias`, `family`, `magnitude` | use the literal form; e.g. “a `thing` declaration” |
| Declaración | `rule`, `action`, `subaction`, `look`, `message`, `test` | use the literal form; e.g. “an `action` declaration” |
| Cláusula | `for`, `on`, `given`, `when`, `changes`, `if`, `then`, `after`, `with`, `otherwise` | use the literal form; e.g. “the `given` clause” |
| Modificador y efecto | `mut`, `unique`, `ordered`, `create`, `destroy`, `add`, `remove`, `from` | use the literal form; e.g. “the `destroy` effect” |
| Iteración | `each`, `by`, `through`, `take`, `exists`, `forall`, `count`, `min`, `max` | use the literal form; e.g. “the `for each` iteration” |
| Operador | `to`, `eventually`, `allowed`, `old`, `is`, `iis`, `in`, `has`, `not`, `and`, `or`, `xor` | use the literal form; e.g. “the `allowed` query” |
| Tipo incorporado | `Text`, `Char`, `Bool`, `Thing`, `Any`, `Nat`, `Int`, `Num`, `Rum`, `Money`, `Rand`, `Name`, `MudPath`, `Anchor`, `MudFile`, `Prefix` | use the literal type name |
| Constante | `true`, `false`, `empty`, `all`, `_` | use the literal form |
| Contextual | `abstract`, `always`, `start`, `value`, `type`, `name`, `path`, `anchor`, `file`, `plural`, `abbreviation`, `prefixes`, `format`, `root`, `unit`, `point`, `over`, `cycle` | use the literal form; e.g. “an `always` rule” |

## Producto, autoridad y documentación

| Español | Inglés canónico | Nota |
| --- | --- | --- |
| alcance | scope | No usar *reach* para el alcance documental. |
| autoridad | authority | *Normative authority* cuando se refiere a la fuerza de una fuente. |
| autoridad consolidada | established authority | Evita el falso amigo *consolidated authority*. |
| autoridad transitoria | interim authority | |
| capítulo | chapter | |
| conformidad | conformance | No usar *compliance* para una implementación de lenguaje. |
| criterio de conformidad | conformance criterion | |
| decisión | decision | *Decision record* para un ADR como documento. |
| decisión vigente | current decision | *In-force decision* solo si el contexto jurídico lo exige. |
| derivado | derived artifact / projection | Usar *projection* cuando se enfatiza que se reconstruye desde la fuente. |
| documento normativo | normative document | |
| estado de publicación | publication status | |
| especificación | specification | |
| fuente de verdad | source of truth | |
| historia / procedencia | history / provenance | *Provenance* para origen y trazabilidad de una regla o artefacto. |
| índice | index | |
| norma | rule / specification requirement | Elegir *rule* para una regla concreta y *requirement* para obligación de conformidad. |
| pregunta activa | active question | No usar *issue* salvo que sea una issue de GitHub. |
| cuestión abierta | open question | |
| requisito | requirement | |
| superficie normativa | normative surface | Mantener esta expresión técnica. |
| trazabilidad | traceability | |
| versión objetivo | target version | |
| vigente | current | Para `status` no traducir hasta migrar sus valores y validadores. |

## Modelo y semántica del dominio

| Español | Inglés canónico | Nota |
| --- | --- | --- |
| acción | action | La construcción se escribe siempre `action`. |
| activación | activation | |
| activación inicial | initial activation | |
| admisibilidad | admissibility | |
| aleatoriedad | randomness | *Randomness*, no *randomnessness* ni *chance* como término técnico. |
| ancla | anchor | No usar *link*, *handle* ni *label*. |
| ancla pública | public anchor | |
| ancla terminal | terminal anchor | |
| ámbito | scope | |
| aplicación anfitriona | host application | |
| autorización | authorisation | |
| binding / vinculación | binding | Mantener *binding* para evitar confundirlo con una relación del dominio. |
| causal | causal | |
| cola | queue | |
| comportamiento observable | observable behaviour | |
| consecuencia | consequence | Usar *effect* solo para un efecto semántico escrito o consolidado. |
| conflicto | conflict | |
| consolidación | consolidation | |
| consulta | query | |
| consulta especulativa | speculative query | |
| contrato | contract | |
| declaración | declaration | |
| definición canónica | canonical definition | |
| delta | delta | |
| dependencia dura | hard dependency | |
| descriptor | descriptor | |
| descriptor callable borrado | erased callable descriptor | *Erased* se refiere al borrado de información de tipo, no a una eliminación. |
| determinismo | determinism | |
| diagnóstico | diagnostic | *Diagnostic*, no *diagnosis*. |
| dominio | domain | *Domain model* para el modelo; *domain* para la restricción de valores. |
| efecto | effect | |
| efecto exterior | external effect | |
| efecto pendiente | pending effect | |
| explicación | explanation | |
| fallo | failure | Distinguir de *error*. |
| fallo técnico | technical failure | |
| frontera pública | public boundary | |
| grafo | graph | |
| grafo nominal | nominal graph | |
| identidad | identity | |
| identidad canónica | canonical identity | |
| implementación conforme | conforming implementation | |
| invariante | invariant | La regla se llama `always` rule; la propiedad que mantiene es an invariant. |
| lector / escritura | reader / write | Preferir *read set* y *write set* para conjuntos de dependencias. |
| materialización | materialisation | No usar *implementation*, *generation* ni *instantiation* como equivalentes generales. |
| modelo | model | |
| mundo | world | |
| mundo inicial | initial world | |
| mundo estable | stable world | |
| observación | observation | |
| ocurrencia | occurrence | Para una ocurrencia de `message`. |
| onda | wave | |
| onda causal | causal wave | |
| operador semántico | semantic operator | |
| orden estable | stable order | |
| propietario | owner | |
| pureza | purity | |
| raíz | root | |
| razón | reason | Campo o explicación de un resultado no aceptado. |
| reacción | reaction | |
| regla reactiva | reactive rule | |
| regla booleana | Boolean rule | |
| regla `always` | `always` rule | No traducir `always` por *always rule*. |
| relación | relation | |
| resolución | resolution | |
| resolución causal | causal resolution | |
| resolución nominal | nominal resolution | |
| resultado | result | |
| retroceso | rollback | No usar *reversal* para la operación transaccional. |
| semántica | semantics | |
| semántica estática / dinámica | static / dynamic semantics | |
| semilla | seed | |
| solicitud | request | |
| suspensión | suspension | Distinguir de `destroy`. |
| transición | transition | |
| transición atómica | atomic transition | |
| valor | value | |
| valor predeterminado | default value | |
| vinculación conjunta | joint binding | |

## Estados y resultados

| Español | Inglés canónico | Nota |
| --- | --- | --- |
| aceptada / aceptado | `accepted` / accepted | El literal de Mud conserva minúsculas y acentos graves. |
| rechazada / rechazado | `rejected` / rejected | Un rechazo es una respuesta válida del dominio. |
| fallida / fallido | `failed` / failed | No mezclar con `rejected`. |
| error | error | Un error impide evaluar o construir el resultado. |
| pasado | passed | Resultado de un test. |
| test fallido | failed test | |
| test con error | errored test | Mantener la distinción con un test que simplemente falla. |
| estado | state | |
| estado confirmado | confirmed state | |
| estado estable | stable state | |
| estado tentativo | tentative state | |
| instantánea | snapshot | |
| instantánea anterior | previous snapshot | |
| estabilización | stabilisation | |
| línea base | baseline | Para la memoria temporal reactiva. |
| memoria reactiva | reactive memory | |

## Entidades, tipos y datos

| Español | Inglés canónico | Nota |
| --- | --- | --- |
| `thing` abstracta / concreta | abstract / concrete `thing` | No traducir la construcción como *object*, *entity* o *class*. |
| `Thing` incorporada | built-in `Thing` | |
| alias | alias | |
| alias nominal | nominal alias | |
| alias estructural | structural alias | |
| antecesora | ancestor | |
| antecesora directa | direct ancestor | |
| campo | field | |
| campo almacenado | stored field | |
| campo calculado | computed field | |
| campo derivado | derived field | |
| capacidad exterior / interior | outer / inner capability | |
| cardinalidad | cardinality | |
| carga propia | own stored data | No usar *payload*: ese término se reserva para `message`. |
| colección | collection | |
| colección almacenada / derivada | stored / derived collection | |
| contenido asociado | associated data | |
| diccionario exacto / funcional | exact / functional dictionary | |
| enumerabilidad | enumerability | |
| familia cerrada | closed family | La construcción es `family`. |
| igualdad estructural | structural equality | |
| igualdad nominal | nominal equality | |
| igualdad de valores | value equality | |
| magnitud | magnitude | |
| magnitud base / derivada / de punto | base / derived / point magnitude | |
| miembro | member | |
| membresía | membership | |
| metadato | metadata | |
| metadato configurado | configured metadata | |
| metadato intrínseco | intrinsic metadata | |
| mutabilidad | mutability | |
| nombre intrínseco | intrinsic name | |
| orden parcial | partial order | |
| pertenencia estricta | strict membership | |
| punto | point | En prosa dimensional, *point*; no confundir con un punto tipográfico. |
| prefijo | prefix | |
| presentación | presentation | |
| proyección efectiva | effective projection | |
| rama | branch | |
| rama funcional | functional branch | |
| relación inmutable | immutable relation | |
| tipo | type | |
| tipo anónimo | anonymous type | |
| tipo callable | callable type | |
| tipo nominal efectivo exacto | exact effective nominal type | |
| tipo superior | top type | |
| unión | union | |
| unidad | unit | |
| valor estructural | structural value | |
| varianza | variance | |

## Sintaxis, compilación y análisis

| Español | Inglés canónico | Nota |
| --- | --- | --- |
| analizador léxico | scanner | Usar *scanner* para la fase de Mud; *lexer* solo si se habla genéricamente. |
| analizador sintáctico | parser | |
| AST superficial | surface AST | |
| ASDL | ASDL | |
| clasificación contextual | contextual classification | |
| comentario | comment | |
| cobertura sintáctica | syntax coverage | |
| CST sin pérdidas | lossless CST | |
| delimitador | delimiter | |
| elaboración | elaboration | No traducir como *development*. |
| entorno | environment | |
| EBNF | EBNF | |
| espacio significativo | significant view | |
| gramática concreta | concrete grammar | |
| gramática léxica | lexical grammar | |
| HIR nominal | nominal HIR | |
| inferencia | inference | |
| literal | literal | |
| origen fuente | source origin | |
| palabra contextual | contextual word | |
| palabra reservada | reserved word | |
| precedencia | precedence | |
| procedencia | provenance | |
| producción | production | |
| representación semántica | semantic representation | |
| resolución de nombres | name resolution | |
| símbolo | symbol | |
| sintaxis abstracta | abstract syntax | |
| sintaxis concreta | concrete syntax | |
| span | span | |
| texto fuente | source text | |
| token | token | |
| trivia | trivia | |
| validación contextual | contextual validation | |

## Módulos, interfaz y pruebas

| Español | Inglés canónico | Nota |
| --- | --- | --- |
| argumento | argument | Un `given` se comporta como argumento, pero la palabra fuente sigue siendo `given`. |
| cierre de tipos | type closure | |
| compatibilidad | compatibility | |
| dependencia modular | module dependency | |
| entrega | delivery | Para la entrega exterior de una ocurrencia. |
| frontera de aplicación | application boundary | |
| interfaz anfitriona | host API | |
| llamada | call | |
| módulo | module | |
| participante | participant | No usar *parameter* cuando denota un rol `for` u `on`. |
| payload | payload | Reservado para los campos públicos de una ocurrencia `message`. |
| propiedad pública | public property | |
| receptor | receiver | |
| reflexión | reflection | |
| solicitud exterior | external request | |
| test declarativo | declarative test | |
| visibilidad | visibility | |

## Análisis avanzado y operación

| Español | Inglés canónico | Nota |
| --- | --- | --- |
| alcanzabilidad | reachability | |
| análisis estático | static analysis | |
| análisis especulativo | speculative analysis | |
| ciclo | cycle | |
| ciclo ejecutable | executable cycle | |
| decidibilidad | decidability | |
| finitud | finiteness | |
| oscilación | oscillation | |
| perfil de mundos finitos | finite-world profile | |
| propiedad metateórica | metatheoretic property | |
| prueba de conformidad | conformance test | |
| reproducibilidad | reproducibility | |
| terminación | termination | |
| amenaza | threat | |
| permiso | permission | |

## Términos editoriales y de proceso

| Español | Inglés canónico | Nota |
| --- | --- | --- |
| archivo temporal | temporary file | |
| bóveda | vault | En el contexto de Obsidian. |
| cambio semántico | semantic change | |
| ciclo documental | document lifecycle | |
| commit atómico | atomic commit | |
| documento generado | generated document | |
| flujo de autoría | authoring workflow | |
| gobierno | governance | |
| historial Git | Git history | |
| política | policy | |
| promoción | promotion | Para elevar un documento en su estado de publicación. |
| repositorio | repository | |
| revisión | review | |
| ruta | path | Usar *Mud path* cuando sea la ruta lógica del lenguaje. |
| validación | validation | |

## Decisiones de estilo deliberadas

- Usar inglés británico: *behaviour*, *modelling*, *materialisation*.
- Mantener *Mud* como nombre propio; usar `.mud` para la extensión y `Mud` en
  prosa, salvo que una construcción de código exija `mud`.
- Conservar términos Mud entre acentos graves en prosa técnica cuando nombran
  una construcción del lenguaje.
- Preferir *semantic operator* a *semantic editor*, porque el componente
  consulta, explica y planifica además de editar.
- Preferir *materialiser* a *generator*, porque puede producir código,
  contratos, documentación o tests sin añadir semántica.
- Distinguir siempre *rule* de *requirement*, *effect* de *consequence*,
  *failure* de *error*, y *rejected* de *failed*.
- Traducir los nombres visibles de capítulos, ADR y preguntas con estas
  equivalencias, pero no renombrar aún sus rutas ni destinos de wikilinks.

## Pendientes de decisión terminológica

Estas expresiones requieren revisión al aparecer en su contexto, no sustitución
ciega:

| Español | Propuesta inicial | Riesgo que se debe revisar |
| --- | --- | --- |
| retirada | retirement | Debe distinguirse de `remove` y `destroy`; quizá *retirement* resulte demasiado jurídico en algunas frases. |
| carga | stored data | Su sentido depende de si es estado, contenido de una declaración o datos de un mensaje. |
| vista | view | Puede significar una vista de lectura, una proyección o una interfaz de Obsidian. |
| forma | form | Puede ser sintáctica, normalizada o declarable. |
| propio | own / intrinsic | *Own* para propiedad o datos de una entidad; *intrinsic* para una propiedad inherente. |
| efectiva | effective | Debe reservarse para contratos, tipos, dominios o proyecciones resultantes; no equivale a *actual* en todos los casos. |
| exterior | external / outer | *External* para frontera o solicitud; *outer* para capacidad. |
| activable | activatable | Confirmar si el término se conserva o se reemplaza por una construcción más legible al redactar. |
