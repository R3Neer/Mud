---
id: D-101
title: "Bloques de valor, variables locales almacenadas y extremos por testigos"
status: current
date: 2026-08-29
supersedes: []
superseded-by: []
questions: []
affects:
  - "ExpressionBlock, ValueBlock, EffectBlock, variables locales, for each, fields, aliases, family, diccionarios, metadata, participantes, min, max, gramática, CST, AST, resolución y consolidación"
---
# ADR-101 — Bloques de valor, variables locales almacenadas y extremos por testigos

- Modifica: [[ADR-036-participants-recipients-and-calls|D-036]], [[ADR-037-fields-and-declarative-domains|D-037]], [[ADR-038-close-knit-families-with-strong-values|D-038]], [[ADR-047-quantifiers-and-finite-iteration|D-047]], [[ADR-066-static-values-and-local-bindings-in-then|D-066]], [[ADR-071-local-bindings-in-boolean-blocks|D-071]], [[ADR-085-diccionarios-funcionales-metadatos-and-activacion-estructurada|D-085]], [[ADR-087-metadatos-reflectivos-descriptores-estables-and-visibilidad-exterior|D-087]], [[ADR-088-iteracion-progresiones-firmadas-and-bloques-de-expresion|D-088]], [[ADR-095-extremos-vacios-como-ausencia-ordinaria|D-095]], [[ADR-096-modulos-callables-look-message-and-activacion|D-096]] y [[ADR-100-orden-logico-procedencia-pertenencia-and-consolidacion-de-efectos|D-100]].
- Conserva el default de `given` como expresión estática cerrada conforme a D-063 y D-066.

## Contexto

MUD ya distinguía bloques declarativos de expresión y bloques ejecutables de efectos, pero esa división dejaba sin una forma propia la construcción de un valor mediante almacenamiento temporal local. Tampoco permitía variables locales almacenadas en `then`, obligaba a modelar todos los `for each` como efectos y mantenía `sum`, `min` y `max` con una familia de agregación demasiado heterogénea.

La ampliación debe conservar dos fronteras deliberadas del lenguaje: un cálculo de valor no puede adquirir efectos observables y `if` no se convierte en una sentencia general dentro de bloques de cálculo.

## Decisión

### Tres contratos de cuerpo

`ExpressionBlock` contiene cero o más locales calculadas puras `:=` y exactamente una expresión final. No admite variables almacenadas, mutación, `for each` como sentencia ni `if` interior.

`ValueBlock` construye exactamente un valor mediante cero o más `ValueStatement` y una expresión final. Su catálogo de sentencias queda cerrado a:

1. declaración calculada local;
2. declaración almacenada local, mutable o inmutable;
3. mutación local;
4. `LocalForEach`.

`EffectBlock` ejecuta consecuencias observables. Admite las declaraciones locales calculadas y almacenadas anteriores, además de efectos ordinarios. Un `then` sigue siendo inválido si no contiene al menos un efecto observable o llamada ejecutable.

Los bloques no son expresiones primarias generales. Solo aparecen en slots propietarios explícitos. Argumentos, índices, elementos de literales, RHS ordinarios de efectos y demás posiciones `expression` no adquieren bloques inline.

### Pureza exterior de `ValueBlock`

Un `ValueBlock` puede modificar únicamente almacenamiento creado dentro de su propia frontera. La comprobación usa el footprint final del destino, no solo el identificador inicial: una local que conduzca a estado exterior no autoriza a escribir ese estado.

No admite efectos sobre el mundo, `create`, `destroy` ni llamadas a actions/subactions como efectos. Una variable local declarada en un ámbito envolvente del mismo `ValueBlock` sí puede ser modificada desde un `LocalForEach` interior.

No existe sentencia `if` dentro de `ExpressionBlock`, `ValueBlock` ni `LocalStatementBlock`. Elección de valores, filtrado, extremos, ausencia y narrowing continúan expresándose con las construcciones declarativas de MUD.

### Variables locales almacenadas

Además de `x := value-body` se admiten:

```mud
x: X = value-body
mut x: X = value-body
```

`:=` no crea un lugar asignable. `x: X =` crea un slot local almacenado no reasignable y `mut x: X =` uno reasignable. El inicializador local se evalúa al alcanzar la declaración y puede leer estado runtime cuando el contexto lo permita.

Las variables almacenadas admiten la forma completa del tipo/valor compatible con su propietario. La mutabilidad del slot y la capacidad interior de su valor son ortogonales.

Una local calculada puede ser `given` o participante `for` readonly. Una local almacenada inmutable puede ser `given` o `for` readonly. Una local almacenada mutable puede además satisfacer `for mut`. La llamada vincula temporalmente el participante al slot; no introduce references de primera clase ni copy-in/copy-out, y un fallo revierte también las modificaciones de ese slot conforme a la atomicidad ordinaria.

### `for each` local

Dentro de `ValueBlock`, `for each` usa `LocalStatementBlock`, que contiene únicamente `ValueStatement` y no posee expresión final propia. Su filtro sigue siendo un `ExpressionBlock` booleano.

En una iteración con orden semántico, una mutable exterior al bucle pero interior al cuerpo propietario se observa secuencialmente entre iteraciones. En una iteración sin orden semántico, todas las iteraciones parten de la misma proyección previa y sus modificaciones sobre una mutable exterior se consolidan como concurrentes. Un conjunto de `+=` compatibles usa la consolidación aritmética general; varias asignaciones absolutas `=` no adquieren por ello semántica de acumulador.

Cada iteración mantiene su ámbito local independiente.

### Propietarios de `ExpressionBlock`

Usan `ExpressionBlock`: reglas booleanas, `always`, `when`, guardas `if`, `after` de action, filtros de `for each`, selección, `exists`, `forall`, `count`, `min`, `max`, claves de diccionario exacto y selectores de diccionario funcional. Los selectores funcionales y los cuerpos de los cinco cuantificadores indicados elaboran a `Bool`, salvo los contratos temporalmente distintos ya fijados para `when`.

### Extremos por testigos

`min` y `max` usan un `ExpressionBlock` como predicado booleano. Entre los testigos aceptados, `min` devuelve el primero y `max` el último según el orden semántico de la fuente. Una fuente `ordered`, incluso sin clave explícita, proporciona orden suficiente. Una fuente sin orden semántico utilizable es inválida. Ningún candidato aceptado produce `empty` con la cardinalidad parcial ordinaria de los extremos.

`by` conserva exclusivamente su significado de progresión cuando la fuente lo admite; `min` y `max` no introducen un criterio de orden propio.

### Propietarios de `ValueBlock`

Pueden usar una forma breve o `ValueBlock`: locales calculadas y almacenadas; campos almacenados, calculados y públicos; inicializadores heredados de `thing`; datos almacenados/calculados de `family`; asignaciones de datos de miembros; defaults y overrides de componentes de alias; campos calculados de alias; valores de diccionario exacto; resultados de diccionario funcional; metadata almacenada o calculada.

Las restricciones del propietario siguen vigentes. Cuando un campo, componente, dato, asignación de miembro u otro slot exige inicialización estática, todo su `ValueBlock` debe poder evaluarse estáticamente. El default de `given` es una excepción deliberada: continúa siendo `constant-expression` y no admite `ValueBlock`.

### Diccionarios

Una asociación exacta tiene `ExpressionBlock` a la izquierda y `ValueBlock` a la derecha. Una rama funcional tiene `ExpressionBlock<Bool>` a la izquierda y `ValueBlock` a la derecha. Los scopes de ambos lados son independientes; las locales del lado izquierdo no pasan al derecho. El entorno exterior común y el `value` contextual funcional siguen disponibles conforme a sus contratos.

Las llaves sustituyen solo al operando extendido. Se admiten libremente las cuatro combinaciones breve/extensa:

```mud
key -> value
key -> { result }
{ key } -> value
{ key } -> { result }
```

y las equivalentes con `-->`. No se introducen keywords auxiliares ni wrapper exterior obligatorio. Un bloque trivial de una sola expresión es válido aunque el tooling pueda sugerir abreviarlo.

Aplicar un diccionario sigue siendo exteriormente puro aunque el resultado use mutabilidad temporal local.

### Metadata integrada

Todo propietario que tenga simultáneamente descriptor metadata-bearing propio y `ValueBlock` puede escribir sus declaraciones `~...` como preámbulo contiguo al comienzo del cuerpo extenso. Ese preámbulo se proyecta al descriptor y no forma parte de `ValueBlock`.

Se aplica a campos almacenados/calculados/públicos, componentes y campos calculados de alias, y datos almacenados/calculados de `family`. No se aplica a `ThingInitializer`, overrides, asignaciones de miembro, locales, `given` ni a `Metadata` misma. `Metadata` sigue siendo terminal.

Una declaración no combina simultáneamente el preámbulo integrado y un segundo metadata-body. La forma breve puede conservar el metadata-body separado existente. Los defaults de metadata de fichero mantienen su contrato constante y no adquieren `ValueBlock`.

## Consecuencias

- `ExpressionBlock` permanece declarativo y no puede recuperar mutabilidad por anidamiento de un bloque de valor como expresión primaria.
- La construcción imperativa local de un valor no obliga a convertir el cálculo en efecto del mundo.
- `EffectBlock` y `ValueBlock` comparten declaraciones locales, pero difieren por su frontera de escritura y por la presencia obligatoria de un resultado en el segundo.
- Los slots locales mutables pueden satisfacer participantes `for mut` sin crear un sistema general de references.
- `min` y `max` componen filtrado y orden ya existente en vez de inventar una expresión de clave propia.
- La metadata integrada es azúcar de superficie; el AST conserva metadata y valor en campos separados del mismo propietario.

## Verificación

1. Forma breve y extensa de cada propietario de `ExpressionBlock` y `ValueBlock`.
2. Rechazo de `if`, efectos exteriores y mutación que escape de `ValueBlock`.
3. Declaraciones `:=`, `=` y `mut ... =` locales con ámbitos y sombreado correctos.
4. `LocalForEach` anidado, filtro puro y cuerpo sin resultado obligatorio.
5. Acumulador ordenado secuencial y acumulador no ordenado consolidado; diferencia entre `+=` y `=`.
6. Binding readonly y `for mut` de cada clase local, incluido rollback.
7. `min`/`max` booleanos que devuelven testigos, fuente ordenada sin clave y `empty` sin candidatos.
8. Las cuatro combinaciones breve/extensa de `->` y `-->`, con scopes independientes.
9. Metadata integrada proyectada al descriptor y rechazo de una segunda metadata-body.
10. Default de `given` todavía constante.
11. `TestAfterBlock`, `start with`, metadata-only bodies y preámbulos compartidos de comportamiento conservan sus contratos especiales.
