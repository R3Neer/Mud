---
id: D-096
title: "Módulos, callables, `look`, `message` y activación"
status: vigente
date: 2026-08-28
supersedes:
  - "D-027"
superseded-by: []
questions:
  - "Q-051"
  - "Q-052"
  - "Q-062"
  - "Q-063"
  - "Q-064"
  - "Q-065"
  - "Q-066"
  - "Q-067"
  - "Q-068"
affects:
  - "módulos, visibilidad y reflexión"
  - "actions, subactions y `then`"
  - "`look`, `message` y triggers"
  - "dominios, `all` y selección"
  - "activación inicial y tests"
  - "gramática, CST, AST, IR, tipado, resolución y frontera host"
---

# ADR-096 — Módulos, callables, `look`, `message` y activación

- Sustituye: [[ADR-027-salidas-look-y-message|D-027]].
- Modifica: [[ADR-036-participantes-receptores-y-llamadas|D-036]], [[ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[ADR-042-acciones-raiz-y-resultados|D-042]], [[ADR-045-resolucion-causal-vinculaciones-y-cola|D-045]], [[ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]], [[ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]], [[ADR-075-dominios-enumerables-all-y-valores-derivados|D-075]], [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]], [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]], [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]] y [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]].
- Preguntas abiertas asociadas: Q-062 a Q-068.

- Modificada por: [[ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].

## Contexto

La evolución de MUD había dejado varias fronteras artificialmente separadas: actions elementales frente a compuestas, `look` como consulta esencialmente exterior, `message` como salida diferida al host, activación separada en `things` y `rules` y consumo implícito de dominios en operaciones que producen colecciones. Estas separaciones interactúan mal cuando el lenguaje se organiza en módulos, permite valores callable y usa una resolución causal por ondas.

Esta decisión unifica esas piezas sin cerrar las cuestiones de tipado callable, identidad de tipos anónimos ni gramática completa de `mud.module` que siguen abiertas.

## Decisión

### Un único modelo de `then`

Se elimina la separación semántica entre actions elementales y compuestas. Un `then` es una secuencia ordenada de consecuencias y puede mezclar vinculaciones locales, efectos directos, llamadas a `action` o `subaction` y recorridos `for each`.

Una llamada interna se ejecuta en su posición textual dentro del delta privado de la resolución: observa los efectos anteriores visibles en ese punto, aporta sus efectos a la misma resolución y las sentencias posteriores observan esos efectos. No abre una transacción independiente.

Los `after` de todas las actions/subactions ejecutadas durante la resolución se comprueban contra el estado estable tentativo final de la resolución completa. Un `for each` ordenado conserva semántica secuencial entre iteraciones; en uno no ordenado los deltas de iteraciones hermanas se consolidan con las reglas ordinarias de concurrencia.

Una `action` o `subaction` puede invocarse desde cualquier contexto semántico `then`, incluido el `then` de una rule reactiva. `action` conserva además capacidad de raíz exterior; `subaction` no. Un `failed` anidado propaga y revierte toda la resolución. Un `rejected` interno también aborta y revierte, pero conserva la categoría `rejected`.

### Módulos y visibilidad

La visibilidad se deriva de la categoría semántica, el módulo propietario, los contratos entre módulos y el cierre de tipos requerido por esos contratos.

Un módulo es una unidad de encapsulación semántica. Entre módulos, la frontera operacional visible se compone de `action`, `look`, `message` y, solo en contexto de tests, `test`. La frontera de aplicación hacia el host incluye `action`, `look` y `message`, no `test`.

Las declaraciones internas de implementación no se vuelven visibles por defecto. Un módulo puede usar sus propias operaciones con las mismas capacidades semánticas que concede a otros módulos en el contexto correspondiente.

La pertenencia a módulo no forma parte del ancla nominal. Anclas como `thing::infrastructure.economy.Bank` o `action::infrastructure.economy.Transfer` conservan su forma; el módulo es una dimensión adicional de visibilidad y dependencia.

La raíz física de un módulo se marca con un archivo visible `mud.module`. Cada `.mud` pertenece al módulo del `mud.module` ancestro más cercano; un `.mud` sin ancestro modular es inválido y un `mud.module` anidado abre una nueva frontera. El nombre lógico del módulo se deriva del MudPath del directorio.

`mud.module` declara dependencias exteriores mediante `uses`. `uses` autoriza que el módulo conozca el contrato de otro módulo; `using` conserva dentro de un `.mud` su función de resolución/importación de nombres y no concede permiso modular por sí solo. Las dependencias modulares pueden formar ciclos: el compilador debe advertir sobre el acoplamiento cíclico, no inventar un orden de inicialización.

La gramática completa del archivo `mud.module` queda abierta en Q-062; esta decisión fija su papel semántico, el nombre físico y la responsabilidad de `uses`, pero no inventa una superficie adicional.

### Cierre de tipos y reflexión entre módulos

Un contrato visible debe ser cerrado respecto de los tipos necesarios para comprenderlo y usarlo. El cierre incluye, cuando corresponda, tipos de `for` y `given`, participantes `on`, resultados de `look`, payloads de `message` y tipos transitivamente necesarios dentro de aliases, families, magnitudes, colecciones, diccionarios y productos expuestos.

Una `thing` visible por contrato expone la identidad/tipo nominal necesaria para vincular valores, no sus campos ordinarios. La lectura pública de estado se expresa mediante `look`. Un `alias`, `family` o `magnitude` visible expone la estructura necesaria para representar sus valores.

La reflexión dentro del propio módulo puede observar el modelo conforme al sistema general de descriptores. Al cruzar una frontera, una operación reflectiva solo es válida cuando su contrato garantiza que no puede devolver entidades invisibles. No se filtran silenciosamente resultados de `~fields`, `~children`, `~descendants` ni propiedades semejantes para simular seguridad.

La especialización/herencia de `thing` no puede cruzar una frontera de módulo.

### Activación por módulo

Cada módulo puede contribuir como máximo un `start with`. No es `main`, no llama módulos y no establece orden de inicialización. Las contribuciones de todos los módulos se combinan y se materializan conjuntamente antes de la estabilización inicial.

El `start with` de un módulo solo puede activar declaraciones con ciclo de vida del mismo módulo. Se elimina la separación obligatoria entre secciones `things` y `rules`: el conjunto conceptual reúne declaraciones activables `thing | rule`, es no ordenado y deduplicado y no se interpreta como un `for each create`.

Se aceptan una contribución directa y un bloque de contribuciones:

```mud
start with Kingdom
```

```mud
start with {
    Kingdom,
    Place,
    CanEnter
}
```

Cada expresión puede aportar cero, una o varias declaraciones activables. Las identidades repetidas se deduplican y el orden no tiene significado semántico.

Los tests respetan la frontera de módulo. En contexto de pruebas pueden llamar desde `then` a tests públicos de otros módulos autorizados por `uses`. Antes de ejecutar el test raíz se calcula el cierre transitivo estático de tests alcanzables y se unen sus contribuciones `start with`; una llamada posterior a un test ya incluido no vuelve a ejecutar su activación inicial. Un ciclo ejecutable de llamadas entre tests es inválido.

### Dominios, `all` y selección

Además del literal contextual `all`, se acepta `all D` para materializar la enumeración canónica completa de un dominio enumerable `D`. `all` sin operando conserva su dominio contextual.

`all D` exige enumeración válida y finita cuando el contexto requiere materialización exhaustiva. También se aplica a dominios reflectivos visibles, por ejemplo `all action`, `all rule`, `all look` o `all A.action(B)`. `all thing` enumera descriptores `thing` visibles; `all Thing` conserva el significado del dominio del tipo incorporado `Thing`.

Las construcciones que recorren o cuantifican un dominio sin producir una colección pueden consumirlo directamente. Cuando una operación produce una colección a partir de un dominio, la materialización debe ser explícita mediante `all D`. Esto incluye selección y `take`, por ejemplo `take n from all D`.

Los usos vigentes de `in` permanecen separados: `x in D` restringe localmente un valor al dominio `D`; `a: A in D` es una restricción declarativa de dominio; `x in source: predicate` es selección y produce una colección. La pertenencia booleana se expresa mediante `D has x` o `D has not x`. No se introduce una conversión implícita de una colección filtrada a `Domain` ni un dominio refinado por predicado.

### Descriptores, `Any`, `is` y `~type`

Los descriptores son valores first-class y pueden formar parte de `Any`. `Any` es un verdadero tipo superior de los valores MUD, no una unión textual de todos los tipos del programa.

`is` puede refinar un valor general hacia un descriptor compatible, incluidos tipos nominales y tipos callable como `Dragon.look(Detail)`. `e~type` devuelve el tipo estático actual de `e` en el punto del programa, después del narrowing demostrado por el análisis de flujo. El resultado es determinable durante elaboración y puede usarse en posición de tipo.

Una expresión que ya denota un `Type`, como `Dragon.look(Detail)`, no necesita `~type` para convertirse en tipo.


Las formas callable de superficie fijadas por esta decisión son `A.action(B...)`, `(A, C).action(B...)`, `A.rule(B...)` y `A.look(B...)`: la parte izquierda describe los tipos de receptor/participantes y los paréntesis la parte `given` de la firma. `subaction <: action` sigue siendo una relación semántica de descriptores y no introduce por sí sola una grafía de tipo `A.subaction(...)`. Q-063 mantiene abiertas la varianza y compatibilidad formal entre tipos callable.
Se acepta la relación reflectiva `subaction <: action <: Declaration`, pero la capacidad de raíz exterior es independiente del subtyping. Un valor ampliado a `action` no puede cruzar la frontera exterior si alguna alternativa runtime posible sigue siendo `subaction`; el narrowing puede demostrar que la capacidad exterior es segura. La varianza y compatibilidad formal de callables queda abierta en Q-063.

### Invocación dinámica de valores callable

Un descriptor callable almacenado se invoca mediante la misma forma de receptor que una declaración nominal, sin sintaxis especial `.(op)`:

```mud
op := someAction
then dragon.op(volume)
```

```mud
predicate := someRule
allowed := dragon.predicate(limit)
```

Con varios participantes puede escribirse `(attacker, defender).op(amount)`. Almacenar el descriptor no pre-vincula receptores ni `given`; la invocación realiza esas vinculaciones en el punto de llamada.

La regla exacta para binding nominal al invocar un descriptor suficientemente borrado queda abierta en Q-066.

### `look` como callable puro

`look` es una consulta pura callable desde el host, desde otro módulo que vea su contrato, desde su propio módulo y desde contextos runtime puros compatibles con lectura de estado. Admite `for` y `given`.

Los `given` de `look` siguen las reglas generales de `given`. Una violación dinámica de dominio desde el host es error de consulta; dentro de una resolución, si invalida la evaluación, produce `failed`. Los `given` no deben introducir preocupaciones puramente de transporte o presentación del host.

Los campos de un `look` se evalúan sobre una única vista de lectura coherente heredada del llamador. Desde el host es el estado estable consultable; desde una rule es la instantánea de esa rule; desde un `then` incluye el delta privado visible en el punto textual de la llamada. Un `look` puede por ello observar efectos privados anteriores del mismo `then` sin dejar de ser puro.

Cada `look` induce un objeto resultado anónimo formado por sus campos públicos. Una llamada devuelve exactamente un valor de ese tipo; la multiplicidad se expresa mediante campos ordinarios. El tipo anónimo no recibe ancla por existir. Puede obtenerse con `~type` y usarse para definir un alias ordinario.

Una llamada `MyDragon.Stats()` es valor y no puede ocupar directamente una posición de tipo; `MyDragon.Stats()~type` sí denota su tipo estático. En cambio `Dragon.look(Detail)` ya es un tipo callable.

Si una llamada dinámica puede seleccionar varios `look` con resultados distintos, el tipo de resultado debe ser el común más específico que cubra todas las alternativas. Cuando no existe un supertipo común más informativo que conservar explícitamente esas alternativas, el resultado es su unión. La elección formal cuando existen varios mínimos comunes incomparables queda abierta en Q-065; la identidad/igualdad de tipos anónimos queda abierta en Q-068.

### `message` como ocurrencia causal

Un `message` no se llama para producir un valor. Ocurre como consecuencia de su `when` durante una resolución causal. Cada ocurrencia conserva la declaración, sus bindings `on`, la vista/onda causal y una identidad técnica que preserva multiplicidad. El payload es un tipo anónimo formado por los campos públicos.

El `when` de una rule reactiva y el de un `message` comparten el mismo lenguaje de triggers. Además de activadores temporales, pueden observarse ocurrencias/disparos de declaraciones visibles compatibles: un `message` ocurrido, una rule reactiva que ha disparado y una rule `always` evaluada para una vinculación. Actions, subactions, looks, reglas booleanas y tests no son fuentes de trigger.

Las declaraciones gobernadas por `on` no admiten `given`; al referenciarlas como trigger no llevan `()`. `when Damaged`, `when Dragon.Damaged` o una local previa como `damage := Dragon.Damaged` seguida de `when damage` son formas válidas. Los receptores de una referencia restringen bindings `on`; no convierten el trigger en llamada ordinaria.

Una rule reactiva usada como trigger pulsa cuando ha disparado efectivamente. Una `always` usada como trigger pulsa en cada onda en la que se evalúa para la vinculación correspondiente; observarla no invierte su significado ni la convierte en trigger de fallo. El tooling debe advertir del riesgo de causalidad inútil o falta de estabilización.

Un trigger produce cero o más matches, no necesariamente un `Bool`. Cada match conserva bindings/testigos y la identidad de las ocurrencias causales. `and` realiza natural join de matches compatibles, o producto cartesiano cuando no comparten bindings; `or` realiza unión. Ocurrencias causalmente distintas no se deduplican por tener el mismo payload y no existe desigualdad implícita entre bindings.

Una ocurrencia nacida en la onda `n` queda disponible como consecuencia causal para la onda siguiente; no ejecuta consumidores inmediatamente por orden físico. La estabilización exige una onda sin efectos ni nuevas consecuencias/ocurrencias pendientes. Un ciclo puramente causal de messages o disparos puede impedir estabilización aunque el estado del mundo no cambie.

El `when` y el `if` del `message` se resuelven en la vista causal que produce la ocurrencia. Si `if` es falso, la ocurrencia no nace. Dentro de MUD, el payload observado se proyecta sobre la vista causal de la ocurrencia. Hacia el host, si la resolución confirma, se proyecta sobre el estado estable final. Ambas proyecciones pertenecen a la misma ocurrencia; si la resolución revierte, no hay entrega exterior.

El tratamiento exterior de participantes que dejan de existir antes del estado final queda abierto en Q-067.


La envoltura exterior de una ocurrencia confirmada conserva separados los bindings `on` y el payload público; no se aplana un único objeto en el que los nombres de participantes compitan con los nombres de payload. La entrega conserva el orden causal entre ondas. Dentro de una misma onda se usa un orden técnico estable y reproducible, sin atribuir a ese orden prioridad semántica entre ocurrencias.
### Locales previas a cláusulas de comportamiento

Una `action`, una rule reactiva o un `message` puede declarar locales puras mediante `:=` entre los metadatos y sus cláusulas principales. Son inmutables, secuenciales, visibles para locales posteriores y cláusulas posteriores y respetan las reglas ordinarias contra referencias adelantadas, ciclos y sombreado.

Una local puede nombrar un trigger antes de `when`; no selecciona una ocurrencia concreta hasta que el `when` produce un match. Los campos de payload solo son accesibles donde el análisis de flujo garantiza que el binding existe.

### Frontera host centrada en operaciones

La API anfitriona canónica se organiza alrededor de la identidad de las operaciones públicas, no alrededor de un participante elegido como propietario. La frontera de producción comprende `action`, `look` y `message`. Los tests pueden ser públicos entre módulos en contexto de pruebas, pero no forman por ello parte de la API exterior de producción.

## Restricciones adicionales

- La frontera modular no se controla mediante modificadores explícitos de visibilidad.
- La reflexión cruzada debe ser segura por contrato; no se censuran resultados silenciosamente.
- Una `thing` no puede especializar una `thing` de otro módulo.
- Una llamada action/subaction interna nunca abre una resolución raíz nueva.
- Un `look` sigue siendo puro incluso si lee el delta privado visible del llamador.
- Un `message` no se emite mediante `emit` ni se modela como valor `Bool`.
- Las ocurrencias de `message` no se convierten en participantes `on`; la causalidad pertenece a `when`.
- Actions, subactions, looks, reglas booleanas y tests no son fuentes declarativas de trigger.
- Una selección que produce colección desde un dominio debe usar una fuente materializada explícitamente con `all D`.

## Cuestiones abiertas

- Q-062: gramática completa de `mud.module`.
- Q-063: compatibilidad y varianza formal de tipos callable.
- Q-064: aliases y especialización nominal a través de módulos.
- Q-065: join de tipos de resultado de `look` con múltiples mínimos comunes.
- Q-066: binding nominal al invocar un descriptor borrado.
- Q-067: participantes de `message` inexistentes al estado final.
- Q-068: identidad e igualdad estructural de tipos anónimos.

Estas cuestiones no autorizan a elegir silenciosamente una variante durante implementación.
