# Modelo del lenguaje

Este documento es dueño del vocabulario semántico de MUD. Resume la estructura conceptual que deberá convertirse en una especificación normativa y una gramática formal.

## Unidades de declaración

MUD tiene nueve declaraciones con nombre y una declaración única de activación inicial:

| Declaración | Representa | Denota identidad o valor dentro del mundo |
| --- | --- | --- |
| `thing` | Cosa, concepto, categoría o especialización | Sí |
| `magnitude` | Cantidad, unidad o punto sobre una cantidad | No como entidad del mundo |
| `rule` | Condición consultable, reacción o invariante | Su declaración tiene ancla; no es un valor ordinario del mundo |
| `action` | Operación externa o composición atómica | Su declaración tiene ancla; no es un valor ordinario del mundo |
| `test` | Escenario aislado que ejecuta efectos y comprueba aserciones | Su declaración tiene ancla; no forma parte del mundo ni de su API |
| `look` | Consulta pública pura del estado estable | Su declaración tiene ancla; su resultado es un valor de salida |
| `message` | Evento público detectado durante una resolución y materializado al estabilizar | Su declaración tiene ancla; cada ocurrencia es una salida |
| `alias` | Tipo nominal de valor simple, estructural o compuesto | La declaración tiene ancla estática; sus valores no tienen identidad runtime |
| `family` | Tipo nominal finito formado por miembros declarados | La declaración tiene ancla estática; sus miembros son valores sin identidad runtime |
| `start with` | Conjunto no ordenado de `thing` y reglas activas al comenzar | No tiene ancla propia ni es un valor del mundo |

Toda declaración con nombre tiene identidad semántica mediante un ancla. El `start with` global es único en el programa y no introduce una identidad adicional; cada test contiene además su propio `start with` local. La última columna distingue la identidad declarativa de las identidades y valores que pueden almacenarse en el mundo. El archivo es una unidad física; el namespace y el tipo de declaración forman parte del ancla.

## Identidad, valor y especialización

MUD no presupone dos dominios separados de clases y objetos. Una `thing` no tiene instancias: las declaradas y las activadas durante la ejecución pertenecen al mismo dominio conceptual, según [[notas/decisiones/ADR-014-ontologia-unificada-de-things|ADR-014]]. Los documentos históricos emplean «constructo» para este mismo concepto.

Toda `thing` concreta denota una cosa con identidad y estado propio, y puede servir a la vez como antecesora de otras. Una `thing` abstracta conserva identidad dentro del mismo dominio, pero no denota directamente una cosa concreta con estado propio.

Hay que conservar tres relaciones distintas:

- Las `thing` se comparan por identidad.
- Los aliases se comparan por tipo nominal y valor.
- `as` declara antecesores directos en la definición canónica de una `thing`.
- `is` consulta especialización nominal no estricta: es reflexiva y transitiva, pero no es igualdad.

Dos `thing` definidas con campos iguales siguen teniendo identidades distintas. Dos valores del mismo alias con el mismo contenido son iguales. Aliases diferentes no son intercambiables aunque su forma normalizada coincida; requieren casting nominal explícito mediante `to`.

Una `family` declara un tipo nominal finito independiente de `thing`. Sus miembros son valores nominales sin estado ni ciclo de vida runtime: no pertenecen a $\mathcal T_P$, no participan en `as` o `is` y no admiten `create` ni `destroy`. Todas las familias se enumeran en orden de declaración; `ordered family` convierte además ese orden en el orden semántico de comparación. Una familia puede declarar directamente un esquema uniforme de datos inmutables antes de sus miembros. Cada miembro puede sustituir valores en un subbloque; los omitidos proceden del predeterminado explícito del dato o del predeterminado de su tipo. Las reglas completas pertenecen a [[notas/decisiones/ADR-038-familias-cerradas-de-valores|D-038]].

Cada `thing` posee una única definición canónica de primer nivel. Puede ser raíz, abstracta o concreta y declarar cero o varios antecesores mediante `as`. `create Nombre` activa esa identidad ya definida: no fabrica una identidad fresca, no añade antecesores y no contiene un cuerpo. Después de `destroy Nombre`, una nueva activación recupera la misma identidad, descriptor y carga almacenada. Las reglas completas pertenecen a [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

La especialización directa es acíclica. Su clausura reflexiva y transitiva, consultada mediante `is`, forma un orden parcial.

El bloque de la definición canónica puede declarar propiedades locales además de las heredadas. Los descendientes heredan declaraciones, restricciones, dominios y valores predeterminados efectivos, pero nunca el estado mutable actual de sus antecesores. Cada `thing` concreta conserva estado independiente. La primera activación resuelve su esquema completo, inicializa desde los predeterminados efectivos y aplica después las inicializaciones explícitas que correspondan.

Esta separación debe existir en el sistema de tipos, el IR, el runtime y los materializadores.

Todo tipo bien formado posee un valor predeterminado perteneciente a su dominio, según [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|ADR-017]]. Por tanto, un campo almacenado sin predeterminado explícito puede inicializarse desde el predeterminado de su tipo. La selección concreta para cada familia de tipos permanece abierta en Q-047.

## Ciclo de vida declarativo

`create` y `destroy` pueden activar y suspender `thing` y las tres clases de reglas. No operan sobre aliases, acciones ni magnitudes. Ambos resuelven únicamente el nombre de una definición canónica de primer nivel:

```mud
thing Dragon {
}

rule FrozenGround on person: Person {
    ...
}

create Dragon
create FrozenGround

destroy Dragon
destroy FrozenGround
```

Una declaración no queda activa por el mero hecho de estar definida. El conjunto inicial se declara una sola vez y sin orden observable:

```mud
start with {
    Dragon,
    FrozenGround
}
```

El `start with` global contiene únicamente referencias separadas por comas, sin coma final. No es una acción ni un bloque de instrucciones y no admite `create`, `destroy` u otros efectos. Si se omite, ninguna `thing` ni regla está explícitamente activa al comienzo ordinario del programa.

El mundo distingue información almacenada y proyección efectiva. `destroy` suspende la estructura de su objetivo y las declaraciones que tengan una dependencia dura de él, pero conserva descriptores y cargas. Una recreación restaura esa información. Por el contrario, `remove field from Thing` elimina la propiedad y su contenido almacenado.

`add` y `remove` se sobrecargan para miembros y propiedades sin introducir la palabra `property`:

```mud
add kingdom: Kingdom[1] = Panama to King
remove kingdom from King

add Panama to King.kingdoms
remove Panama from King.kingdoms
```

Como todas las definiciones son de primer nivel, ninguna declaración puede capturar variables libres de una activación. Puede usar sus propios participantes y `given`, además de anclas globales. La definición completa del ciclo de vida pertenece a [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]] y D-054.

## Aliases nominales

Un alias declara un tipo nominal de valor. Una expresión de tipo se introduce mediante `:=`:

```mud
alias PlayerName :=
    Text

alias Board :=
    Square -> Piece [0..32 ordered]
```

Un alias estructural declara componentes obligatorios, ordenados e inmutables:

```mud
alias Square {
    file: File
    rank: Rank
}
```

Los componentes pueden declarar dominios, pero no `mut`. El valor completo es inmutable; un campo mutable puede sustituirlo, no modificar uno de sus componentes.

Los literales son contextuales. `"Ada"` puede construir directamente un `PlayerName` cuando ese es el tipo esperado, y `(E, Four)` puede construir un `Square`. Una expresión ya tipada no se convierte implícitamente: utiliza `to` si su forma normalizada es compatible. La rama nominal de `to` conserva el contenido y valida el dominio de destino; la cuantitativa continúa definida por D-030.

La forma posicional y la nombrada siguen el orden de declaración. La forma nombrada no permite reordenar y todos los componentes deben aparecer exactamente una vez.

La igualdad exige el mismo alias y el mismo contenido. Los operadores de orden requieren una representación ordenada; para aliases estructurales usan el orden lexicográfico de componentes. Un alias estructural cuyos componentes tengan dominios finitos y enumerables puede recorrerse como su producto cartesiano lexicográfico y puede actuar como clave única compuesta de un diccionario.

Un alias no posee identidad ni ciclo de vida runtime, no participa en especialización y no admite `create` ni `destroy`. Las reglas completas pertenecen a [[notas/decisiones/ADR-031-aliases-nominales-e-inmutables|D-031]], [[notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal|D-032]] y [[notas/decisiones/ADR-033-claves-y-enumeracion-de-aliases|D-033]].

## Estado del mundo

El estado se expresa mediante campos:

- Campo almacenado inmutable: `=`.
- Campo almacenado mutable: `mut` y `=`.
- Campo calculado: `:=`.
- Campo con dominio: `in`.

La forma de un campo almacenado es `[mut] nombre: Tipo [in dominio] [especificación de colección] [= valor]`. El dominio se escribe antes que la especificación de colección. Un campo calculado usa `nombre: Tipo := expresión` y no admite `mut`, dominio ni especificación de colección propios; esas propiedades proceden del tipo estático de la expresión.
- Campo singular, opcional, colección o diccionario mediante cardinalidad.

Todo campo se modela semánticamente como una colección; omitir la cardinalidad equivale a `[1]`. La mutabilidad exterior de una colección y la capacidad de modificar sus miembros son permisos distintos y ortogonales para cualquier cardinalidad:

- `mut field: T [k]` permite cambiar la colección, pero no modificar sus miembros.
- `field: T [k mut]` permite modificar miembros, pero no cambiar la colección.
- `mut field: T [k mut]` concede ambos permisos.

No existe mutabilidad profunda implícita ni excepción para `[1]`. En particular, `mut field: T` equivale a `mut field: T [1]`, no a `field: T [1 mut]`, según [[notas/decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|ADR-019]].

Los campos derivados también pueden producir colecciones, pero su forma se deduce de la expresión. La declaración derivada no vuelve a anotar cardinalidad, orden, unicidad ni capacidad interior.

La sintaxis y las obligaciones de campos almacenados, calculados y dominios pertenecen a [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]]. La semántica común de cardinalidad, `empty`, multiplicidad, orden y diccionarios pertenece a [[notas/decisiones/ADR-039-colecciones-y-diccionarios|D-039]].

Una colección cuyo tipo de miembro sea una `thing` utiliza siempre membresía estricta. `person: Person[1]` puede contener `Alice` si `Alice is Person` y `Alice != Person`, pero nunca el ancla exacta `Person`. No existe un modificador que habilite ese caso. La comparación se realiza con el tipo escrito, no con el propietario de la colección, según [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]].

## Participantes y valores suministrados

La distinción más insistente de la especificación es:

- `on`: vinculaciones construidas automáticamente por el runtime para reglas de cambio, reglas `always` y mensajes.
- `for`: cosas existentes proporcionadas al consultar una regla booleana, solicitar una acción o evaluar un `look`.
- `given`: valores auxiliares proporcionados a una regla booleana o una acción.

Los participantes ocupan roles semánticos. Los `given` no son participantes. En una llamada:

- El receptor identifica participantes.
- Los argumentos identifican valores `given`.

El nombre de cada participante de `on` o `for` puede omitirse. Una referencia no cualificada se resuelve entre los participantes anónimos y los demás nombres visibles solo si existe un candidato compatible único; cualquier ambigüedad es un error estático. Si el cuerpo necesita el participante como valor completo, debe nombrarlo.

Los receptores y los argumentos `given` admiten vinculación posicional. En los argumentos `given`, `nombre = expresión` añade una etiqueta opcional que debe coincidir con el nombre de esa posición: puede mezclarse con argumentos sin etiqueta, pero nunca reordena la llamada. La forma nombrada de un receptor multiparte sí constituye una vinculación por nombre y se rige por reglas distintas.

Consecuencias normativas:

- Las reglas booleanas usan `for` y pueden usar `given`.
- Las acciones usan `for` y pueden usar `given`.
- Los `look` usan `for`, pero no `given`.
- Las reglas reactivas, las reglas `always` y los mensajes usan `on`.
- Las reglas reactivas y `always` no admiten `given`.
- Los mensajes tampoco admiten `given`.
- La palabra `input` no pertenece a la sintaxis MUD.

## Las tres clases de regla

### Regla booleana

Es pura, devuelve `Bool`, se consulta explícitamente y puede tener `given`. No escribe, crea ni destruye.

Cuando su declaración no es efectiva, sus llamadas se eliminan de la expresión mediante una poda estructural. No devuelven simplemente `true` o `false`: el operador exterior conserva el operando restante y una expresión exterior borrada se interpreta como verdadera. Véase [[notas/decisiones/ADR-022-borrado-de-reglas-booleanas-inactivas|D-022]].

### Regla reactiva

Se vincula automáticamente con `on`, observa una transición mediante `when`, puede filtrar con `if` y produce efectos mediante `then`.

### Regla `always`

Se vincula automáticamente con `on`, no tiene efectos y debe ser verdadera en todo estado publicable.

Aunque compartan la palabra `rule`, estas tres formas tienen contratos y ciclos de vida distintos. El AST debería representarlas como variantes explícitas, no como una estructura permisiva con muchos campos opcionales.

El contrato normativo completo de cada variante pertenece a [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]].

## Acciones

Una acción es la API semántica de escritura. Declara:

- Participantes `for`.
- Participantes mutables.
- Valores `given` y sus dominios.
- Precondición `if`.
- Efectos o llamadas atómicas en `then`.
- Poscondición `after`.

Una acción no se activa sola. Se solicita desde el exterior o desde una acción compuesta. Su resultado es `accepted`, `rejected` o `failed`; la semántica de esos resultados pertenece a [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md).

La separación entre acciones elementales y compuestas, la raíz simultánea, `old`, `after`, rollback y resultados pertenecen a [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]].

## Tests

Un `test` declara un escenario cerrado, aislado y reproducible. No es un modificador de `action`, no pertenece a la API pública y usa un ancla `test::*`.

```mud
test CounterIncreases {
    start with {
        Counter
    }

    then Counter.value += 1

    after Counter.value == 1 otherwise "The counter did not increase"
}
```

El `start with` local sustituye completamente al global y solo contiene referencias a definiciones canónicas activables. Después de materializarlas y estabilizar el mundo inicial, `then` forma la transición probada. Las asignaciones escritas en `then` son efectos, no parte del estado inicial.

El `after` del test contiene aserciones booleanas ordenadas. Cada una puede asociar un diagnóstico `Text` mediante `otherwise`. `old` observa el estado estable anterior al `then` completo. La ejecución produce `passed`, `failed` o `error` para el ejecutor de tests y descarta siempre el mundo aislado y sus salidas.

Un test no admite `for`, `given`, `if`, `when` ni participantes. El contrato completo pertenece a [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]].

## Salidas: `look` y `message`

Un `look` es una consulta pública pura sobre un estado estable. Declara participantes mediante `for`, no acepta `given` y publica campos tipados calculados a partir de propiedades o expresiones puras.

Un `message` es un evento público. Declara vinculaciones mediante `on`, exige `when`, admite un `if` opcional y publica campos tipados. El hecho puede detectarse durante una secuencia de ondas, pero los campos se evalúan una vez estabilizada la resolución de la acción causante. Los detalles abiertos de selección, multiplicidad y entrega se registran en [[notas/decisiones/ADR-027-salidas-look-y-message|D-027]].

Junto con las acciones forman la frontera semántica del modelo: `action` introduce cambios; `look` consulta; `message` notifica.

## Forma de las cláusulas

`when`, `if`, `after` y `then` permiten omitir llaves cuando contienen un solo elemento. Las llaves siguen siendo válidas y pueden mejorar la lectura. Un `then` con varias instrucciones debe encerrarlas entre llaves. En acciones y reglas, `when`, `if` y `after` contienen una única expresión booleana, aunque sea compuesta, según [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|D-025]]. El `after` de un test es la excepción explícita: puede contener varias aserciones, por lo que exige llaves cuando hay más de una.

## Tipos y formas de datos

La especificación incluye:

- Tipos básicos no numéricos: `Text`, `Character` y `Bool`.
- Tipos numéricos básicos: `Natural`, `Integer`, `Number`, `Rumber` y `Money`.
- Aliases nominales simples, estructurales y compuestos.
- Familias cerradas de valores declaradas mediante `family` u `ordered family`.
- Cardinalidades y colecciones.
- Diccionarios.
- Intervalos.
- Magnitudes no derivadas, derivadas y de punto.

Los tipos numéricos básicos determinan representación y no son magnitudes. Una magnitud no derivada usa `Number` si omite su tipo numérico; una derivada infiere la representación menos ampliada capaz de representar su operación. `Percentage` no es un tipo básico.

`Number` representa racionales exactos mediante fracciones canónicas de enteros sin límite semántico de tamaño. `Rumber` representa valores aproximados finitos IEEE 754 `binary64`. El primero es la opción general predeterminada; el segundo debe elegirse explícitamente y no expone `NaN`, infinitos ni cero negativo distinguible.

Un literal `Rumber` puro exige el prefijo `r`, incluso bajo un tipo esperado `Rumber`. En una cantidad con unidad de una magnitud basada en `Rumber`, el prefijo es opcional porque la magnitud aporta el contexto. `Number` y `Rumber` no se mezclan en operaciones ni comparaciones sin `to`.

La conversión `Number to Rumber` selecciona el `binary64` más cercano; `Rumber to Number` recupera el racional exacto almacenado. Toda conversión estrecha usa redondeo al más cercano con empates al par. Los intervalos `Rumber` sirven como dominios, pero nunca como fuentes enumerables. Véase [[notas/decisiones/ADR-034-number-exacto-y-rumber-binary64|D-034]].

Las unidades se identifican mediante `name` dentro de un bloque sin identificador de cabecera. Una magnitud no derivada con unidades declara una `root unit`; las alternativas y los nombres derivados se expresan mediante `unit := cantidad`. Una magnitud derivada combina automáticamente las unidades raíz de sus componentes y no puede declarar raíz.

Los literales numéricos no tienen sufijos de tipo. `in` cambia la unidad de presentación de una cantidad. `to` convierte valores cuantitativos compatibles o cambia el tipo nominal de una representación compatible. Los dominios declarados en cabeceras de magnitud usan límites numéricos desnudos interpretados en su representación canónica.

Una magnitud de punto se declara mediante `point over`. Solo estas magnitudes pueden usar el dominio cíclico `[a..b cycle)`. Las decisiones completas pertenecen a [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos|D-029]] y [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]].

Para formalizar esta parte se necesita una matriz por operador que indique:

1. Tipos aceptados.
2. Tipo resultante.
3. Conversión implícita permitida.
4. Posibles errores.
5. Normalización.
6. Comportamiento en compilación y runtime.

La lista textual actual es una base, pero todavía no constituye un sistema de tipos completo.

## Dominios

`in` puede declarar un conjunto válido para campos, componentes de alias y valores `given`.

El mismo token también expresa pertenencia, vinculación estructural y conversión de unidad. El parser puede distinguir los contextos, pero la especificación debe definirlos como construcciones semánticas separadas.

Un dominio puede ser estático o calculado. Los dominios calculados introducen dependencias y posibles ciclos; por eso requieren análisis específico.

## Namespaces, `using` y anclas

El namespace se deriva de la ruta. Las declaraciones `using` pueden ser exactas o recursivas. La resolución da prioridad a símbolos locales, mismo namespace, declaraciones `using` y nombres cualificados.

Formato conceptual de anclas:

```text
thing::warfare.armies.Army
thing::warfare.armies.Army::morale
family::warfare.armies.Severity
rule::warfare.armies.IsDestroyed
action::warfare.armies.Recruit
test::warfare.armies.RecruitIncreasesArmy
look::warfare.armies.ArmySummary
message::warfare.armies.ArmyDestroyed
```

Las anclas no incluyen el archivo. Mover una declaración dentro del mismo namespace no cambia su identidad; moverla de namespace sí, salvo una migración explícita todavía por diseñar.

MUD distingue palabras reservadas y contextuales. `using`, `with`, `family`, `test`, `otherwise` y `ordered` están reservadas. `start` introduce `start with`; `abstract` solo actúa como modificador delante de `thing`; `always` solo actúa como variante delante de `rule`; y etiquetas como `name` o `prefixes` se reconocen dentro de la declaración que las define. Las palabras contextuales pueden usarse como identificadores ordinarios fuera de su posición especial; `ordered` no puede.

Las reglas completas de organización física, declaraciones `using`, resolución, nombres y formación de anclas pertenecen a [[notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas|D-035]]. La semántica de participantes, receptores posicionales o nombrados y argumentos `given` pertenece a [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|D-036]].

## Pureza y efectos

Las expresiones usadas en reglas booleanas, dominios, condiciones y filtros deben ser puras. Los efectos están limitados a construcciones declaradas:

- Asignaciones.
- Operaciones de colección.
- Creación y destrucción.
- Composición de acciones.

No hay escape a código de implementación, funciones generales con efectos, bucles no acotados ni recursión general expuesta.

## Trabajo normativo pendiente

Antes de llamar estable al lenguaje hacen falta, al menos:

- Gramática léxica y sintáctica completa.
- AST canónico con invariantes por nodo.
- Reglas de nombres y resolución.
- Sistema de tipos y conversiones.
- Catálogo formal de efectos.
- Reglas de estática para pureza, mutabilidad y dominios.
- Especificación de diagnósticos.
- Ejemplos válidos e inválidos ejecutables.
