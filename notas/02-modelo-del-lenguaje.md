# Modelo del lenguaje

Este documento es dueño del vocabulario semántico de MUD. Resume la estructura conceptual que deberá convertirse en una especificación normativa y una gramática formal.

## Unidades de declaración

MUD tiene cuatro declaraciones principales y una auxiliar:

| Declaración | Representa | Tiene identidad propia |
| --- | --- | --- |
| `construct` | Cosa, concepto, categoría, especialización o familia cerrada | Sí |
| `magnitude` | Cantidad, unidad o punto sobre una cantidad | No como entidad del mundo |
| `rule` | Condición consultable, reacción o invariante | No |
| `action` | Operación externa o composición atómica | No |
| `alias` | Valor estructural nominal o nombre de tipo | No |

Una declaración tiene identidad semántica mediante un ancla. El archivo es una unidad física; el namespace y el tipo de declaración forman parte de su identidad.

## Identidad, valor y especialización

MUD no presupone dos dominios separados de clases y objetos. Un constructo no tiene instancias: los constructos declarados y los creados durante la ejecución pertenecen al mismo dominio conceptual, según [[notas/decisiones/ADR-014-ontologia-unificada-de-constructos|ADR-014]].

Todo constructo concreto denota una cosa con identidad y estado propio, y puede servir a la vez como antecesor de otros constructos. Un constructo abstracto conserva identidad dentro del mismo dominio, pero no denota directamente una cosa concreta con estado propio.

Hay que conservar tres relaciones distintas:

- Los constructos se comparan por identidad.
- Los aliases se comparan por valor estructural.
- `is` expresa especialización nominal no estricta: es reflexiva y transitiva, pero no es igualdad.

Dos constructos creados durante la ejecución con campos iguales siguen teniendo identidades distintas. Dos valores del mismo alias con los mismos componentes son iguales. Aliases diferentes no son intercambiables aunque su forma coincida.

`create C N` crea un nuevo constructo concreto $N$ y establece la misma relación `is` que una declaración estática de especialización. El origen y el ciclo de vida no forman una segunda categoría ontológica.

La especialización directa es acíclica. Su clausura reflexiva y transitiva, consultada mediante `is`, forma un orden parcial.

Los descendientes heredan declaraciones, restricciones, dominios y valores predeterminados efectivos, pero nunca el estado mutable actual de sus antecesores. Cada constructo concreto conserva estado independiente. `create` inicializa desde los predeterminados efectivos y aplica después las asignaciones explícitas de su bloque.

Esta separación debe existir en el sistema de tipos, el IR, el runtime y los materializadores.

## Estado del mundo

El estado se expresa mediante campos:

- Campo almacenado inmutable: `=`.
- Campo almacenado mutable: `mut` y `=`.
- Campo calculado: `:=`.
- Campo con dominio: `in`.
- Campo singular, opcional, colección o diccionario mediante cardinalidad.

La mutabilidad exterior de una relación y la capacidad de modificar sus miembros son permisos distintos. No existe mutabilidad profunda implícita.

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
