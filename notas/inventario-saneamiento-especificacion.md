---
title: Inventario de saneamiento de la especificación
tags:
  - mud/notas
  - mud/especificacion
  - mud/saneamiento
status: activo
temporary: true
temporary-reason: "Checklist operativo del saneamiento de la especificación"
temporary-delete-when: "Se complete la Etapa 8 del saneamiento de la especificación"
---

# Inventario de saneamiento de la especificación

Este documento es un checklist de trabajo no normativo. Resume los defectos y obligaciones todavía relevantes detectados durante la auditoría de `especificacion/` posterior a la integración de módulos, callables, `look`, `message` y activación modular.

No define MUD. La autoridad normativa permanece en `especificacion/` y, transitoriamente cuando la superficie canónica todavía no existe, en las decisiones vigentes según MUD-EDIT-003.

## Estado de las etapas

- Etapa 0 — reglas editoriales persistentes: completada.
- Etapa 1 — inventario inicial: completada.
- Etapa 2 — integración editorial semánticamente neutra: completada.
- Etapa 3 — contradicciones y residuos semánticos en superficies desarrolladas: completada.
- Etapa 4 — auditoría sistemática de decisiones vigentes contra superficies existentes: completada.
- Etapa 5 — auditoría exhaustiva del documento fuente de la integración D-096: completada.
- Etapa 6 — revisión semántica del mapa futuro de `especificacion/README.md`: completada.
- Etapa 7 — barrera mecánica contra regresiones editoriales: completada.
- Etapa 8 — validación semántica global final: pendiente.

## Taxonomía de trabajo

| Código | Significado |
| --- | --- |
| C | Contradicción interna de una superficie. |
| X | Contradicción con el modelo vigente. |
| I | Integración incompleta: la superficie canónica ya existe pero no contiene una regla aceptada que le corresponde. |
| M | Semántica aceptada pendiente de formalización porque su superficie canónica todavía no existe. |
| Q | Tratamiento incorrecto de una pregunta activa. |
| U | Posible decisión nueva o fortalecimiento no claramente autorizado. |

Las categorías históricas/editoriales `H`, `A` y `D` del inventario inicial se consideran cubiertas por la Etapa 2 salvo que una auditoría posterior demuestre un residuo concreto.

## Etapa 3 — contradicciones y residuos semánticos

Completada. Los puntos E3-01 a E3-08 se cerraron integrando la regla vigente en sus superficies canónicas y propagando los renombres mecánicos necesarios. El detalle previo queda disponible en Git y no se conserva como deuda activa.

## Etapa 4 — auditoría de decisiones vigentes

Completada. Se recorrieron las decisiones vigentes contra las superficies normativas ya desarrolladas y contra los hogares futuros declarados por el mapa de la especificación.

La frontera vigente después de D-097 mantiene como superficie mecánica actual el HIR nominal de resolución de nombres y difiere cualquier esquema posterior a tipado/elaboración hasta que esas fases estén desarrolladas. La auditoría exige por tanto coherencia del AST superficial, capítulo 09 y HIR nominal; los requisitos semánticos posteriores se clasifican como `M` cuando todavía no existe su superficie canónica.

El grafo nominal queda limitado a `Owns`, `Specializes` y `RefersTo`. Tipos efectivos, dominios, cardinalidades, efectos y dependencias semánticas no se introducen en el HIR para compensar la ausencia de una representación posterior.

## Etapa 5 — auditoría específica de la integración D-096

Completada contra el documento fuente original **«Módulos, frontera semántica, callables, `look`, `message` y activación»** suministrado para esta auditoría. Se recorrieron sus decisiones acordadas, sintaxis, semántica, restricciones, consecuencias, ejemplos válidos e inválidos, casos límite, decisiones provisionales, preguntas abiertas, alternativas descartadas y el apéndice final **«`on` sobre valores finitos»**.

Cada afirmación sustantiva queda cubierta por una única fila de la matriz siguiente. Los ejemplos, contraejemplos y alternativas descartadas se asignan a la misma fila que la regla positiva cuya frontera ilustran; no se cuentan como decisiones independientes para evitar duplicar su clasificación.

### Matriz de trazabilidad de la fuente

| ID | Afirmación o grupo inseparable de afirmaciones de la fuente | Estado | Superficie vigente o hogar pendiente |
| --- | --- | --- | --- |
| S5-01 | `then` posee una única superficie que puede mezclar locales, efectos, llamadas a `action`/`subaction` y `for each`. | Mecánicamente integrada | EBNF, CST/AST superficial y `EffectBlock`. |
| S5-02 | La ejecución de un `then` es textual sobre el delta privado; las llamadas internas comparten resolución; los `after` se comprueban sobre el estado estable tentativo final; la iteración ordenada/no ordenada conserva su semántica propia. | M | efectos, evaluación, resultados de action y estabilización. |
| S5-03 | `action` y `subaction` pueden invocarse desde cualquier `then`; solo `action` puede ser raíz exterior; `failed` y `rejected` anidados abortan y revierten conservando su categoría. | M | actions, efectos, resultados y evaluación. |
| S5-04 | `~private` deja de ser metadato estándar y default de archivo; no existen modificadores `public`/`private`/`internal` equivalentes. | Mecánicamente integrada | léxico, gramática y sistema general de metadata. `private` no está reservado: puede seguir siendo un identificador de metadata de usuario sin semántica de visibilidad. |
| S5-05 | La exposición se deriva de categoría, módulo, contratos visibles y cierre de tipos; la frontera intermodular operacional es `action`/`look`/`message` y `test` solo en pruebas, y la frontera host excluye `test`. | M | módulos, tipos y frontera pública. |
| S5-06 | La pertenencia a módulo no forma parte del ancla nominal. | Integrada | `09-nombres-y-anclas.md`. |
| S5-07 | `mud.module` delimita por ancestro más cercano; un `.mud` huérfano es inválido; un módulo anidado abre frontera; el nombre lógico deriva del MudPath; `uses` autoriza contrato y `using` solo resuelve nombres; los ciclos `uses` son legales con warning y no inducen orden. | Integrada | `05-texto-fuente.md`. |
| S5-08 | La gramática/formato completo de `mud.module` permanece sin fijar sin reabrir nombre, descubrimiento ni papel de `uses`. | Pregunta abierta | Q-062. |
| S5-09 | Un contrato intermodular arrastra el cierre mínimo transitivo de tipos necesario para `for`, `given`, `on`, resultados de `look`, payloads de `message`, aliases, families, magnitudes y demás formas expuestas. | M | sistema de tipos + frontera pública. |
| S5-10 | La reflexión entre módulos solo es válida si el contrato garantiza que no expone entidades invisibles; no existe filtrado silencioso de resultados reflectivos. | M | reflexión, tipos y frontera pública. |
| S5-11 | La especialización de `thing` no cruza módulos. | M | `11-things.md` + módulos. |
| S5-12 | Cada módulo aporta como máximo un `start with`; solo activa ciclo de vida propio; las contribuciones de todos los módulos se materializan conjuntamente y no establecen orden de inicialización. | Integrada | `04-modelo-matematico.md` + `05-texto-fuente.md`. |
| S5-13 | `start with` usa una contribución directa o un bloque y no contiene secciones `things`/`rules`. | Mecánicamente integrada | léxico, EBNF, CST y AST `ModuleStartDecl(StartSet)`. |
| S5-14 | El conjunto de activación reúne `thing \| rule`, es plano, no ordenado y deduplicado; cada expresión puede aportar cero, una o varias declaraciones; no equivale a `for each create`. | Integrada | `04-modelo-matematico.md`; forma mecánica en `StartSet`. |
| S5-15 | Existe `all D` además de `all` contextual. | Mecánicamente integrada | léxico, EBNF y AST. |
| S5-16 | `all D` materializa la enumeración canónica finita cuando se exige exhaustividad, respeta visibilidad reflectiva y distingue categorías como `thing` del tipo incorporado `Thing`. | M | dominios, tipos, reflexión y evaluación. |
| S5-17 | Recorridos/cuantificadores pueden consumir dominios directamente, pero selección y `take` que producen colección exigen materialización explícita `all D`; la selección no fabrica un `Domain`. | M | expresiones, dominios y colecciones. La sintaxis compatible ya existe. |
| S5-18 | Pertenencia `x in D`, restricción declarativa `a: A in D` y selección `x in source: predicate` son construcciones distintas. | Mecánicamente integrada | EBNF y AST superficial. |
| S5-19 | Los descriptores de comportamiento son valores first-class, pertenecen a `Any`, participan en una jerarquía reflectiva y pueden estrecharse con `is`. | M | sistema de tipos, reflexión y narrowing. |
| S5-20 | Los tipos callable de superficie son `A.action(B...)`, `(A,C).action(B...)`, `A.rule(B...)` y `A.look(B...)`; `rule` callable significa regla booleana y no existe grafía `A.subaction(...)` por el mero subtyping. | Mecánicamente integrada | EBNF y AST `CallableType(ActionCallable\|RuleCallable\|LookCallable)`. |
| S5-21 | La selección puede filtrar colecciones de descriptores por un contrato callable y estrechar sus miembros; `all A.action(B)` puede enumerar directamente el dominio compatible visible. | M | tipos, expresiones, selección y reflexión. |
| S5-22 | `look` posee superficie propia con `for`, `given` y campos públicos. | Mecánicamente integrada | EBNF, CST y `LookDecl`. |
| S5-23 | `look` es puro y callable desde host/MUD según visibilidad; sus `given` siguen el contrato general; hereda una única `ReadView` coherente y puede leer efectos privados anteriores del mismo `then`; los fallos dinámicos de dominio se distinguen por contexto. | M | frontera pública, evaluación, actions y rules. |
| S5-24 | Cada `look` induce un único resultado anónimo formado por campos públicos, sin ancla por ese hecho; una llamada produce un valor y la multiplicidad vive en campos; el tipo puede nombrarse después mediante alias. | M | sistema de tipos, `look` y reflexión. |
| S5-25 | Una llamada concreta de `look` no es una expresión de tipo; `...~type` sí puede aparecer en posición de tipo cuando el análisis demuestra `Type`; un tipo callable ya denota `Type`. | Mecánicamente integrada | EBNF y AST `ReflectedType`; las reglas estáticas completas quedan en tipos. |
| S5-26 | `message` posee declaración propia con `on`, locales previas, `when`, `if` y campos públicos, sin una operación `emit`. | Mecánicamente integrada | EBNF, CST y `MessageDecl`. |
| S5-27 | Un `message` es una ocurrencia causal, no una función ni un `Bool`; su payload es un tipo anónimo y referenciarlo en `when` produce un trigger de ocurrencia. | M | ondas, mensajes, evaluación y tipos. |
| S5-28 | `message`, rule reactiva y `always` comparten el lenguaje causal de triggers; actions, subactions, looks, rules booleanas y tests no son fuentes; una declaración `on` usada como trigger no es una llamada y puede observar todas o restringir algunas vinculaciones. | M | triggers, ondas y resolución dependiente de tipos. |
| S5-29 | Una rule reactiva como trigger pulsa cuando dispara; una `always` pulsa en cada onda aplicable y no solo cuando falla, con warning de posible causalidad inútil. | M | rules y ondas. |
| S5-30 | Un trigger produce cero o más matches con testigos y multiplicidad; `and` hace natural join/producto cartesiano, `or` unión; no se deduplican ocurrencias distintas por payload ni existe desigualdad implícita; la disponibilidad de bindings es flow-sensitive. | M | álgebra de triggers, análisis de flujo y ondas. |
| S5-31 | Las ocurrencias nacidas en una onda alimentan la siguiente; no ejecutan consumidores por orden físico; estabilizar exige ausencia de efectos y consecuencias causales pendientes; un ciclo puramente causal puede impedir estabilización sin cambio de estado. | M | ondas y estabilización. |
| S5-32 | Una ocurrencia de `message` conserva identidad, declaración, bindings y vista causal; `when`/`if` se resuelven causalmente; MUD proyecta payload en la vista causal y el host en el estado estable final; rollback cancela entrega exterior; la envoltura host separa bindings y payload. | M | messages, ondas y frontera host. El borde de participantes desaparecidos queda en Q-067. |
| S5-33 | `action`, rule reactiva y `message` admiten locales puras `:=` antes de sus cláusulas principales. | Mecánicamente integrada | EBNF, CST y AST `leading_locals`. |
| S5-34 | Las locales previas son inmutables, secuenciales y sometidas a scopes ordinarios; una local de trigger no adquiere payload hasta que un match flow-sensitive garantiza su binding. | M | resolución, análisis de flujo y triggers. |
| S5-35 | `Any` es tipo superior real; `is` puede estrechar valores y descriptores; `e~type` devuelve el tipo estático actual después del narrowing y es determinable durante elaboración. | M | sistema de tipos y elaboración. |
| S5-36 | `subaction <: action <: Declaration`, pero subtyping y capacidad de raíz exterior son dimensiones distintas y un upcast no concede capacidad exterior. | M | tipos callable + frontera pública. La varianza completa queda en Q-063. |
| S5-37 | Un callable almacenado se invoca con la sintaxis ordinaria de receptor, sin forma especial `.(op)`. | Mecánicamente integrada | gramática/AST ordinarios de acceso y llamada. |
| S5-38 | Almacenar un descriptor no pre-vincula receptores ni `given`; la vinculación se realiza al invocar. | M | llamadas, tipos y evaluación. El binding nominal tras borrado queda en Q-066. |
| S5-39 | Una llamada dinámica de `look` usa el tipo común más específico de todos los resultados posibles; si no existe un supertipo común adecuado se conserva la alternativa mediante unión; el narrowing del descriptor puede estrechar el resultado. | M | sistema de tipos. El caso de varios mínimos comunes incomparables queda en Q-065. |
| S5-40 | La API host canónica se organiza por identidad de `action`/`look`/`message`, no alrededor de un participante arbitrario como propietario; `test` no entra en producción. | M | frontera pública. |
| S5-41 | Un test raíz usa un mundo fresco y el cierre transitivo estático de tests alcanzables para reunir `start with`; las contribuciones se materializan conjuntamente y una llamada posterior no reactiva ese setup. | Integrada | `04-modelo-matematico.md`; D-055 conserva el detalle operativo. |
| S5-42 | Los tests pueden cruzar módulos únicamente en contexto de pruebas, mediante contrato visible y `uses`; el detalle completo de setup, ejecución y frontera de pruebas permanece para su capítulo canónico. | M | `43-tests-declarativos.md` + módulos. |
| S5-43 | `on` relacionado admite `nombre[: Tipo] in fuente` con una expresión fuente, además del universo implícito de `thing` de la forma directa. | Mecánicamente integrada | EBNF `on-participant` y AST `RelatedOnParticipant`. |
| S5-44 | Una fuente explícita de `on` puede aportar valores no-`thing` si es finita y enumerable; cada valor forma un binding independiente con memoria temporal propia; tipos como `Nat` no tienen universo directo infinito implícito. | M | reglas, bindings, finitud y ondas. D-063 conserva autoridad transitoria. |
| S5-45 | La representación mecánica exacta de los testigos/bindings de trigger queda deliberadamente sin fijar; cualquier futura representación debe preservar natural join, unión y disponibilidad flow-sensitive. | Pregunta abierta | decisión provisional no numerada; D-097 impide fijar prematuramente un IR semántico. |
| S5-46 | Namespaces, nombres de métodos, tipos de referencia, suscripciones y ergonomía generada de TypeScript/Rust/C++ u otros hosts no forman parte todavía de la semántica MUD. | Pregunta abierta | decisión provisional de materialización host. |
| S5-47 | Compatibilidad y varianza exacta de tipos callable. | Pregunta abierta | Q-063. |
| S5-48 | Especialización nominal de aliases a través de módulos. | Pregunta abierta | Q-064. |
| S5-49 | Elección formal del join de resultados de `look` cuando existen varios mínimos comunes incomparables. | Pregunta abierta | Q-065. |
| S5-50 | Binding nominal al invocar un descriptor callable cuyo tipo ha borrado identidad suficiente de la declaración. | Pregunta abierta | Q-066. |
| S5-51 | Proyección exterior de un `message` cuando un participante capturado deja de existir o estar activo antes del estado final. | Pregunta abierta | Q-067. |
| S5-52 | Identidad e igualdad estructural de tipos anónimos de resultados de `look`, payloads de `message` y formas equivalentes. | Pregunta abierta | Q-068. |

### Cobertura de las demás secciones de la fuente

- **Sintaxis:** todos sus ejemplos son testigos de S5-01, S5-13, S5-15, S5-20, S5-22, S5-25, S5-28, S5-33, S5-37 y S5-43. No introduce una regla adicional.
- **Semántica:** sus tablas y casos de accesibilidad/proyección desarrollan S5-02, S5-05, S5-09, S5-10, S5-23, S5-27 a S5-32, S5-40 a S5-42.
- **Restricciones e invariantes:** son reformulaciones de S5-02 a S5-05, S5-07, S5-10 a S5-18, S5-23 a S5-40 y no añaden una obligación independiente.
- **Interacciones y consecuencias:** el grafo causal combinado, la consulta pública por `look`, la doble función de `message`, la generalización de `Trigger`, el cierre exterior/intermodular y las necesidades de tooling quedan absorbidos por S5-05, S5-09, S5-19 a S5-32 y S5-40. Las “divergencias conocidas” del documento fuente fueron comprobadas contra las decisiones que debía modificar y ya no describen el estado actual.
- **Ejemplos válidos, inválidos y casos límite:** se comprobaron como testigos de las filas anteriores; no se detectó un ejemplo que exija una regla ausente o contradiga el estado vigente.
- **Alternativas descartadas:** las 27 alternativas se verificaron contra la regla positiva correspondiente. No reaparecen como diseño vigente: separación elemental/compuesta (S5-01/02), hojas contra mismo estado inicial (S5-02), `look` solo exterior (S5-23), alias obligatorio o llamada concreta como tipo (S5-24/25), `~type` sobre tipo callable y anclas sintéticas (S5-20/24/25), message como `on`/Bool/`emit` o actions como triggers (S5-27/28), semántica invertida de `always` (S5-29), paréntesis o captura imperativa de triggers (S5-28/34), filtrado reflectivo silencioso y herencia cross-module (S5-10/11), módulo en anclas o dotfile (S5-06/07), `~private` (S5-04), secciones antiguas y `for each create` en activación (S5-13/14), fusión de los significados de `in` o dominios refinados por predicado (S5-17/18), primer participante como propietario host (S5-40), prebinding de action y `.(op)` (S5-37/38).
- **Apéndice «`on` sobre valores finitos»:** modifica dentro de la propia fuente la formulación anterior que describía `on` exclusivamente como bindings de `thing`. La formulación final marcada **Acordado** es la autoridad de esa fuente y queda trazada por S5-43/44.

### Comprobaciones de procedencia reservadas para esta etapa

**`~private`.** La fuente retira `~private` como metadato **estándar**, como default de archivo y como mecanismo de visibilidad. No ordena reservar o prohibir el identificador `private` como nombre de metadata definido por el usuario. El estado actual es fiel: no existe `~private` estándar ni palabra reservada `private`, y `metadata-name` sigue admitiendo identificadores de usuario. No hay fortalecimiento `U`.

**Join dinámico de `look`.** La fuente dice expresamente que se usa el supertipo común más específico y que, cuando no existe un padre/supertipo común adecuado, se necesita una unión de tipos. También deja abierto el caso de varios supertipos comunes mínimos incomparables. D-096 y Q-065 conservan exactamente esa frontera. La regla de fallback a unión no es un fortalecimiento añadido por la integración. No hay `U`.

**`on` sobre valores finitos.** La fuente añade al final, como decisión acordada, que `on` relacionado puede obtener valores de una fuente finita enumerable aunque no sean `thing`, con memoria temporal por binding; la forma directa conserva el universo implícito finito de `thing`. D-063, EBNF y AST reflejan la ampliación. No hay omisión ni contradicción.

### Resultado de la Etapa 5

- Afirmaciones sustantivas de la fuente sin clasificar: **0**.
- Sospechas `U` pendientes: **0**.
- Contradicciones nuevas `C`/`X`: **0**.
- Integraciones incompletas nuevas `I`: **0**.
- Preguntas tratadas incorrectamente `Q`: **0**.
- Las preguntas Q-062 a Q-068 siguen abiertas únicamente en el alcance que la fuente dejó sin decidir.
- Q-051 y Q-052 permanecen correctamente cerradas por D-096; sus bordes no resueltos están separados en Q-065/Q-068 y Q-067 respectivamente.

Con ello se cumple el criterio de cierre de la Etapa 5 sin modificar semántica normativa: la auditoría no necesita corregir D-096 ni abrir una decisión nueva.

## Semántica aceptada pendiente de formalización

Los siguientes puntos no son defectos por su mera ausencia actual. Deben conservarse como obligaciones para cuando se desarrollen sus superficies canónicas.

| Obligación | Estado | Hogar probable |
| --- | --- | --- |
| Compatibilidad y varianza exacta entre tipos callable | Pregunta abierta | `10-sistema-de-tipos.md` |
| Binding nominal de un descriptor callable cuyo tipo se haya borrado o ensanchado | Pregunta abierta, Q-066 | tipos / expresiones / frontera pública |
| Almacenar un descriptor callable no pre-vincula receptor ni argumentos `given`; la vinculación ocurre en la invocación | M | expresiones / frontera pública / evaluación |
| Violación dinámica del dominio de un `given` de `look`: error de consulta desde host y posible `failed` dentro de una resolución | M | frontera pública + evaluación/acciones |
| Join de resultados de `look` invocado dinámicamente | Parte aceptada + Q-065 | tipos / frontera pública |
| Una `thing` visible entre módulos expone identidad y tipo nominal, no sus campos ordinarios; el estado público se proyecta mediante `look` | M | `11-things.md` + frontera pública |
| Reflexión cruzada segura por contrato y sin filtrado silencioso | M | tipos / reflexión / frontera pública |
| Una `thing` no puede especializar otra `thing` de otro módulo | M | `11-things.md` |
| La API host canónica se organiza alrededor de la identidad de las operaciones públicas, no de un participante arbitrario como propietario | M | frontera pública |
| Un ciclo puramente causal de mensajes/disparos puede impedir la estabilización aunque el estado no cambie | M | ondas / estabilización |
| Proyección causal interna y proyección final al host de `message`, con rollback que cancela entrega exterior | M en detalle | frontera pública + ondas |
| Los tests incorporan el cierre transitivo estático de `start with` de los tests alcanzables | M en detalle | `43-tests-declarativos.md` |
| `on` relacionado puede vincular valores de una fuente finita enumerable no-`thing`; la memoria reactiva pertenece a cada binding | M | reglas / finitud / ondas |

Cuando aparezca cualquiera de estos capítulos, MUD-EDIT-003 obliga a promover la regla a esa superficie. Hasta entonces no debe duplicarse en un capítulo impropio solo para «tenerla en specification».

## Etapa 6 — mapa futuro

Completada mediante una revisión íntegra de todas las entradas `Archivo previsto` de `especificacion/README.md`. El mapa se redujo a alcance editorial y obligaciones que los capítulos futuros deberán absorber, evitando que el propio índice actúe como una segunda especificación anticipada.

La revisión detectó y corrigió cuatro residuos semánticos concretos:

| ID | Defecto del mapa previo | Corrección |
| --- | --- | --- |
| E6-01 | El capítulo 12 todavía prohibía especialización/herencia de aliases. | El mapa refleja especialización nominal simple/múltiple, herencia de representación o miembros y mantiene abierta la frontera intermodular de Q-064. |
| E6-02 | El capítulo 21 conservaba la regla antigua de nombre obligatorio solo para ciertos roles `for`. | El mapa exige participantes `for` explícitamente nombrados, coherente con el modelo reflectivo vigente. |
| E6-03 | El capítulo 43 incorporaba activación ordinaria de módulos al mundo inicial de un test. | El mapa limita el cierre inicial a las contribuciones `start with` propias de los tests estáticamente alcanzables; la activación ordinaria de módulos queda fuera. |
| E6-04 | Los capítulos 41, 44, 48 y el criterio global seguían presuponiendo un IR semántico actual, un JSON Schema y artefactos derivados. | El mapa conserva solo una futura representación posterior a tipado/elaboración, sin fijar esquema, nodos, versión ni serialización actuales; conformidad y migraciones se refieren a artefactos normativos que realmente existan. |

Además se propagaron al alcance de los capítulos futuros las obligaciones `M` de Etapa 5 que podían perderse si el mapa conservaba el diseño anterior: cierre de tipos y reflexión modular segura, límite de especialización de `thing` entre módulos, `all D`, callables almacenados, joins dinámicos de `look`, tipos anónimos, trigger algebra, causalidad de `message`, proyecciones host, ciclos puramente causales y bindings `on` sobre fuentes finitas.

Las preguntas Q-063 a Q-068 aparecen en el frontmatter del índice porque el mapa delimita explícitamente sus incertidumbres presentes. Ninguna se resuelve ni amplía.

**Criterio de cierre cumplido:** el mapa futuro es compatible con el estado vigente, conserva las obligaciones necesarias para los hogares todavía inexistentes y ya no formaliza anticipadamente un IR ni otras estructuras internas no desarrolladas.

## Etapa 7 — barrera mecánica

Completada mediante `gobierno/validate_spec_editorial.py` y su suite `gobierno/test_validate_spec_editorial.py`. La barrera recorre Markdown y artefactos mecánicos textuales de `especificacion/` (`.md`, `.ebnf`, `.asdl`, `.yaml` y `.yml`), excluyendo únicamente `00-convenciones-editoriales.md`, que necesariamente contiene los ejemplos y definiciones de la propia regla.

El validador detecta mecánicamente:

- identificadores `D-NNN` o `ADR-NNN` en el cuerpo de la especificación, separando previamente el frontmatter Markdown;
- encabezados inequívocos de actualización/revisión/corrección/sustitución editorial y formulaciones que sustituyen explícitamente una regla, redacción o versión anterior;
- referencias corporales a preguntas inexistentes o inactivas;
- referencias corporales a preguntas activas ausentes de `questions:` cuando el Markdown dispone de frontmatter;
- preguntas inexistentes o inactivas conservadas en `questions:`.

La suite contiene diez fixtures representativos: caso válido con Q activa, IDs `D-NNN` y `ADR-NNN` indebidos, encabezado y frase de migración editorial, Q cerrada en cuerpo, Q activa no declarada, Q cerrada en frontmatter, Q inexistente y referencia válida desde un artefacto sin frontmatter. También verifica que el documento de convenciones quede excluido.

Deliberadamente no se intenta decidir por regex si palabras generales como «antes», «anterior», «retirado» o una negación describen historia o una regla vigente. Esa revisión semántica permanece reservada a la Etapa 8.

La barrera queda incorporada al ciclo documental y a `AGENTS.md`: los cambios que afecten `especificacion/` o `notas/preguntas/` deben ejecutarla antes del commit, y los cambios al propio validador deben ejecutar además su suite de fixtures.

**Criterio de cierre cumplido:** los fixtures de regresión fallan con códigos específicos y la especificación saneada pasa la barrera completa.

## Etapa 8 — auditoría final

Antes de considerar cerrado el saneamiento:

1. buscar globalmente `D-NNN`/`ADR-NNN` en cuerpos de `especificacion/`;
2. revisar manualmente términos de riesgo editorial como `retirado`, `sustituye`, `actualización`, `migrada`, `antes` y `anterior`;
3. comprobar referencias y frontmatter de todas las preguntas activas;
4. comprobar que ninguna pregunta cerrada siga activa en la especificación;
5. cruzar decisiones vigentes con superficies desarrolladas;
6. comprobar coherencia prosa ↔ EBNF ↔ CST ↔ AST ↔ HIR nominal y tratar cualquier futura representación posterior solo cuando exista;
7. ejecutar todos los validadores oficiales y la barrera editorial de Etapa 7;
8. revisar el diff global del saneamiento para detectar cambios semánticos accidentales.

**Criterio de cierre global:** una persona puede leer solo las superficies ya desarrolladas de `especificacion/` y obtener el estado formalizado vigente de MUD sin reconstruir historia decisional ni encontrar contradicciones conocidas; las reglas aceptadas cuyo capítulo aún no existe permanecen localizables como autoridad transitoria y obligaciones `M`, no como apéndices impropios.
