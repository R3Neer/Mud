# Modelo del lenguaje

Este documento es dueño del vocabulario semántico de MUD. Resume la estructura conceptual que deberá convertirse en una especificación normativa y una gramática formal.

## Unidades de declaración

MUD tiene cuatro declaraciones principales y una auxiliar:

| Declaración | Representa | Denota identidad o valor dentro del mundo |
| --- | --- | --- |
| `construct` | Cosa, concepto, categoría, especialización o familia cerrada | Sí |
| `magnitude` | Cantidad, unidad o punto sobre una cantidad | No como entidad del mundo |
| `rule` | Condición consultable, reacción o invariante | Su declaración tiene ancla; no es un valor ordinario del mundo |
| `action` | Operación externa o composición atómica | Su declaración tiene ancla; no es un valor ordinario del mundo |
| `alias` | Valor estructural nominal o nombre de tipo | La declaración tiene ancla; sus valores no tienen identidad |

Toda declaración tiene identidad semántica mediante un ancla. La última columna distingue esa identidad declarativa de las identidades y valores que pueden almacenarse en el mundo. El archivo es una unidad física; el namespace y el tipo de declaración forman parte del ancla.

## Identidad, valor y especialización

MUD no presupone dos dominios separados de clases y objetos. Un constructo no tiene instancias: los constructos declarados y los creados durante la ejecución pertenecen al mismo dominio conceptual, según [[notas/decisiones/ADR-014-ontologia-unificada-de-constructos|ADR-014]].

Todo constructo concreto denota una cosa con identidad y estado propio, y puede servir a la vez como antecesor de otros constructos. Un constructo abstracto conserva identidad dentro del mismo dominio, pero no denota directamente una cosa concreta con estado propio.

Hay que conservar tres relaciones distintas:

- Los constructos se comparan por identidad.
- Los aliases se comparan por valor estructural.
- `from` declara antecesores directos en cabeceras estáticas y dinámicas.
- `is` consulta especialización nominal no estricta: es reflexiva y transitiva, pero no es igualdad.

Dos constructos creados durante la ejecución con campos iguales siguen teniendo identidades distintas. Dos valores del mismo alias con los mismos componentes son iguales. Aliases diferentes no son intercambiables aunque su forma coincida.

`create` puede activar un constructo raíz, abstracto o concreto y relacionarlo con cero o varios antecesores mediante `from`, según [[notas/decisiones/ADR-016-creacion-generalizada-de-constructos|ADR-016]]. El nombre introducido es una identidad global reservada, no una variable local ni una identidad fresca por ejecución. Si está ausente, se activa; después de destruirlo, una nueva creación reactiva la misma identidad. Cada antecesor añade la misma relación directa que una declaración estática con `from`, según [[notas/decisiones/ADR-018-from-declara-is-consulta|ADR-018]]. El origen y el ciclo de vida no forman una segunda categoría ontológica.

La especialización directa es acíclica. Su clausura reflexiva y transitiva, consultada mediante `is`, forma un orden parcial.

El bloque de `create` es un cuerpo declarativo completo: puede añadir propiedades locales además de las heredadas. Los descendientes heredan declaraciones, restricciones, dominios y valores predeterminados efectivos, pero nunca el estado mutable actual de sus antecesores. Cada constructo concreto conserva estado independiente. Un `create` concreto resuelve su esquema completo, inicializa desde los predeterminados efectivos y aplica después las inicializaciones explícitas que correspondan.

Esta separación debe existir en el sistema de tipos, el IR, el runtime y los materializadores.

Todo tipo bien formado posee un valor predeterminado perteneciente a su dominio, según [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|ADR-017]]. Por tanto, un campo almacenado sin predeterminado explícito puede inicializarse desde el predeterminado de su tipo. La selección concreta para cada familia de tipos permanece abierta en Q-047.

## Ciclo de vida declarativo

`create` y `destroy` también pueden activar y suspender aliases y las tres clases de reglas. No operan sobre acciones ni magnitudes. `create` explicita la clase de declaración; `destroy` resuelve únicamente el nombre:

```mud
create construct Dragon {
}

create alias Coordinate {
    x: Integer
    y: Integer
}

create rule FrozenGround for person: Person {
    ...
}

destroy Dragon
destroy Coordinate
destroy FrozenGround
```

El mundo distingue información almacenada y proyección efectiva. `destroy` suspende la estructura de su objetivo y las declaraciones que tengan una dependencia dura de él, pero conserva descriptores y cargas. Una recreación restaura esa información. Por el contrario, `remove field from Construct` elimina la propiedad y su contenido almacenado.

`add` y `remove` se sobrecargan para miembros y propiedades sin introducir la palabra `property`:

```mud
add kingdom: Kingdom[1] = Panama to King
remove kingdom from King

add Panama to King.kingdoms
remove Panama from King.kingdoms
```

Las declaraciones creadas no capturan variables libres de su contexto creador. Pueden usar sus propios participantes y `given`, además de anclas globales. La definición completa pertenece a [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]].

## Estado del mundo

El estado se expresa mediante campos:

- Campo almacenado inmutable: `=`.
- Campo almacenado mutable: `mut` y `=`.
- Campo calculado: `:=`.
- Campo con dominio: `in`.
- Campo singular, opcional, colección o diccionario mediante cardinalidad.

Todo campo se modela semánticamente como una colección; omitir la cardinalidad equivale a `[1]`. La mutabilidad exterior de una colección y la capacidad de modificar sus miembros son permisos distintos y ortogonales para cualquier cardinalidad:

- `mut field: T [k]` permite cambiar la colección, pero no modificar sus miembros.
- `field: T [k mut]` permite modificar miembros, pero no cambiar la colección.
- `mut field: T [k mut]` concede ambos permisos.

No existe mutabilidad profunda implícita ni excepción para `[1]`. En particular, `mut field: T` equivale a `mut field: T [1]`, no a `field: T [1 mut]`, según [[notas/decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|ADR-019]].

Los campos derivados también producen colecciones. Su pertenencia se calcula y no admite mutabilidad exterior; la capacidad interior, cuando se declare, solo permite modificar los miembros alcanzados.

Una colección cuyo tipo de miembro sea un constructo utiliza membresía estricta por defecto. `person: Person[1]` puede contener un constructo `Alice` que satisfaga `Alice is Person`, pero no el ancla exacta `Person`. El modificador `[reflexive]` habilita ese caso exacto. No significa que el propietario del campo pueda o no almacenarse a sí mismo, según [[notas/decisiones/ADR-020-membresia-estricta-y-reflexive|ADR-020]].

## Participantes y valores suministrados

La distinción más insistente de la especificación es:

- `on`: cosas existentes proporcionadas al consultar una regla o solicitar una acción.
- `for`: vinculaciones construidas automáticamente por el runtime para reglas reactivas e invariantes.
- `given`: valores proporcionados a una regla consultable o una acción.

Los participantes ocupan roles semánticos. Los `given` no son participantes. En una llamada:

- El receptor identifica participantes.
- Los argumentos identifican valores `given`.

Consecuencias normativas:

- Las reglas booleanas usan `on`.
- Las acciones usan `on`.
- Las reglas reactivas y `always` usan `for`.
- Las reglas reactivas y `always` no admiten `given`.
- Las acciones no usan `for`.
- La palabra `input` no pertenece a la sintaxis MUD.

## Las tres clases de regla

### Regla booleana

Es pura, devuelve `Boolean`, se consulta explícitamente y puede tener `given`. No escribe, crea ni destruye.

Cuando su declaración no es efectiva, sus llamadas se eliminan de la expresión mediante una poda estructural. No devuelven simplemente `true` o `false`: el operador exterior conserva el operando restante y una expresión exterior borrada se interpreta como verdadera. Véase [[notas/decisiones/ADR-022-borrado-de-reglas-booleanas-inactivas|D-022]].

### Regla reactiva

Se vincula automáticamente con `for`, observa una transición mediante `when`, puede filtrar con `if` y produce efectos mediante `then`.

### Regla `always`

Se vincula automáticamente con `for`, no tiene efectos y debe ser verdadera en todo estado publicable.

Aunque compartan la palabra `rule`, estas tres formas tienen contratos y ciclos de vida distintos. El AST debería representarlas como variantes explícitas, no como una estructura permisiva con muchos campos opcionales.

## Acciones

Una acción es la API semántica de escritura. Declara:

- Participantes `on`.
- Participantes mutables.
- Valores `given` y sus dominios.
- Precondición `if`.
- Efectos o llamadas atómicas en `then`.
- Poscondición `after`.

Una acción no se activa sola. Se solicita desde el exterior o desde una acción compuesta. Su resultado es `accepted`, `rejected` o `failed`; la semántica de esos resultados pertenece a [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md).

## Tipos y formas de datos

La especificación incluye:

- `Boolean`, `Natural`, `Integer`, `Number`, `Text`, `Money` y `Percentage`.
- Aliases estructurales.
- Familias cerradas de valores.
- Cardinalidades y colecciones.
- Diccionarios.
- Intervalos.
- Magnitudes lineales, unidades y magnitudes de punto.

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

## Namespaces, imports y anclas

El namespace se deriva de la ruta. Los imports pueden ser exactos o recursivos. La resolución da prioridad a símbolos locales, mismo namespace, imports y nombres cualificados.

Formato conceptual de anclas:

```text
construct::warfare.armies.Army
construct::warfare.armies.Army::morale
rule::warfare.armies.IsDestroyed
action::warfare.armies.Recruit
```

Las anclas no incluyen el archivo. Mover una declaración dentro del mismo namespace no cambia su identidad; moverla de namespace sí, salvo una migración explícita todavía por diseñar.

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
