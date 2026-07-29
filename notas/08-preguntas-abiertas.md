# Registro de preguntas en migración

> [!warning]
> Este registro conserva temporalmente preguntas anteriores mientras se separan en `notas/preguntas/`. El índice activo y la política vigente están en [[notas/preguntas/README|Preguntas activas de MUD]] y [[gobierno/POLITICA-DE-PREGUNTAS|Política de preguntas de MUD]]. Las entradas marcadas como cerradas son históricas y no forman parte de la agenda activa.

Una pregunta solo se considera cerrada cuando existe una decisión registrada, una actualización del documento dueño y pruebas cuando corresponda.

Prioridades:

- **P0**: bloquea el núcleo v0 o puede forzar una reescritura cercana.
- **P1**: bloquea una fase posterior concreta.
- **P2**: puede aplazarse sin falsear el núcleo.

## P0 — Antes de congelar el núcleo

### Q-001 — Gramática y saltos de línea

Estado: **cerrada** mediante [[notas/decisiones/ADR-050-comentarios-terminadores-y-separadores-numericos|D-050]], [[notas/decisiones/ADR-056-char-texto-y-orden-unicode|D-056]] y [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|D-057]].

Una instrucción termina mediante `;` o salto de línea. El salto continúa cuando el prefijo todavía no puede formar una unidad sintáctica completa pero admite una continuación válida; la sangría no interviene.

La sintaxis completa vive en `especificacion/gramatica/`; [[especificacion/07-gramatica-concreta]] fija precedencia, prefijos abiertos y distinciones contextuales. La recuperación de errores puede variar entre implementaciones, pero nunca amplía el lenguaje aceptado.

### Q-002 — Modelo exacto de efectos secuenciales y simultáneos

¿Qué estado lee cada instrucción de un `then` elemental y cada hoja de una acción compuesta? ¿Cómo se combinan efectos de una misma raíz?

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]], [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]] y [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]].

Cada `then` se interpreta secuencialmente sobre un delta privado derivado de la instantánea común y no observa deltas parciales ajenos. En `Natural`, una lectura privada proyecta a cero la suma del valor inicial y el delta local acumulado sin recortar el delta. Las hojas de una acción compuesta leen el mismo estado inicial y forman una raíz simultánea. Falta una semántica operacional para las lecturas intermedias de las demás familias de efectos y todas sus combinaciones.

### Q-003 — Puntos de validación

¿En qué momento exacto se validan dominios, cardinalidades y `always`: tras cada escritura, al cerrar la raíz, al cerrar cada onda o en varios de esos puntos?

La respuesta afecta qué estados tentativos son observables para reglas posteriores.

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]] y [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]].

La cardinalidad final se demuestra estáticamente para cada `then` y para toda consolidación concurrente posible. Los estados intermedios dentro del delta privado de un `then` pueden incumplirla. Los dominios se preservan en inicialización, materialización, especialización, escrituras, raíces, ondas y estados publicables. Siguen abiertos la formulación operacional unificada, el tratamiento exacto de referencias suspendidas y los puntos de comprobación de reglas `always`.

### Q-004 — Rollback de `rejected`

Estado: **cerrada** mediante [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]].

Todo resultado distinto de `accepted`, incluido un `after` falso, restaura exactamente el estado estable anterior y no publica mensajes ni efectos externos.

### Q-005 — Identidad y ciclo de vida de vinculaciones

¿Cómo se identifica canónicamente una vinculación `on`, cuándo se elimina su memoria y qué ocurre si una vinculación equivalente desaparece y reaparece?

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola|D-045]] y [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]].

La memoria temporal pertenece a la vinculación; estas se fijan al inicio de cada onda y sus altas o bajas surten efecto en la siguiente. Una vinculación presente en la primera instantánea materializada por `start with` usa un anterior virtual falso para ramas booleanas y la propia instantánea para `changes` y `old`; una nacida después usa su primera onda activa para establecer toda la línea base sin disparar. Falta definir su identidad canónica y la política de eliminación o conservación de memoria cuando desaparece.

### Q-006 — Conflictos

¿Cuál es la matriz completa de compatibilidad entre asignaciones, incrementos, multiplicaciones y operaciones estructurales concurrentes?

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]], [[notas/decisiones/ADR-039-colecciones-y-diccionarios|D-039]], [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]] y [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]].

Ya están fijadas asignaciones iguales o distintas, acumulaciones homogéneas, mezclas aritméticas incompatibles, el núcleo estructural y la consolidación idempotente de varias adiciones del mismo valor a una colección `unique`. En `Natural`, los deltas aditivos se suman como enteros firmados y solo después se normalizan a cero. Falta completar la matriz para adiciones y retiradas combinadas, inserciones distintas con orden observable, límites de cardinalidad, diccionarios, propiedades, ciclo de vida y destinos parcialmente solapados.

### Q-007 — Fallos técnicos

¿Qué estructura tiene un error técnico y cómo se distingue de `failed` semántico, de un límite de recursos y de un defecto del runtime?

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-043-consulta-especulativa-allowed|D-043]], [[notas/decisiones/ADR-048-azar-reproducible-y-fallos|D-048]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].

Un fallo semántico revierte la acción y se propaga en `allowed`; no equivale a rechazo ni falsedad. Todo resultado externo distinto de `accepted` exige `reason: Text`, por lo que tanto los rechazos como los fallos normativos aportan un diagnóstico humano. Un límite de recursos o defecto interno debe distinguirse de ellos. Falta fijar la estructura y el orden canónicos al agregar varias causas, el contrato adicional de códigos y trazas para CLI, plugin y materializaciones y la tabla de errores en expresiones ordinarias.

### Q-008 — Protocolo Git y `READ`

¿Qué operaciones producen commit? Propuesta: consultas `READ` no; CREATE, UPDATE, RETIRE y migraciones sí.

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-053-operador-semantico-y-flujo-de-autoria|D-053]].

Las consultas `READ` puras no producen commit y todo cambio confirmado se limita al plan sin descartar trabajo ajeno. Falta fijar el formato estable del mensaje, el aislamiento técnico y qué derivados se versionan.

### Q-009 — Forma canónica del IR

¿Cuál es el esquema versionado mínimo, cómo conserva procedencia y qué normalizaciones realiza?

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]].

El IR es reconstruible, versionado, usa anclas, conserva procedencia y representa todas las distinciones semánticas enumeradas en D-051. Falta el esquema ejecutable, los nombres de campos y las reglas de compatibilidad.

### Q-010 — Estado de las decisiones de la fuente

Estado: **cerrada** mediante [[notas/13-auditoria-de-cobertura-y-divergencias]].

Las 78 secciones fueron migradas, sustituidas o retiradas de forma explícita. Ninguna fórmula como «se mantiene vigente» conserva autoridad propia ni presupone texto ausente: el contenido actual debe existir en una decisión, nota dueña, capítulo o pregunta abierta.

### Q-041 — Ontología de `thing`

Estado: **cerrada**.

¿Cuál es la estructura matemática común de las `thing` declaradas y las activadas durante la ejecución, y qué añade `create` al mundo?

Decisión: [[notas/decisiones/ADR-014-ontologia-unificada-de-things|ADR-014]].

MUD tiene un único dominio conceptual de `thing`. Toda `thing` concreta es una cosa con identidad y estado propio que también puede ser antecesora. Las abstractas pertenecen al mismo dominio, pero no denotan directamente una cosa concreta. D-054 precisa que todas se definen canónicamente en el nivel superior; `start with` o `create Nombre` las activan sin cambiar su identidad. `is` es reflexivo y transitivo.

Las consecuencias se separaron en Q-042 y Q-043 y quedaron resueltas mediante [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]].

### Q-042 — Especialización desde una `thing` concreta

Estado: **cerrada**.

Cuando una `thing` concreta $B$ se especializa a partir de otra `thing` concreta $A$, ¿hereda solo las declaraciones, restricciones y valores predeterminados de $A$, o copia u observa también su estado mutable actual?

Decisión: [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]].

Se heredan esquema y predeterminados efectivos, nunca estado activo. Cada `thing` concreta posee estado independiente y su primera activación inicializa desde predeterminados antes de aplicar sus asignaciones explícitas.

### Q-043 — Ciclos de especialización

Estado: **cerrada**.

¿Debe rechazarse cualquier ciclo no trivial de especialización directa?

Decisión: [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]].

Todo ciclo de especialización directa es inválido. La relación semántica `is` es un orden parcial.

### Q-044 — Identidad y referencias a `thing` futuras

Estado: **cerrada**.

¿Qué designa el nombre activado por `create A`?

Decisión vigente: [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

`A` posee una única definición canónica de primer nivel y es resoluble antes de estar activa. `create A` solo solicita su activación. Tras `destroy A`, una ejecución posterior reactiva la misma identidad; nunca fabrica un segundo `A` ni modifica sus antecesoras.

Las operaciones que requieran presencia activa deben comprobarla. El nacimiento y la memoria de las vinculaciones `on` continúan coordinados con Q-005.

### Q-045 — Contenido declarativo de `create`

Estado: **cerrada**.

¿Dónde se define el contenido declarativo de una identidad activada mediante `create`?

Decisión vigente: [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

```mud
abstract thing B as A {
    # Única definición canónica.
}

create B
```

`create` no admite bloque, categoría, antecesoras ni contenido declarativo. La definición canónica contiene todas las propiedades, restricciones, predeterminados y antecesoras. La activación solo las incorpora a la proyección efectiva.

### Q-046 — Creación inefectiva dentro de una raíz

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]] y [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

Si una regla contiene `create A` cuando la identidad canónica `A` ya está activa, la regla completa no se ejecuta y no publica ninguno de sus efectos.

Falta decidir:

- Qué resultado obtiene una acción solicitada en el mismo caso: `rejected`, `failed` u otro resultado.
- Si una regla con varias creaciones exige que todas sus identidades estén ausentes.
- Cómo se combinan creaciones de disponibilidad mixta dentro de acciones compuestas.

D-054 exige una única definición completa de primer nivel para cada `thing` y regla. Varias activaciones concurrentes de una misma identidad ausente se consolidan idempotentemente; ya no existen cuerpos ni fragmentos que fusionar. D-031 retira los aliases del sistema de `create` y `destroy`. La activación y destrucción solicitadas por `then` distintos dejan la identidad destruida al cerrar la oleada.

Bloquea la semántica operacional completa de `create`, los conjuntos de efectos y la atomicidad.

### Q-047 — Selección de predeterminados por tipo

Estado de la premisa: **decidida** mediante [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|ADR-017]].

Todo tipo bien formado tiene un valor predeterminado perteneciente a su dominio. Los tipos básicos ya tienen selección concreta; en particular, `Char` usa `'\u{0}'` (`U+0000`). D-031 fija que un alias estructural compone el suyo usando, para cada componente, su predeterminado explícito o el de su tipo efectivo. Falta definir la función concreta para:

- Aliases no estructurales y colecciones con restricciones.
- Intervalos, selección del miembro predeterminado de una familia cerrada y refinamientos.
- Tipos cuyo dominio pueda depender del mundo activo.

Los componentes de un alias estructural pueden reemplazar explícitamente el predeterminado que obtendrían de su tipo. Falta decidir si otras clases de tipo derivado pueden reemplazar su predeterminado intrínseco.

Desde [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]], debe definirse además cómo obtiene predeterminado una colección de `thing` con mínimo positivo. El ancla exacta nunca es candidata; puede ser necesario exigir un descendiente estricto predeterminado o un inicializador explícito.

### Q-048 — Destrucción con descendientes activos

Estado: **cerrada**.

Decisión: [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]].

Las aristas declaradas se conservan en el almacenamiento. La proyección efectiva atraviesa antecesores inactivos y conecta cada descendiente activo con sus antecesores activos más próximos. El descendiente conserva sus propiedades propias, pierde temporalmente lo heredado desde el nodo destruido y recupera la estructura original al recrearlo.

### Q-049 — Destrucción y colecciones de `thing`

Estado: **parcialmente cerrada** mediante [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]].

La destrucción no poda ni reescribe colecciones almacenadas. Si el tipo declarado de una propiedad queda inactivo, la propiedad completa se suspende y conserva orden, multiplicidad, claves, cardinalidad y carga para una recreación posterior. No necesita mutabilidad exterior ni valores de reparación.

Permanece abierta la observación de una identidad inactiva dentro de una colección cuyo tipo declarado continúa efectivo por ser más general. También falta coordinar esta observación con iteraciones, diccionarios, `old` y serialización.

## P1 — Antes de ampliar el lenguaje

### Q-050 — Borrado en operadores booleanos restantes

Estado de la premisa: **decidida** mediante [[notas/decisiones/ADR-022-borrado-de-reglas-booleanas-inactivas|D-022]].

Las llamadas a reglas booleanas inactivas se podan después de un desazucarado canónico a `not`, `and` y `or`. Falta fijar la elaboración de `!=`, `xor`, cuantificadores booleanos y las interacciones con `allowed`, `eventually` y fallos internos.

### Q-011 — Vinculación nombrada de participantes

Estado: **cerrada** mediante [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|D-036]].

Una llamada puede usar un receptor posicional o un receptor nombrado entre paréntesis. La forma nombrada debe ser exacta y exhaustiva: no admite roles ausentes, repetidos ni desconocidos. Los roles `for` pueden contener cualquier tipo de valor; una colección ocupa una sola posición y no se expande. Una `thing` se vincula por identidad, un valor inmutable por valor y un rol exteriormente mutable por lugar almacenado. El orden de la declaración sigue siendo canónico y los argumentos posteriores corresponden exclusivamente a `given`.

### Q-012 — Valores `given` nombrados

Estado: **cerrada** mediante [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|D-036]].

Los argumentos `given` son siempre posicionales y pueden llevar la etiqueta opcional `nombre =` para mejorar la lectura. Se pueden mezclar argumentos etiquetados y no etiquetados en cualquier posición; una etiqueta debe coincidir con el `given` declarado en esa misma posición y nunca permite reordenar.

### Q-013 — Restricciones relacionales entre participantes `on`

Estado: **cerrada** mediante [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|D-036]].

La cabecera puede construir participantes relacionados mediante `role: Type in previousRole.relation`. Las condiciones relacionales que no formen parte de esa vinculación estructural se expresan en `if`; `given` no está permitido en declaraciones `on`.

### Q-014 — Migración de anclas

¿Cómo se renombra o mueve una declaración sin perder historia, referencias ni compatibilidad?

### Q-015 — Retirada

¿`RETIRE` marca obsolescencia, exige reemplazo, elimina físicamente o admite varias fases?

### Q-016 — Canonicalización de identidades activadas durante la ejecución

Formato estable de la reserva global, snapshots, comparación, referencias y ciclos de activación–destrucción–reactivación.

### Q-017 — Dominios dinámicos circulares

Qué ciclos son inválidos y si existe un punto fijo admisible.

### Q-018 — Intervalos discontinuos

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]] y [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]].

Los intervalos se normalizan por contenido. En los lineales, extremos efectivos invertidos producen `empty` y no implican recorrido descendente ni ciclo. Permanecen abiertos la sintaxis consolidada de intervalos discontinuos, el orden descendente explícito y varias claves.

### Q-019 — Números

Estado de la premisa: **parcialmente decidida** mediante [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]], [[notas/decisiones/ADR-034-number-exacto-y-rumber-binary64|D-034]], [[notas/decisiones/ADR-040-semantica-numerica-basica-restante|D-040]] y [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]].

`Natural`, `Integer`, `Number`, `Rumber` y `Money` son representaciones numéricas básicas. `Number` es racional exacto; `Rumber` es `binary64`; no se mezclan implícitamente. `Money` usa decimal exacto de escala dos, no tiene sufijo literal y aplica el redondeo global al más cercano con empates al par. La ampliación exacta ordinaria sigue `Natural → Integer → Number`. La resta pura de naturales satura en cero; los efectos aditivos suman deltas firmados antes de una única normalización. Falta fijar:

- Los límites de representación y overflow de `Natural`, `Integer` y `Money`.
- La matriz completa de inferencia de `Money` frente a otras representaciones y magnitudes.
- Los fallos aritméticos no cubiertos expresamente por D-034.

### Q-020 — Oscilaciones y límite de ondas

Detección semántica, salvaguarda técnica, diagnósticos y reproducibilidad.

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola|D-045]].

Una oscilación semántica produce `failed`; un límite de recursos es una salvaguarda técnica distinguible. Falta el algoritmo normativo de detección, la configuración portable y los diagnósticos.

### Q-021 — Análisis estático de conflictos

Qué conflictos pueden probarse en compilación y cuáles solo en una resolución concreta.

D-023 y [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]] establecen el criterio inicial: un conflicto que el compilador pueda demostrar se rechaza estáticamente; la coincidencia que no pueda decidir se valida en runtime y revierte la transacción si llega a ocurrir. D-054 retira de esta categoría las activaciones coincidentes de una misma `thing` o regla: son idempotentes porque sus definiciones son únicas. D-031 hace inaplicable el caso de aliases.

D-026 endurece el caso de cardinalidad: el compilador debe demostrar la preservación local y consolidada; si no puede, rechaza conservadoramente el programa en vez de diferir el caso al runtime.

### Q-051 — Identidad y selección de un `look`

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-027-salidas-look-y-message|D-027]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].

Un `look` es una consulta pública pura cuyos campos se evalúan sobre un único estado estable. Una magnitud usada directamente selecciona su unidad con `in`; omitirla usa la unidad raíz o combinación canónica y emite un aviso. Un punto directo publica su coordenada, mientras que su formato se publica construyendo `Text`. Falta definir la sintaxis de solicitud, el tratamiento de participantes inactivos, la posible multiplicidad de filas y la serialización recursiva de aliases, colecciones y magnitudes anidadas.

### Q-052 — Entrega de `message`

Estado de la premisa: **decidida** mediante [[notas/decisiones/ADR-027-salidas-look-y-message|D-027]].

Un `message` detecta un hecho durante la resolución de una acción y evalúa sus campos públicos después de estabilizarla. Falta definir multiplicidad, deduplicación, orden, momento de evaluación de `if`, participantes destruidos y el destino de detecciones pertenecientes a acciones `rejected` o `failed`.

### Q-053 — Conversiones explícitas

Estado: **cerrada** mediante [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]], [[notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal|D-032]], [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]], [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].

`as` queda reservado para especialización. `to` convierte valores cuantitativos compatibles o cambia el tipo nominal entre representaciones estructuralmente compatibles; `in` cambia la unidad de expresión de magnitudes lineales y de punto. En un punto transforma la coordenada completa y evita su `format`; la extracción de partes usa `unidad from contenedor in punto`. Un `given` fuera de dominio produce `rejected`, mientras un estado tentativo con un campo fuera de dominio produce `failed`. La normalización de un intervalo invertido a `empty` no es por sí misma una violación.

### Q-022 — Valores de retorno de acciones

¿Además del resultado operativo, una acción puede producir valores de dominio? Si sí, ¿cómo interactúan con atomicidad y composición?

### Q-023 — Composición dinámica

Si una acción puede seleccionar dinámicamente otras acciones, cómo se conserva aciclicidad y análisis de impacto.

### Q-059 — Observación de resultados de acción en tests

Estado: **abierta** a partir de [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].

¿Cómo comprueba un test que una acción solicitada produjo `accepted`, `rejected` o `failed` sin confundir esos resultados con `passed`, `failed` y `error` del propio test?

Debe decidirse:

- Si una solicitud de acción dentro de `then` puede vincular su resultado a un nombre local.
- Si una acción `rejected` constituye por defecto un error del escenario o un resultado observable.
- Cómo se enlaza el `reason` externo ya definido para `rejected` y `failed`, junto con su traza, sin convertir diagnósticos en valores ordinarios del mundo.

### Q-024 — Datos asociados a miembros de una `family`

Estado: **cerrada** mediante [[notas/decisiones/ADR-038-familias-cerradas-de-valores|D-038]].

Una `family` puede declarar directamente un esquema uniforme de datos inmutables, almacenados o calculados, antes de sus miembros. Cada miembro puede sustituir valores almacenados en un subbloque; los omitidos proceden primero del predeterminado explícito del dato y después del predeterminado de su tipo. Los datos calculados se evalúan estáticamente para cada miembro, tienen tipo opcional si puede inferirse de forma unívoca, admiten dependencias acíclicas con otros datos asociados y no pueden sustituirse en el miembro. Los datos no alteran la identidad ni la igualdad nominal del miembro.

### Q-025 — Destrucción de `thing` estáticas

Estado: **cerrada** mediante [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]] y [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

Toda `thing` se define estáticamente y puede activarse mediante `start with` o `create Nombre`. `destroy` suspende su identidad canónica sin borrar ancla, descriptor, aristas ni carga; una activación posterior restaura la misma declaración.

## P2 — Funciones avanzadas

### Q-026 — Varias acciones en `eventually`

Estado: **parcialmente cerrada** mediante [[notas/decisiones/ADR-044-alcanzabilidad-eventually|D-044]] y [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|D-057]].

`through` acepta una colección contextual, con corchetes opcionales, de referencias a acciones. Falta fijar el orden canónico de enumeración de solicitudes y su posible efecto en testigos y diagnósticos; no afecta a la verdad existencial.

### Q-027 — Estado relevante

Cómo calcular la proyección mínima de estado que conserva la verdad de una consulta de alcanzabilidad.

### Q-028 — Finitud

Límites del análisis, aproximaciones conservadoras y mensajes cuando no puede demostrarse.

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-044-alcanzabilidad-eventually|D-044]] y [[notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita|D-047]].

La incapacidad de demostrar finitud o enumerabilidad rechaza estáticamente el uso que las exige; no produce una respuesta negativa en runtime. Falta definir el análisis y sus diagnósticos.

### Q-029 — Terminación

Qué clases de acciones y reglas puede certificar el compilador.

### Q-030 — Perfil de mundos finitos

Conjunto explícito de restricciones que habilita `eventually`.

### Q-031 — Subconjunto no Turing completo

Si merece la pena definirlo, qué garantías ofrece y cómo convive con el lenguaje general.

### Q-032 — Aleatoriedad reproducible

Subsemillas, cachés, identidad de puntos aleatorios y exposición de campos estocásticos.

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-048-azar-reproducible-y-fallos|D-048]].

Todo punto aleatorio tiene identidad semántica, deriva de una semilla y un campo calculado mantiene su muestra dentro de una instantánea. Falta el algoritmo de subsemillas, cachés, reintentos y exposición.

### Q-033 — Calendarios y localización

Calendario civil inicial, zonas horarias, formatos, idiomas y separación entre valor y presentación.

### Q-034 — Magnitudes derivadas

Estado de la premisa: **decidida** mediante [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|D-028]].

`:=` define composición dimensional; la representación canónica combina unidades raíz y las expresiones compatibles de unidad se admiten automáticamente. Falta concretar el algoritmo de normalización dimensional, sus diagnósticos y las interacciones especiales con `Money`.

### Q-054 — Catálogo y resolución léxica de unidades y prefijos

Qué prefijos incorpora MUD, qué formas ASCII y Unicode reconoce, cómo se resuelven colisiones entre `name`, `plural`, `abbreviation` y formas prefijadas, y qué identidad semántica estable recibe una unidad cuya cabecera no tiene identificador.

### Q-056 — Forma normalizada y recursión de aliases

Definición inductiva de la forma estructural normalizada, tratamiento de aliases anidados, admisión o rechazo de recursión directa e indirecta, decidibilidad de la compatibilidad y enumeración canónica de cada tipo componente.

### Q-057 — Capacidad interior dentro de valores de alias

Si una representación de alias contiene una colección de `thing`, decidir si puede declarar capacidad interior `[mut]` aunque el valor de alias sea inmutable, qué autoridad concede y cómo se conserva la distinción entre modificar un miembro alcanzado y reemplazar la colección contenida.

### Q-058 — Evaluación portable de `Rumber`

Fijar la conversión de la escritura decimal de un literal al patrón `binary64`, el modo de redondeo de cada operación, tratamiento de subnormales y underflow, prohibición o semántica de contracción FMA, precisión de resultados intermedios, canonicalización en IR y reglas de inferencia para magnitudes derivadas cuyos componentes usan `Rumber`.

### Q-035 — Coste de `allowed`

Memorización, profundidad especulativa, ciclos y límites de recursos sin cambiar su verdad semántica.

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-043-consulta-especulativa-allowed|D-043]].

El grafo de admisibilidad es acíclico y un límite de recursos no puede transformarse silenciosamente en falso. Falta definir memorización, presupuestos y diagnóstico.

## Preguntas de producto adicionales

### Q-036 — Unidad de interacción humana

¿La persona aprueba un plan completo, cada operación o solo los cambios clasificados como peligrosos?

### Q-037 — Convivencia con código manual

¿Qué partes de una materialización pueden editarse a mano y cómo se evita que una regeneración las destruya o introduzca semántica oculta?

### Q-038 — Compatibilidad entre versiones del lenguaje

¿Cómo se declara la versión MUD de un proyecto y cómo se migran fuente, IR y materializaciones?

### Q-039 — Explicación suficiente

¿Qué evidencia mínima debe presentar el sistema antes y después de un cambio para que una persona pueda confiar en él?

### Q-040 — Amenazas y permisos

¿Qué operaciones puede ejecutar automáticamente la IA y cuáles requieren autorización por afectar Git, archivos, materializaciones o sistemas externos?

## Formato para cerrar una pregunta

Al resolver una cuestión:

1. Crear una decisión en [10-registro-de-decisiones.md](10-registro-de-decisiones.md).
2. Incluir alternativas y consecuencias.
3. Actualizar el documento dueño.
4. Añadir ejemplos y contraejemplos.
5. Añadir pruebas de conformidad si ya existe implementación.
6. Marcar aquí la pregunta como cerrada con enlace a la decisión.
