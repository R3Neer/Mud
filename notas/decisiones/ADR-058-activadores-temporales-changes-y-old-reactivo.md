---
id: D-058
title: "Activadores temporales, `changes` y `old` reactivo"
status: vigente
date: 2026-07-29
supersedes: []
superseded-by: []
questions:
  - "Q-005"
affects:
  - "[[especificacion/07-gramatica-concreta]], `especificacion/gramatica/mud.ebnf`"
---
# ADR-058 — Activadores temporales, `changes` y `old` reactivo

- Modifica: [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola|D-045]], [[notas/decisiones/ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]], [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]] y [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|D-057]]
- Preguntas relacionadas: Q-005
- Ampliada por: [[notas/decisiones/ADR-071-vinculaciones-locales-en-bloques-booleanos|D-071]]
- Documentos afectados: [[especificacion/07-gramatica-concreta]], `especificacion/gramatica/mud.ebnf`

## Contexto

D-041 distinguía dos formas completas de `when`: `when e`, que detectaba `false → true`, y `when e changes`, que comparaba valores consecutivos. Aunque la prosa llamaba postfijo a `changes`, la gramática solo lo admitía al final de toda la cláusula. No podían expresarse activadores como:

```mud
when position changes or ready
when position changes and velocity changes
```

Tratar `changes` como un `Bool` ordinario tampoco sirve. Si el valor cambia en dos transiciones consecutivas, el pulso sería verdadero en ambas y una segunda detección exterior `false → true` perdería la segunda.

## Decisión

### Activadores

El IR distingue los activadores temporales de los valores `Bool` ordinarios:

```text
Trigger
    = Rise(BoolExpression)
    | Temporal(BoolExpression)
    | Changed(Expression)
    | All(Trigger, Trigger)
    | Any(Trigger, Trigger)
```

Para una vinculación $b$, sea $v_n(b,e)$ el valor de la expresión pura $e$ en la instantánea de inicio $W_n$ de la onda $n$.

Un `when e` que no contiene `old` ni `changes` se elabora como un único `Rise(e)`:

$$
\operatorname{Rise}_n(b,e)
\iff
\neg v_{n-1}(b,e)\land v_n(b,e).
$$

Por tanto, los operadores booleanos interiores continúan formando primero una condición de nivel. En particular, `when ready and authorized` detecta que la conjunción completa pasa de falsa a verdadera.

Una expresión booleana de `when` que usa `old` forma un activador `Temporal`: se evalúa directamente sobre el par $(W_{n-1},W_n)$ y pulsa en cada transición donde resulte verdadera. No se somete después a otra detección `false → true`.

`e changes` forma:

$$
\operatorname{Changed}_n(b,e)
\iff
v_{n-1}(b,e)\ne v_n(b,e),
$$

y exige que el tipo de $e$ tenga igualdad definida. Es azúcar temporal equivalente a comparar el valor anterior y el actual:

```mud
e changes
old e != e
```

La equivalencia es semántica; no obliga al compilador a perder la forma original ni su procedencia en el AST.

### Composición

Un trigger produce cero o más matches causales. Las formas temporales `Rise`, `Temporal` y `Changed` describen cuándo una vinculación aporta un match; cuando un operando ordinario `Bool` participa en una composición temporal se eleva a `Rise` como antes.

`and` realiza natural join de los matches compatibles de ambos operandos y, si no comparten bindings, su producto cartesiano. `or` realiza la unión de matches. Las identidades de ocurrencias causales forman parte del match, de modo que dos ocurrencias distintas no se deduplican aunque tengan el mismo payload.

```mud
when position changes and velocity changes
```

requiere matches compatibles cuyas diferencias netas correspondan al mismo paso entre instantáneas. Una subexpresión booleana ordinaria entre paréntesis se eleva como una unidad: `(ready or authorized) and position changes` usa `Rise(ready or authorized)`, no dos fuentes independientes.

Los triggers solo se combinan inicialmente mediante las palabras `and` y `or`. `not`, `xor`, `=>`, `<=>`, `&`, `|` y `^` no aceptan operandos `Trigger`. Esta restricción no impide usar operadores booleanos ordinarios dentro de la expresión booleana de un `Rise` o `Temporal`. D-096 añade además como fuentes declarativas ocurrencias de `message`, disparos de rules reactivas y evaluaciones de `always`.

### Precedencia de `changes`

`changes` es un operador sufijo de la capa temporal. Tiene menos precedencia que las operaciones aritméticas, las conversiones y las comparaciones, pero más que `and` y `or`:

```mud
when position + offset changes
when temperature > limit changes
when position changes or ready
```

se agrupan respectivamente como:

```text
(position + offset) changes
(temperature > limit) changes
(position changes) or ready
```

Para cambiar el alcance lógico se usan paréntesis:

```mud
when (ready and authorized) changes
```

`changes` solo es válido dentro del `when` de una regla reactiva o de un `message`. No produce un valor almacenable, retornable ni utilizable en `if`, `then`, `after`, campos calculados o reglas booleanas.

En la forma de bloque, el operador pertenece a la expresión interior:

```mud
when {
    calendar.day changes
}
```

### `old` en reglas reactivas

Dentro del `when` y el `if` de una regla reactiva:

```text
old e
```

evalúa la expresión pura $e$ en $W_{n-1}$ y conserva su tipo. La expresión debe ser evaluable tanto en $W_{n-1}$ como en $W_n$. No se restringe a la expresión observada por `changes`:

```mud
when price changes
if price > old price and stock < old stock
```

El `if` sin `old` se evalúa sobre $W_n$. `old` no se admite dentro de `then`: D-058 incorpora observación temporal, no efectos retrospectivos.

Dentro del `after` de una acción o test, `old` conserva la semántica de D-042 y D-055: observa el estado estable anterior a la resolución completa, no la onda anterior. Fuera de esos contextos y del `when` o `if` reactivo, `old` es un error estático.

Una comparación temporal puede medir cambios cuantitativos sin sintaxis adicional:

```mud
when position - old position >= 10 meters
```

Por ello MUD 1.0 no introduce `changes by`. Los tipos que admitan resta determinan el tipo y significado de la diferencia; `changes` continúa disponible para cualquier tipo con igualdad.

### Línea base

Para las vinculaciones presentes en la primera instantánea materializada por `start with`:

- cada lectura temporal `old e` toma inicialmente el mismo valor que $e$ en $W_0$;
- `Changed` y `Temporal` memorizan esa línea base y no pulsan por sí mismos;
- un `Rise` conserva el anterior virtual falso de D-041 y puede pulsar si su condición inicial es verdadera;
- en una composición, las ramas temporales no pulsan y las ramas `Rise` se evalúan con ese anterior virtual.

Si una rama `Rise` provoca un disparo inicial, un `old e` usado por el `if` de la regla lee la línea base $W_0$ y por tanto coincide inicialmente con el valor actual de $e$.

Una vinculación nacida después de `start with` conserva la política anterior: su primera onda activa establece toda su línea base sin disparar ningún activador y comienza a comparar en la siguiente.

## Consecuencias

- El AST de superficie conserva `changes` como sufijo y la composición escrita; el modelo semántico debe preservar el comportamiento de cero o más matches, sus bindings/testigos y las identidades causales. D-096 no fija una codificación IR cerrada de esos matches.
- La memoria reactiva conserva los valores anteriores requeridos por `when` e `if`, no solo un booleano agregado.
- Los pulsos temporales pueden producirse en ondas consecutivas.
- Una diferencia cuantitativa utiliza los operadores ordinarios y el sistema de magnitudes.
- La identidad y conservación de esta memoria cuando desaparece una vinculación permanecen en Q-005.

## Alternativas descartadas

### Precedencia máxima

Haría que `position + offset changes` intentase combinar `position` con un activador aplicado solo a `offset`. `changes` debe recibir primero el valor completo construido a su izquierda.

### `changes by`

No fija si la diferencia es firmada, absoluta, exacta o mínima y solo tendría significado directo para algunos tipos. `old` y los operadores ordinarios expresan la comprobación sin una segunda sintaxis.

### `old` solo sobre la expresión cambiada

La transición ya proporciona dos instantáneas completas. Impedir comparaciones cruzadas como precio actual frente a stock anterior no añade seguridad ni simplifica el runtime.

## Verificación

1. `changes` sobre acceso, suma, conversión y comparación con la precedencia acordada.
2. Unión de matches mediante `or` y natural join/producto cartesiano compatible mediante `and`, preservando ocurrencias causalmente distintas.
3. Elevación de un operando booleano ordinario a `Rise` en una composición temporal.
4. Dos cambios consecutivos producen dos pulsos.
5. `old` en `when` mide una diferencia y puede pulsar en transiciones consecutivas.
6. `old` en `if` consulta cualquier expresión pura disponible en ambas instantáneas.
7. Rechazo de `changes` fuera de `when`, de `old` reactivo dentro de `then` y de operadores temporales no admitidos.
8. Ausencia de pulso temporal en la línea base inicial y posible pulso inicial de una rama `Rise`.
9. Una vinculación creada posteriormente establece línea base sin disparar.
10. Rechazo de `changes by`.

## Modificación vigente por D-096

El álgebra de `Trigger` se generaliza de pulsos booleanos a cero o más matches causales. Un match conserva bindings/testigos e identidad de ocurrencias. `and` realiza natural join de matches compatibles y `or` su unión. Messages, rules reactivas y `always` pueden ser fuentes declarativas de trigger; una referencia a declaración `on` no usa paréntesis de llamada.
